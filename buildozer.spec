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

# 【修复】包含所有必要的文件扩展名
source.include_exts = py,png,jpg,kv,atlas,json,fst,conf,bin,txt,md,scorer

# 【修复】显式包含Vosk模型目录（确保递归打包）
# 注意：需要将模型目录列为include_patterns
source.include_patterns = assets/*,images/*,vosk-model-small-en-us-0.15/*

# 排除不需要的目录
source.exclude_dirs = tests,bin,.git,.github,__pycache__,.venv,.buildozer

# 屏幕方向和全屏
orientation = portrait
fullscreen = 0

# =============================================================================
# Python依赖
# 【重要说明】
# 1. vosk是C++原生库，无法直接通过python-for-android编译
# 2. 正确的做法是使用vosk-android预编译AAR包
# 3. 当前先验证基本Kivy打包能否成功，再处理vosk集成
# 
# 【临时方案】使用不含vosk的依赖，验证打包流程
# 【最终方案】需要使用p4a的recipes或预编译库来集成vosk
# =============================================================================
requirements = python3,kivy==2.2.1,pyjnius,android

# =============================================================================
# Android 配置（必须在[app]section中！）
# =============================================================================

# =============================================================================
# Android API 版本配置
# 【官方文档来源】https://buildozer.readthedocs.io/en/latest/specifications.html
# =============================================================================

# android.api - 目标API版本（必须与安装的platforms;android-xx一致）
# 官方配置名：android.api
android.api = 33

# android.minapi - 最低支持API版本
# 官方配置名：android.minapi
android.minapi = 24

# android.ndk - NDK版本（格式如25c，对应ndk;25.2.9519653）
# 官方配置名：android.ndk
android.ndk = 25c

# android.build_tools - 指定build-tools版本，避免Buildozer自动下载最新版
# 官方配置名：android.build_tools（不是android.build_tools_version！）
# 【重要】此配置告诉python-for-android使用指定版本的build-tools
android.build_tools = 33.0.2

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
