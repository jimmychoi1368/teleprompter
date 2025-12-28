# -*- coding: utf-8 -*-
"""
===============================================================================
英文提词器 - English Teleprompter
===============================================================================
【重要声明】本代码仅属于「teleprompter」仓库，与现有网站仓库无任何关联！

功能说明：
1. 支持英文文案输入/粘贴，自动拆分句子并提取关键词
2. 蓝牙麦克风离线语音识别（使用Vosk引擎）
3. 句子级关键词匹配触发字幕滚动
4. 支持暂停/继续、滑动调节速度、调整字体大小
5. 适配安卓平板竖屏，全程离线运行

技术栈：
- Kivy框架（跨平台UI）
- Vosk离线语音识别（vosk-model-small-en-us-0.15）
- 自动申请RECORD_AUDIO、BLUETOOTH_CONNECT权限
===============================================================================
"""

# =============================================================================
# 导入必要的库
# =============================================================================
import os
import sys
import json
import re
import queue
import threading
from pathlib import Path

# Kivy配置必须在导入其他Kivy模块之前设置
os.environ['KIVY_AUDIO'] = 'sdl2'  # 使用SDL2音频后端

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.utils import platform
from kivy.properties import (
    StringProperty, 
    NumericProperty, 
    BooleanProperty,
    ListProperty
)
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp, sp

# =============================================================================
# 安卓平台特定导入和权限申请
# =============================================================================
if platform == 'android':
    # 安卓平台专用导入
    from android.permissions import request_permissions, Permission
    from jnius import autoclass
    
    # 申请必要权限：录音权限 + 蓝牙连接权限
    # 这些权限是蓝牙麦克风正常工作的必要条件
    request_permissions([
        Permission.RECORD_AUDIO,           # 录音权限
        Permission.BLUETOOTH_CONNECT,       # 蓝牙连接权限（Android 12+需要）
        Permission.BLUETOOTH,               # 蓝牙基础权限
        Permission.BLUETOOTH_ADMIN,         # 蓝牙管理权限
        Permission.BLUETOOTH_SCAN,          # 蓝牙扫描权限（Android 12+需要）
        Permission.MODIFY_AUDIO_SETTINGS,   # 音频设置权限
    ])
    
    # 获取安卓音频管理器，用于配置蓝牙麦克风
    AudioManager = autoclass('android.media.AudioManager')
    Context = autoclass('android.content.Context')

# =============================================================================
# Vosk语音识别引擎封装类
# =============================================================================
class VoskRecognizer:
    """
    Vosk离线语音识别器封装类
    
    功能：
    - 自动下载/加载vosk-model-small-en-us-0.15模型
    - 处理音频流并返回识别结果
    - 每2-3秒更新一次识别结果
    """
    
    def __init__(self):
        """初始化识别器"""
        self.model = None           # Vosk模型对象
        self.recognizer = None      # Vosk识别器对象
        self.is_running = False     # 识别是否正在运行
        self.result_queue = queue.Queue()  # 识别结果队列
        self.audio_queue = queue.Queue()   # 音频数据队列
        
    def load_model(self):
        """
        加载Vosk语音识别模型
        
        模型路径说明：
        - 安卓：存放在应用私有目录
        - 其他平台：存放在当前目录
        """
        try:
            from vosk import Model, KaldiRecognizer
            
            # 确定模型路径
            if platform == 'android':
                # 安卓平台使用应用私有存储
                from android.storage import app_storage_path
                model_path = os.path.join(app_storage_path(), 'vosk-model-small-en-us-0.15')
            else:
                # 其他平台使用当前目录
                model_path = './vosk-model-small-en-us-0.15'
            
            # 检查模型是否存在
            if not os.path.exists(model_path):
                print(f"[警告] 模型不存在: {model_path}")
                print("[提示] 请下载模型: https://alphacephei.com/vosk/models")
                return False
            
            # 加载模型
            print(f"[信息] 正在加载Vosk模型: {model_path}")
            self.model = Model(model_path)
            
            # 创建识别器，采样率16000Hz（标准语音识别采样率）
            self.recognizer = KaldiRecognizer(self.model, 16000)
            self.recognizer.SetWords(True)  # 启用单词级别识别
            
            print("[成功] Vosk模型加载完成！")
            return True
            
        except ImportError:
            print("[错误] 未安装Vosk库，请运行: pip install vosk")
            return False
        except Exception as e:
            print(f"[错误] 加载模型失败: {e}")
            return False
    
    def process_audio(self, audio_data):
        """
        处理音频数据并返回识别结果
        
        参数：
            audio_data: 16位PCM音频数据（bytes）
            
        返回：
            识别到的文本（如果有），否则返回None
        """
        if self.recognizer is None:
            return None
            
        try:
            # 将音频数据送入识别器
            if self.recognizer.AcceptWaveform(audio_data):
                # 获取完整识别结果
                result = json.loads(self.recognizer.Result())
                text = result.get('text', '').strip()
                if text:
                    return text
            else:
                # 获取部分识别结果（实时反馈）
                partial = json.loads(self.recognizer.PartialResult())
                text = partial.get('partial', '').strip()
                if text:
                    return f"[部分] {text}"
        except Exception as e:
            print(f"[错误] 音频处理失败: {e}")
            
        return None

