# =============================================================================
# Buildozer 配置文件 - English Teleprompter
# =============================================================================
# 【重要声明】本配置文件仅属于「teleprompter」仓库！
# 
# 【修复说明】
# 错误日志：build-tools folder not found /home/runner/.buildozer/android/platform/android-sdk/build-tools
# 根本原因：之前使用了错误的section名称[app:android]，Buildozer不识别
# 修复方案：所有android配置必须在[app]section中，使用android.xxx格式
# =============================================================================

[app]

# 应用基本信息
title = English Teleprompter
package.name = teleprompter
package.domain = org.teleprompter
version = 1.0.0

# 源代码配置
source.dir = .
source.main = main.py
source.include_exts = py,png,jpg,kv,atlas,json,fst,conf,bin,txt,md,scorer

# 排除不需要的目录
source.exclude_dirs = tests,bin,.git,.github,__pycache__,.venv,.buildozer

# 屏幕方向和全屏
orientation = portrait
fullscreen = 0

# =============================================================================
# Python依赖
# 【注意】暂时不包含vosk，因为它可能无法通过p4a编译
# =============================================================================
requirements = python3,kivy==2.2.1,pyjnius

# =============================================================================
# Android 配置（必须在[app]section中！）
# =============================================================================

# Android API版本
android.api = 33
android.minapi = 24
android.ndk = 25c

# 【关键修复】指定build-tools版本，避免Buildozer自动下载36.1
# 对应日志错误：license is not accepted: Android SDK Build-Tools 36.1
android.build_tools_version = 34.0.0

# 目标架构
android.archs = arm64-v8a

# 权限声明
android.permissions = RECORD_AUDIO,BLUETOOTH,BLUETOOTH_ADMIN,BLUETOOTH_CONNECT,BLUETOOTH_SCAN,MODIFY_AUDIO_SETTINGS,INTERNET

# 使用SDL2后端
android.bootstrap = sdl2

# 【关键修复】接受SDK许可
# 对应日志错误：license is not accepted
android.accept_sdk_license = True

# 【关键修复】指定系统SDK路径
# 对应日志错误：build-tools folder not found /home/runner/.buildozer/android/platform/android-sdk
android.sdk_path = /usr/local/lib/android/sdk
android.ndk_path = /usr/local/lib/android/sdk/ndk/25.2.9519653

# 允许备份
android.allow_backup = True

# =============================================================================
# Buildozer 配置
# =============================================================================

[buildozer]

# 详细日志
log_level = 2
warn_on_root = 0

# 构建目录
build_dir = ./.buildozer
bin_dir = ./bin
