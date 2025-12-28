# =============================================================================
# Buildozer 配置文件 - English Teleprompter
# =============================================================================
# 【重要声明】本配置文件仅属于「teleprompter」仓库！
# 与现有网站仓库无任何代码/配置交集，无冲突风险！
#
# 用途：使用Buildozer将Kivy应用打包为Android APK
# 环境：GitHub Codespaces / GitHub Actions
# =============================================================================

[app]

# 应用名称（显示在安卓桌面）
title = English Teleprompter

# 包名（唯一标识符，格式：org.组织名.应用名）
package.name = teleprompter

# 包域名
package.domain = org.teleprompter

# 源代码目录（当前目录）
source.dir = .

# 源代码文件类型
source.include_exts = py,png,jpg,kv,atlas,json

# 排除的文件/目录（减小APK体积）
source.exclude_dirs = tests, bin, .git, .github, __pycache__, .venv

# 主程序入口
source.main = main.py

# 应用版本
version = 1.0.0

# 需要的Python包
# vosk: 离线语音识别引擎
# 注意：vosk会在打包时自动包含
requirements = python3,kivy==2.2.1,vosk,pyjnius

# 预设模式：标准Python
presplash.filename = 

# 应用图标（可选，使用默认）
icon.filename = 

# 屏幕方向：纵向（适配平板竖屏）
orientation = portrait

# 是否全屏
fullscreen = 0

# =============================================================================
# Android 配置
# =============================================================================

[app:android]

# Android API版本配置
android.api = 33
android.minapi = 24
android.ndk = 25b
android.sdk = 33

# 目标架构（ARM64，现代安卓设备主流架构）
android.archs = arm64-v8a

# 权限声明（蓝牙麦克风必需）
android.permissions = 
    RECORD_AUDIO,
    BLUETOOTH,
    BLUETOOTH_ADMIN,
    BLUETOOTH_CONNECT,
    BLUETOOTH_SCAN,
    MODIFY_AUDIO_SETTINGS,
    INTERNET

# 允许备份
android.allow_backup = True

# 使用SDL2后端
android.bootstrap = sdl2

# 接受SDK许可协议
android.accept_sdk_license = True

# =============================================================================
# 【关键配置】强制使用系统级SDK，解决GitHub Actions许可问题
# 说明：Buildozer默认会下载私有SDK到~/.buildozer，与系统SDK隔离
#       必须显式指定路径，才能使用已接受许可的系统SDK
# =============================================================================
android.sdk_path = /usr/local/lib/android/sdk
android.ndk_path = /usr/local/lib/android/sdk/ndk/25.2.9519653

# Android Gradle插件版本
android.gradle_dependencies = 

# 额外的Java库
# android.add_jars = 

# 额外的AAR库
# android.add_aars = 

# 额外的Gradle仓库
# android.add_gradle_repositories = 

# 额外的Gradle依赖
# android.gradle_dependencies = 

# 特性声明
android.features = android.hardware.microphone

# 元数据
android.meta_data = 

# 额外的清单XML
# android.extra_manifest_xml = 

# 额外的清单应用参数
# android.extra_manifest_application_arguments = 

# 资源目录
# android.add_assets = 

# =============================================================================
# Buildozer 配置
# =============================================================================

[buildozer]

# 日志级别（2=详细）
log_level = 2

# 构建警告模式
warn_on_root = 1

# 构建目录
build_dir = ./.buildozer

# 输出目录
bin_dir = ./bin