# =============================================================================
# 音频录制类（支持蓝牙麦克风）
# =============================================================================
class AudioRecorder:
    """
    音频录制器类
    
    功能：
    - 自动检测并使用蓝牙麦克风
    - 16000Hz采样率，单声道，16位深度
    - 后台线程持续录制
    """
    
    def __init__(self, callback=None):
        """
        初始化录制器
        
        参数：
            callback: 音频数据回调函数
        """
        self.callback = callback    # 音频数据回调
        self.is_recording = False   # 是否正在录制
        self.stream = None          # 音频流对象
        self.thread = None          # 录制线程
        
        # 音频参数配置
        self.sample_rate = 16000    # 采样率（Vosk推荐16000Hz）
        self.channels = 1           # 单声道
        self.chunk_size = 4000      # 每次读取的采样点数（约250ms）
        
    def start(self):
        """开始录制音频"""
        if self.is_recording:
            return
            
        self.is_recording = True
        
        if platform == 'android':
            # 安卓平台：使用AudioRecord API
            self._start_android_recording()
        else:
            # 其他平台：使用sounddevice库
            self._start_desktop_recording()
    
    def _start_android_recording(self):
        """安卓平台录音实现"""
        try:
            from jnius import autoclass
            
            # 获取安卓音频相关类
            AudioRecord = autoclass('android.media.AudioRecord')
            AudioFormat = autoclass('android.media.AudioFormat')
            MediaRecorder = autoclass('android.media.MediaRecorder')
            
            # 配置音频参数
            # 使用VOICE_COMMUNICATION以优化蓝牙麦克风
            audio_source = MediaRecorder.AudioSource.VOICE_COMMUNICATION
            channel_config = AudioFormat.CHANNEL_IN_MONO
            audio_format = AudioFormat.ENCODING_PCM_16BIT
            
            # 计算缓冲区大小
            buffer_size = AudioRecord.getMinBufferSize(
                self.sample_rate,
                channel_config,
                audio_format
            )
            buffer_size = max(buffer_size, self.chunk_size * 2)
            
            # 创建AudioRecord对象
            self.stream = AudioRecord(
                audio_source,
                self.sample_rate,
                channel_config,
                audio_format,
                buffer_size
            )
            
            # 开始录制
            self.stream.startRecording()
            
            # 启动后台线程读取音频数据
            self.thread = threading.Thread(target=self._android_record_loop, daemon=True)
            self.thread.start()
            
            print("[成功] 安卓录音已启动（蓝牙麦克风模式）")
            
        except Exception as e:
            print(f"[错误] 安卓录音启动失败: {e}")
            self.is_recording = False
    
    def _android_record_loop(self):
        """安卓录音循环（后台线程）"""
        from jnius import autoclass
        import array
        
        while self.is_recording and self.stream:
            try:
                # 创建缓冲区
                buffer = array.array('h', [0] * self.chunk_size)
                
                # 读取音频数据
                read_size = self.stream.read(buffer, 0, self.chunk_size)
                
                if read_size > 0:
                    # 转换为bytes并回调
                    audio_bytes = buffer[:read_size].tobytes()
                    if self.callback:
                        self.callback(audio_bytes)
                        
            except Exception as e:
                print(f"[错误] 录音读取失败: {e}")
                break
    
    def _start_desktop_recording(self):
        """桌面平台录音实现（用于开发测试）"""
        try:
            import sounddevice as sd
            
            def audio_callback(indata, frames, time, status):
                """音频数据回调"""
                if status:
                    print(f"[警告] 音频状态: {status}")
                if self.callback:
                    # 转换为16位整数格式
                    audio_data = (indata * 32767).astype('int16').tobytes()
                    self.callback(audio_data)
            
            # 创建输入流
            self.stream = sd.InputStream(
                samplerate=self.sample_rate,
                channels=self.channels,
                dtype='float32',
                blocksize=self.chunk_size,
                callback=audio_callback
            )
            self.stream.start()
            
            print("[成功] 桌面录音已启动")
            
        except ImportError:
            print("[警告] 未安装sounddevice库，桌面录音不可用")
            print("[提示] 运行: pip install sounddevice")
        except Exception as e:
            print(f"[错误] 桌面录音启动失败: {e}")
            self.is_recording = False
    
    def stop(self):
        """停止录制"""
        self.is_recording = False
        
        if self.stream:
            try:
                if platform == 'android':
                    self.stream.stop()
                    self.stream.release()
                else:
                    self.stream.stop()
                    self.stream.close()
            except:
                pass
            self.stream = None
        
        print("[信息] 录音已停止")

