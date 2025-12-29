# =============================================================================
# Buildozer 配置文件 - English Teleprompter
# =============================================================================
# 【重要声明】本配置文件仅属于「teleprompter」仓库！
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

# 【修复①】包含所有必要的文件扩展名
# 添加 Vosk 模型需要的扩展名：fst, conf, bin, txt, md
source.include_exts = py,png,jpg,kv,atlas,json,fst,conf,bin,txt,md,scorer

# 【修复②】明确包含 Vosk 模型目录
# 使用 source.include_patterns 确保模型目录被打包
source.include_patterns = vosk-model-small-en-us-0.15/*

# 排除不需要的目录
source.exclude_dirs = tests, bin, .git, .github, __pycache__, .venv, .buildozer

# 屏幕方向和全屏
orientation = portrait
fullscreen = 0

# 【修复③】Python 依赖
# 注意：vosk 可能无法直接通过 p4a 编译，先尝试，如果失败需要用预编译方案
requirements = python3,kivy==2.2.1,pyjnius,android

# =============================================================================
# Android 配置
# =============================================================================

[app:android]

# Android API 版本
android.api = 33
android.minapi = 24
android.sdk = 33

# 【修复④】NDK 版本 - 使用正确的版本标识
android.ndk = 25c

# 目标架构
android.archs = arm64-v8a

# 权限声明
android.permissions = RECORD_AUDIO,BLUETOOTH,BLUETOOTH_ADMIN,BLUETOOTH_CONNECT,BLUETOOTH_SCAN,MODIFY_AUDIO_SETTINGS,INTERNET

# 使用 SDL2 后端
android.bootstrap = sdl2

# 接受 SDK 许可
android.accept_sdk_license = True

# 【关键】指定系统 SDK/NDK 路径
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
