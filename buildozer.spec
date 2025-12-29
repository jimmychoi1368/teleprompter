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
# 应用名称（显示在安装界面）
title = English Teleprompter
# 包名（唯一标识符，格式：org.组织名.应用名）
package.name = teleprompter
# 包域名
package.domain = org.teleprompter
# 源码目录（当前目录）
source.dir = .
# 源码文件类型
source.include_exts = py,png,jpg,kv,atlas,json
# 排除的文件/目录（减小APK体积）
source.exclude_dirs = tests, bin, .git, .github, __pycache__, .venv
# 主程序入口
source.main = main.py
# 应用版本
version = 1.0.0
# 需要的Python库
# vosk: 离线语音识别引擎
# 注意：vosk会在打包时自动包含
requirements = python3,kivy==2.2.1,vosk,pyjnius
# 启动画面（可选，留空使用默认）
presplash.filename = 
# 应用图标（可选，留空使用默认）
icon.filename = 
# 屏幕方向：竖屏（适配平板）
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
# 目标架构（ARM64，适配大多数现代安卓设备）
android.archs = arm64-v8a
# 权限说明（蓝牙麦克风必需）
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
# 接受SDK许可
android.accept_sdk_license = True
# =============================================================================
# 【关键配置】强制使用系统SDK，解决GitHub Actions许可问题
# 说明：Buildozer默认会下载私有SDK到~/.buildozer，与系统SDK隔离
#       必须指定路径，才能使用已接受许可的系统SDK
# =============================================================================
android.sdk_path = /usr/local/lib/android/sdk
android.ndk_path = /usr/local/lib/android/sdk/ndk/25.2.9519653
# Android Gradle插件版本
android.gradle_dependencies = 
# 额外的Java库（可选）
# android.add_jars = 
# 额外的AAR库（可选）
# android.add_aars = 
# 额外的Gradle仓库（可选）
# android.add_gradle_repositories = 
# 额外的Gradle依赖（可选）
# android.gradle_dependencies = 
# 硬件功能说明（麦克风）
android.features = android.hardware.microphone
# 元数据（可选）
# android.meta_data = 
# 额外的AndroidManifest.xml代码（可选）
# android.extra_manifest_xml = 
# 额外的应用参数（可选）
# android.extra_manifest_application_arguments = 
# 资源目录（可选）
# android.add_assets = 
# =============================================================================
# Buildozer 全局配置
# =============================================================================
[buildozer]
# 日志级别：2=详细（调试用）
log_level = 2
# 构建警告模式
warn_on_root = 1
# 构建目录
build_dir = ./.buildozer
# 输出目录
bin_dir = ./bin