# =============================================================================
# 文本处理工具类
# =============================================================================
class TextProcessor:
    """
    文本处理工具类
    
    功能：
    - 将文本拆分为句子
    - 提取每句的关键词（用于匹配）
    - 容错处理（忽略标点、大小写，容忍拼写错误）
    """
    
    @staticmethod
    def split_sentences(text):
        """
        将文本拆分为句子列表
        
        参数：
            text: 原始文本
            
        返回：
            句子列表 [{"text": "原句", "keywords": ["关键词"]}]
        """
        if not text:
            return []
        
        # 使用正则表达式按句子结束符拆分
        # 保留句号、问号、感叹号作为分隔
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        
        result = []
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence:
                keywords = TextProcessor.extract_keywords(sentence)
                result.append({
                    'text': sentence,
                    'keywords': keywords
                })
        
        return result
    
    @staticmethod
    def extract_keywords(sentence):
        """
        从句子中提取关键词
        
        规则：
        - 移除常见停用词（a, the, is, are等）
        - 提取长度>=3的单词
        - 转为小写便于匹配
        
        参数：
            sentence: 句子文本
            
        返回：
            关键词列表
        """
        # 常见英文停用词列表
        stop_words = {
            'a', 'an', 'the', 'is', 'are', 'was', 'were', 'be', 'been',
            'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
            'would', 'could', 'should', 'may', 'might', 'must', 'shall',
            'can', 'need', 'dare', 'ought', 'used', 'to', 'of', 'in',
            'for', 'on', 'with', 'at', 'by', 'from', 'as', 'into',
            'through', 'during', 'before', 'after', 'above', 'below',
            'between', 'under', 'again', 'further', 'then', 'once',
            'here', 'there', 'when', 'where', 'why', 'how', 'all',
            'each', 'few', 'more', 'most', 'other', 'some', 'such',
            'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than',
            'too', 'very', 'just', 'and', 'but', 'if', 'or', 'because',
            'until', 'while', 'although', 'though', 'this', 'that',
            'these', 'those', 'it', 'its', 'i', 'you', 'he', 'she',
            'we', 'they', 'my', 'your', 'his', 'her', 'our', 'their'
        }
        
        # 提取单词（只保留字母）
        words = re.findall(r'[a-zA-Z]+', sentence)
        
        # 过滤：移除停用词，保留长度>=3的单词
        keywords = [
            word.lower() 
            for word in words 
            if word.lower() not in stop_words and len(word) >= 3
        ]
        
        return keywords
    
    @staticmethod
    def match_keywords(recognized_text, target_keywords, threshold=0.5):
        """
        检查识别文本是否匹配目标关键词
        
        参数：
            recognized_text: 语音识别结果
            target_keywords: 目标句子的关键词列表
            threshold: 匹配阈值（匹配到的关键词比例）
            
        返回：
            是否匹配成功
        """
        if not target_keywords:
            return False
            
        # 提取识别文本中的单词
        recognized_words = set(
            word.lower() 
            for word in re.findall(r'[a-zA-Z]+', recognized_text)
        )
        
        # 计算匹配的关键词数量
        matched = sum(
            1 for kw in target_keywords 
            if kw in recognized_words or 
               any(TextProcessor.fuzzy_match(kw, rw) for rw in recognized_words)
        )
        
        # 计算匹配率
        match_ratio = matched / len(target_keywords)
        
        return match_ratio >= threshold
    
    @staticmethod
    def fuzzy_match(word1, word2, max_distance=2):
        """
        模糊匹配两个单词（容忍拼写错误）
        
        使用编辑距离算法，允许最多max_distance个字符的差异
        
        参数：
            word1, word2: 待比较的单词
            max_distance: 最大允许编辑距离
            
        返回：
            是否匹配
        """
        if abs(len(word1) - len(word2)) > max_distance:
            return False
            
        # 简化的编辑距离计算
        if len(word1) < 4 or len(word2) < 4:
            # 短单词要求完全匹配
            return word1 == word2
        
        # 计算编辑距离
        distance = TextProcessor._edit_distance(word1, word2)
        return distance <= max_distance
    
    @staticmethod
    def _edit_distance(s1, s2):
        """计算两个字符串的编辑距离（Levenshtein距离）"""
        if len(s1) < len(s2):
            return TextProcessor._edit_distance(s2, s1)
        
        if len(s2) == 0:
            return len(s1)
        
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]

