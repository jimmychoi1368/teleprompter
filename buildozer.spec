# =============================================================================
# Buildozer 配置文件 - English Teleprompter (v6.0)
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
source.include_patterns = assets/*,images/*,vosk-model-small-en-us-0.15/*
source.exclude_dirs = tests,bin,.git,.github,__pycache__,.venv,.buildozer

# 屏幕配置
orientation = portrait
fullscreen = 0

# Python依赖
requirements = python3,kivy==2.2.1,pyjnius,android

# Android API版本（必须与platforms;android-33一致）
android.api = 33
android.minapi = 24
android.ndk = 25c
android.build_tools = 33.0.2

# 目标架构
android.archs = arm64-v8a

# 权限声明
android.permissions = RECORD_AUDIO,BLUETOOTH,BLUETOOTH_ADMIN,BLUETOOTH_CONNECT,BLUETOOTH_SCAN,MODIFY_AUDIO_SETTINGS,INTERNET

# p4a配置（修复：android.bootstrap已弃用）
p4a.bootstrap = sdl2

# SDK配置
android.accept_sdk_license = True
android.sdk_path = /usr/local/lib/android/sdk
android.ndk_path = /usr/local/lib/android/sdk/ndk/25.2.9519653

# 其他
android.allow_backup = True

# =============================================================================

[buildozer]

log_level = 2
warn_on_root = 0
build_dir = ./.buildozer
bin_dir = ./bin
