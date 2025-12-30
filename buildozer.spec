# Buildozer配置 - English Teleprompter (v7.0 推倒重来版)

[app]

title = English Teleprompter
package.name = teleprompter
package.domain = org.teleprompter
version = 1.0.0

source.dir = .
source.main = main.py
source.include_exts = py,png,jpg,kv,atlas,json,fst,conf,bin,txt,md,scorer
source.include_patterns = vosk-model-small-en-us-0.15/*
source.exclude_dirs = tests,bin,.git,.github,__pycache__,.venv,.buildozer

orientation = portrait
fullscreen = 0

requirements = python3,kivy==2.2.1,pyjnius,android

android.api = 33
android.minapi = 24
android.ndk = 25c
android.build_tools = 33.0.2
android.archs = arm64-v8a
android.permissions = RECORD_AUDIO,BLUETOOTH,BLUETOOTH_ADMIN,BLUETOOTH_CONNECT,BLUETOOTH_SCAN,MODIFY_AUDIO_SETTINGS,INTERNET

p4a.bootstrap = sdl2

android.accept_sdk_license = True
android.sdk_path = /usr/local/lib/android/sdk
android.ndk_path = /usr/local/lib/android/sdk/ndk/25.2.9519653
android.allow_backup = True

[buildozer]

log_level = 2
warn_on_root = 0
build_dir = ./.buildozer
bin_dir = ./bin