# =============================================================================
# 文本输入界面（Screen 1）
# =============================================================================
class TextInputScreen(Screen):
    """
    文本输入界面
    
    功能：
    - 输入/粘贴英文文案
    - 预览拆分后的句子
    - 跳转到提词界面
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'input'
        self._build_ui()
    
    def _build_ui(self):
        """构建UI界面"""
        # 主布局（垂直排列）
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        # 设置背景色
        with layout.canvas.before:
            Color(0.12, 0.12, 0.15, 1)  # 深灰色背景
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
        layout.bind(size=self._update_rect, pos=self._update_rect)
        
        # 标题
        title = Label(
            text='📝 English Teleprompter',
            font_size=sp(28),
            size_hint_y=None,
            height=dp(50),
            color=(0.9, 0.9, 0.9, 1),
            bold=True
        )
        layout.add_widget(title)
        
        # 说明文字
        hint = Label(
            text='Paste or type your script below:',
            font_size=sp(16),
            size_hint_y=None,
            height=dp(30),
            color=(0.7, 0.7, 0.7, 1)
        )
        layout.add_widget(hint)
        
        # 文本输入框
        self.text_input = TextInput(
            hint_text='Enter your English script here...\n\nExample:\nWelcome to our channel. Today we will discuss something important. Please subscribe and like this video.',
            font_size=sp(18),
            size_hint_y=0.6,
            background_color=(0.18, 0.18, 0.22, 1),
            foreground_color=(0.95, 0.95, 0.95, 1),
            cursor_color=(0.3, 0.7, 1, 1),
            padding=[dp(15), dp(15), dp(15), dp(15)],
            multiline=True
        )
        layout.add_widget(self.text_input)
        
        # 句子预览区域
        preview_label = Label(
            text='Sentences Preview:',
            font_size=sp(14),
            size_hint_y=None,
            height=dp(25),
            color=(0.6, 0.6, 0.6, 1)
        )
        layout.add_widget(preview_label)
        
        # 预览滚动区
        preview_scroll = ScrollView(size_hint_y=0.2)
        self.preview_text = Label(
            text='[Sentences will appear here after parsing]',
            font_size=sp(14),
            size_hint_y=None,
            color=(0.5, 0.8, 0.5, 1),
            text_size=(None, None),
            halign='left',
            valign='top'
        )
        self.preview_text.bind(texture_size=self._update_preview_size)
        preview_scroll.add_widget(self.preview_text)
        layout.add_widget(preview_scroll)
        
        # 按钮区域
        btn_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(60), spacing=dp(15))
        
        # 解析按钮
        parse_btn = Button(
            text='🔍 Parse Text',
            font_size=sp(18),
            background_color=(0.2, 0.5, 0.8, 1),
            background_normal=''
        )
        parse_btn.bind(on_press=self._on_parse)
        btn_layout.add_widget(parse_btn)
        
        # 开始按钮
        start_btn = Button(
            text='▶ Start Teleprompter',
            font_size=sp(18),
            background_color=(0.3, 0.7, 0.4, 1),
            background_normal=''
        )
        start_btn.bind(on_press=self._on_start)
        btn_layout.add_widget(start_btn)
        
        layout.add_widget(btn_layout)
        self.add_widget(layout)
    
    def _update_rect(self, *args):
        """更新背景矩形"""
        self.rect.size = self.children[0].size
        self.rect.pos = self.children[0].pos
    
    def _update_preview_size(self, *args):
        """更新预览文本大小"""
        self.preview_text.height = self.preview_text.texture_size[1]
        self.preview_text.text_size = (self.preview_text.width, None)
    
    def _on_parse(self, *args):
        """解析文本"""
        text = self.text_input.text.strip()
        if not text:
            self.preview_text.text = '[Please enter some text first]'
            return
        
        # 拆分句子
        sentences = TextProcessor.split_sentences(text)
        
        # 显示预览
        preview_lines = []
        for i, sent in enumerate(sentences, 1):
            keywords_str = ', '.join(sent['keywords'][:5])  # 最多显示5个关键词
            preview_lines.append(f"{i}. {sent['text'][:50]}...")
            preview_lines.append(f"   Keywords: {keywords_str}")
        
        self.preview_text.text = '\n'.join(preview_lines) or '[No sentences found]'
        
        # 保存解析结果到App
        App.get_running_app().sentences = sentences
    
    def _on_start(self, *args):
        """开始提词"""
        text = self.text_input.text.strip()
        if not text:
            # 显示提示
            popup = Popup(
                title='Notice',
                content=Label(text='Please enter some text first!'),
                size_hint=(0.8, 0.3)
            )
            popup.open()
            return
        
        # 确保文本已解析
        sentences = TextProcessor.split_sentences(text)
        App.get_running_app().sentences = sentences
        
        # 切换到提词界面
        self.manager.current = 'teleprompter'

# =============================================================================
# 提词器主界面（Screen 2）
# =============================================================================
class TeleprompterScreen(Screen):
    """
    提词器主界面
    
    功能：
    - 显示当前句子（大字体）
    - 显示语音识别状态
    - 控制滚动速度和字体大小
    - 暂停/继续功能
    """
    
    # 属性定义
    current_sentence = StringProperty('')  # 当前显示的句子
    current_index = NumericProperty(0)     # 当前句子索引
    is_paused = BooleanProperty(False)     # 是否暂停
    font_size = NumericProperty(36)        # 字体大小
    recognition_text = StringProperty('')  # 识别结果显示
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'teleprompter'
        
        # 语音识别相关
        self.recognizer = VoskRecognizer()
        self.recorder = None
        self.recognition_buffer = []  # 识别结果缓冲
        
        self._build_ui()
    
    def _build_ui(self):
        """构建UI界面"""
        # 主布局
        layout = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10))
        
        # 设置深色背景
        with layout.canvas.before:
            Color(0.08, 0.08, 0.1, 1)  # 深黑色背景，减少屏幕刺眼
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
        layout.bind(size=self._update_rect, pos=self._update_rect)
        
        # 顶部控制栏
        top_bar = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50), spacing=dp(10))
        
        # 返回按钮
        back_btn = Button(
            text='← Back',
            font_size=sp(16),
            size_hint_x=0.25,
            background_color=(0.4, 0.4, 0.5, 1),
            background_normal=''
        )
        back_btn.bind(on_press=self._on_back)
        top_bar.add_widget(back_btn)
        
        # 进度显示
        self.progress_label = Label(
            text='0 / 0',
            font_size=sp(16),
            size_hint_x=0.5,
            color=(0.7, 0.7, 0.7, 1)
        )
        top_bar.add_widget(self.progress_label)
        
        # 暂停/继续按钮
        self.pause_btn = Button(
            text='⏸ Pause',
            font_size=sp(16),
            size_hint_x=0.25,
            background_color=(0.8, 0.6, 0.2, 1),
            background_normal=''
        )
        self.pause_btn.bind(on_press=self._toggle_pause)
        top_bar.add_widget(self.pause_btn)
        
        layout.add_widget(top_bar)
        
        # 主字幕显示区域
        subtitle_container = BoxLayout(orientation='vertical', size_hint_y=0.5)
        
        # 当前句子标签（大字体、居中）
        self.subtitle_label = Label(
            text='Ready to start...',
            font_size=sp(self.font_size),
            color=(1, 1, 1, 1),
            text_size=(Window.width - dp(40), None),
            halign='center',
            valign='middle',
            bold=True
        )
        self.bind(current_sentence=self._update_subtitle)
        self.bind(font_size=self._update_font_size)
        subtitle_container.add_widget(self.subtitle_label)
        
        layout.add_widget(subtitle_container)
        
        # 下一句预览
        self.next_label = Label(
            text='Next: ...',
            font_size=sp(18),
            size_hint_y=None,
            height=dp(60),
            color=(0.5, 0.5, 0.5, 1),
            text_size=(Window.width - dp(40), None),
            halign='center'
        )
        layout.add_widget(self.next_label)
        
        # 语音识别状态显示
        recognition_container = BoxLayout(
            orientation='vertical', 
            size_hint_y=None, 
            height=dp(80),
            padding=[dp(10), dp(5)]
        )
        
        rec_title = Label(
            text='🎤 Voice Recognition:',
            font_size=sp(14),
            size_hint_y=None,
            height=dp(25),
            color=(0.6, 0.8, 0.6, 1)
        )
        recognition_container.add_widget(rec_title)
        
        self.rec_label = Label(
            text='Waiting for speech...',
            font_size=sp(14),
            color=(0.4, 0.7, 0.4, 1),
            text_size=(Window.width - dp(60), None),
            halign='center'
        )
        self.bind(recognition_text=self._update_rec_text)
        recognition_container.add_widget(self.rec_label)
        
        layout.add_widget(recognition_container)
        
        # 控制滑块区域
        controls = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(120), spacing=dp(5))
        
        # 字体大小滑块
        font_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))
        font_label = Label(
            text='Font Size:',
            font_size=sp(14),
            size_hint_x=0.3,
            color=(0.7, 0.7, 0.7, 1)
        )
        font_row.add_widget(font_label)
        
        self.font_slider = Slider(
            min=24,
            max=72,
            value=36,
            size_hint_x=0.5
        )
        self.font_slider.bind(value=self._on_font_change)
        font_row.add_widget(self.font_slider)
        
        self.font_value = Label(
            text='36',
            font_size=sp(14),
            size_hint_x=0.2,
            color=(0.7, 0.7, 0.7, 1)
        )
        font_row.add_widget(self.font_value)
        controls.add_widget(font_row)
        
        # 手动控制按钮
        manual_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50), spacing=dp(10))
        
        prev_btn = Button(
            text='◀ Previous',
            font_size=sp(16),
            background_color=(0.5, 0.5, 0.6, 1),
            background_normal=''
        )
        prev_btn.bind(on_press=self._prev_sentence)
        manual_row.add_widget(prev_btn)
        
        next_btn = Button(
            text='Next ▶',
            font_size=sp(16),
            background_color=(0.5, 0.5, 0.6, 1),
            background_normal=''
        )
        next_btn.bind(on_press=self._next_sentence)
        manual_row.add_widget(next_btn)
        
        controls.add_widget(manual_row)
        layout.add_widget(controls)
        
        self.add_widget(layout)
    
    def _update_rect(self, *args):
        """更新背景矩形"""
        self.rect.size = self.children[0].size
        self.rect.pos = self.children[0].pos
    
    def _update_subtitle(self, *args):
        """更新字幕显示"""
        self.subtitle_label.text = self.current_sentence
    
    def _update_font_size(self, *args):
        """更新字体大小"""
        self.subtitle_label.font_size = sp(self.font_size)
    
    def _update_rec_text(self, *args):
        """更新识别文本显示"""
        self.rec_label.text = self.recognition_text
    
    def on_enter(self):
        """进入界面时调用"""
        # 重置状态
        self.current_index = 0
        self.is_paused = False
        
        # 获取句子列表
        app = App.get_running_app()
        if hasattr(app, 'sentences') and app.sentences:
            self._show_current_sentence()
            
            # 启动语音识别
            self._start_recognition()
        else:
            self.current_sentence = 'No text loaded!'
    
    def on_leave(self):
        """离开界面时调用"""
        self._stop_recognition()
    
    def _show_current_sentence(self):
        """显示当前句子"""
        app = App.get_running_app()
        sentences = getattr(app, 'sentences', [])
        
        if 0 <= self.current_index < len(sentences):
            self.current_sentence = sentences[self.current_index]['text']
            self.progress_label.text = f'{self.current_index + 1} / {len(sentences)}'
            
            # 显示下一句预览
            if self.current_index + 1 < len(sentences):
                next_text = sentences[self.current_index + 1]['text']
                self.next_label.text = f'Next: {next_text[:60]}...' if len(next_text) > 60 else f'Next: {next_text}'
            else:
                self.next_label.text = 'Next: [End of script]'
        else:
            self.current_sentence = 'End of script!'
            self.next_label.text = ''
    
    def _start_recognition(self):
        """启动语音识别"""
        # 加载Vosk模型
        if not self.recognizer.model:
            model_loaded = self.recognizer.load_model()
            if not model_loaded:
                self.recognition_text = '[Model not loaded - Manual mode]'
                return
        
        # 创建录音器
        self.recorder = AudioRecorder(callback=self._on_audio_data)
        self.recorder.start()
        
        # 启动识别结果处理定时器（每2秒检查一次）
        Clock.schedule_interval(self._process_recognition, 2.0)
        
        self.recognition_text = 'Listening... (Bluetooth Mic)'
    
    def _stop_recognition(self):
        """停止语音识别"""
        if self.recorder:
            self.recorder.stop()
            self.recorder = None
        
        Clock.unschedule(self._process_recognition)
    
    def _on_audio_data(self, audio_data):
        """
        音频数据回调
        
        参数：
            audio_data: PCM音频数据
        """
        if self.is_paused:
            return
            
        # 处理音频并获取识别结果
        result = self.recognizer.process_audio(audio_data)
        
        if result and not result.startswith('[部分]'):
            # 将完整识别结果加入缓冲
            self.recognition_buffer.append(result)
    
    def _process_recognition(self, dt):
        """
        处理识别结果（定时器回调）
        
        每2-3秒执行一次，检查缓冲区的识别结果
        如果匹配当前句子的关键词，触发滚动
        """
        if self.is_paused or not self.recognition_buffer:
            return
        
        # 合并缓冲区的识别结果
        combined_text = ' '.join(self.recognition_buffer)
        self.recognition_text = combined_text[-100:]  # 只显示最后100个字符
        
        # 获取当前句子的关键词
        app = App.get_running_app()
        sentences = getattr(app, 'sentences', [])
        
        if 0 <= self.current_index < len(sentences):
            current_keywords = sentences[self.current_index]['keywords']
            
            # 检查是否匹配
            if TextProcessor.match_keywords(combined_text, current_keywords, threshold=0.4):
                # 匹配成功，滚动到下一句
                print(f"[匹配] 关键词匹配成功，滚动到下一句")
                self._next_sentence()
                
                # 清空缓冲区
                self.recognition_buffer = []
    
    def _toggle_pause(self, *args):
        """切换暂停状态"""
        self.is_paused = not self.is_paused
        
        if self.is_paused:
            self.pause_btn.text = '▶ Resume'
            self.pause_btn.background_color = (0.3, 0.7, 0.4, 1)
            self.recognition_text = '[PAUSED]'
        else:
            self.pause_btn.text = '⏸ Pause'
            self.pause_btn.background_color = (0.8, 0.6, 0.2, 1)
            self.recognition_text = 'Listening...'
    
    def _on_font_change(self, slider, value):
        """字体大小滑块变化"""
        self.font_size = int(value)
        self.font_value.text = str(int(value))
    
    def _prev_sentence(self, *args):
        """上一句"""
        if self.current_index > 0:
            self.current_index -= 1
            self._show_current_sentence()
            self.recognition_buffer = []
    
    def _next_sentence(self, *args):
        """下一句"""
        app = App.get_running_app()
        sentences = getattr(app, 'sentences', [])
        
        if self.current_index < len(sentences) - 1:
            self.current_index += 1
            self._show_current_sentence()
            self.recognition_buffer = []
    
    def _on_back(self, *args):
        """返回上一界面"""
        self._stop_recognition()
        self.manager.current = 'input'

# =============================================================================
# 主应用类
# =============================================================================
class TeleprompterApp(App):
    """
    提词器主应用
    
    【重要声明】本代码仅属于「teleprompter」仓库！
    与现有网站仓库无任何代码/配置交集，无冲突风险！
    """
    
    # 存储解析后的句子
    sentences = []
    
    def build(self):
        """构建应用界面"""
        # 设置窗口标题
        self.title = 'English Teleprompter'
        
        # 设置窗口大小（仅桌面平台生效）
        if platform != 'android':
            Window.size = (400, 700)  # 模拟平板竖屏
        
        # 创建屏幕管理器
        sm = ScreenManager()
        sm.add_widget(TextInputScreen())
        sm.add_widget(TeleprompterScreen())
        
        return sm
    
    def on_start(self):
        """应用启动时调用"""
        print("=" * 60)
        print("English Teleprompter Started!")
        print("=" * 60)
        print("[提示] 本应用仅属于「teleprompter」仓库")
        print("[提示] 与现有网站仓库无任何关联")
        print("=" * 60)

# =============================================================================
# 程序入口
# =============================================================================
if __name__ == '__main__':
    TeleprompterApp().run()

