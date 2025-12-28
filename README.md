# 📝 English Teleprompter (英文提词器)

> **【重要声明】本代码仅属于「teleprompter」仓库，与现有网站仓库无任何关联！**

一款专为安卓平板设计的离线英文提词器应用，支持蓝牙麦克风语音识别自动滚动字幕。

## ✨ 核心功能

| 功能 | 说明 |
|------|------|
| 📄 文本输入 | 支持任意英文文案输入/粘贴，自动拆分句子 |
| 🎤 语音识别 | 蓝牙麦克风离线识别，2-3秒更新一次结果 |
| 🎯 智能匹配 | 句子级关键词匹配，容忍发音/拼写错误 |
| 📺 字幕滚动 | 匹配成功自动滚动，支持手动前进/后退 |
| ⚙️ 自定义 | 可调节字体大小、支持暂停/继续 |
| 📴 离线运行 | 所有功能无网络依赖，模型内置 |

## 🛠️ 技术栈

- **UI框架**: Kivy 2.2.1 (跨平台)
- **语音识别**: Vosk (vosk-model-small-en-us-0.15)
- **目标平台**: Android 7.0+ (ARM64)
- **打包工具**: Buildozer + GitHub Actions

## 📱 权限说明

应用会自动申请以下权限（蓝牙麦克风必需）：

- `RECORD_AUDIO` - 录音权限
- `BLUETOOTH_CONNECT` - 蓝牙连接权限 (Android 12+)
- `BLUETOOTH` - 蓝牙基础权限
- `BLUETOOTH_ADMIN` - 蓝牙管理权限
- `BLUETOOTH_SCAN` - 蓝牙扫描权限 (Android 12+)
- `MODIFY_AUDIO_SETTINGS` - 音频设置权限

---

# 🚀 3步极简操作指引

> 全程在GitHub Codespaces（在线VSCode）中完成，无需本地操作！

## 📋 步骤1: 创建GitHub仓库

1. 登录 [GitHub](https://github.com)
2. 点击右上角 `+` → `New repository`
3. 仓库名填写: `teleprompter`
4. 选择 `Public`（公开仓库）
5. 勾选 `Add a README file`
6. 点击 `Create repository`

## 📋 步骤2: 上传代码到仓库

### 方法A：使用GitHub网页上传

1. 进入你的 `teleprompter` 仓库页面
2. 点击 `Add file` → `Upload files`
3. 将以下文件拖拽上传：
   - `main.py`
   - `buildozer.spec`
   - `requirements.txt`
   - `README.md`
4. 创建 `.github/workflows/` 文件夹并上传 `build-apk.yml`
5. 点击 `Commit changes`

### 方法B：使用Codespaces（推荐）

1. 在仓库页面点击绿色 `Code` 按钮
2. 选择 `Codespaces` 标签
3. 点击 `Create codespace on main`
4. 等待Codespaces启动（约1-2分钟）
5. 在终端中执行：

```bash
# 克隆代码（如果需要的话）
# 直接将文件内容复制粘贴到对应文件即可
```

## 📋 步骤3: 触发自动打包APK

### 自动触发
- 每次推送代码到 `main` 分支，GitHub Actions会自动开始构建APK

### 手动触发
1. 进入仓库页面 → `Actions` 标签
2. 左侧选择 `Build Android APK`
3. 点击右侧 `Run workflow` → `Run workflow`
4. 等待构建完成（首次约15-30分钟）
5. 构建完成后，点击构建记录
6. 在 `Artifacts` 区域下载 `teleprompter-apk.zip`
7. 解压后将APK传输到安卓平板安装

---

# 📖 开发说明

## 在Codespaces中运行（测试模式）

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 下载Vosk模型
wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
unzip vosk-model-small-en-us-0.15.zip

# 3. 运行应用（桌面测试模式）
python main.py
```

> ⚠️ 注意：Codespaces中运行仅用于测试UI，语音识别功能需要在真机上测试。

## 本地打包APK（可选）

如果你想在本地打包，需要安装：
- Python 3.10
- Buildozer
- Android SDK/NDK

```bash
# 安装Buildozer
pip install buildozer

# 打包APK
buildozer android debug
```

---

# 🔧 配置说明

## buildozer.spec 关键配置

| 配置项 | 值 | 说明 |
|--------|-----|------|
| `android.api` | 33 | 目标Android API版本 |
| `android.minapi` | 24 | 最低支持Android 7.0 |
| `android.archs` | arm64-v8a | ARM64架构 |
| `orientation` | portrait | 竖屏模式 |

## 修改应用名称

编辑 `buildozer.spec`：
```ini
title = Your App Name
package.name = yourappname
```

## 修改应用图标

1. 准备512x512的PNG图标
2. 放在项目根目录，命名为 `icon.png`
3. 编辑 `buildozer.spec`：
```ini
icon.filename = icon.png
```

---

# ❓ 常见问题

## Q: 构建失败怎么办？

A: 检查以下几点：
1. 确保所有文件都已正确上传
2. 查看GitHub Actions日志，找到具体错误
3. 首次构建可能需要更长时间，请耐心等待

## Q: APK安装失败？

A: 确保：
1. 安卓设备允许安装未知来源应用
2. 设备架构是ARM64（大多数现代设备都是）
3. 安卓版本 ≥ 7.0

## Q: 语音识别不工作？

A: 检查：
1. 是否已授予录音权限
2. 蓝牙麦克风是否已连接并设为默认输入
3. 麦克风是否正常工作

## Q: 如何减小APK体积？

A: 编辑 `buildozer.spec`：
```ini
# 移除不需要的架构
android.archs = arm64-v8a

# 使用更小的模型（需要修改代码）
```

---

# 📄 文件结构

```
teleprompter/
├── main.py                 # 主程序代码
├── buildozer.spec          # Buildozer打包配置
├── requirements.txt        # Python依赖
├── README.md               # 本说明文档
└── .github/
    └── workflows/
        └── build-apk.yml   # GitHub Actions配置
```

---

# 📜 开源协议

本项目采用 MIT 协议开源。

---

# 🙏 致谢

- [Kivy](https://kivy.org/) - 跨平台UI框架
- [Vosk](https://alphacephei.com/vosk/) - 离线语音识别
- [Buildozer](https://buildozer.readthedocs.io/) - Android打包工具

---

**【再次声明】本代码仅属于「teleprompter」仓库，与用户现有网站仓库完全独立，无任何代码/配置交集，无冲突风险！**

