# Buildozer 配置文件 - English Teleprompter
[app]
title = English Teleprompter
package.name = teleprompter
package.domain = org.teleprompter
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
source.exclude_dirs = tests, bin, .git, .github, __pycache__, .venv
source.main = main.py
version = 1.0.0
requirements = python3,kivy==2.2.1,vosk,pyjnius
presplash.filename = 
icon.filename = 
orientation = portrait
fullscreen = 0

[app:android]
android.api = 33
android.minapi = 24
android.ndk = 25b
android.sdk = 33
android.archs = arm64-v8a
android.permissions = RECORD_AUDIO,BLUETOOTH,BLUETOOTH_ADMIN,BLUETOOTH_CONNECT,BLUETOOTH_SCAN,MODIFY_AUDIO_SETTINGS,INTERNET
android.allow_backup = True
android.bootstrap = sdl2
android.accept_sdk_license = True
android.sdk_path = /usr/local/lib/android/sdk
android.ndk_path = /usr/local/lib/android/sdk/ndk/25.2.9519653
android.features = android.hardware.microphone

[buildozer]
log_level = 2
build_dir = ./.buildozer
bin_dir = ./bin