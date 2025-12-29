# =============================================================================
# Buildozer 閰嶇疆鏂囦欢 - English Teleprompter
# =============================================================================
# 銆愰噸瑕佸０鏄庛€戞湰閰嶇疆鏂囦欢浠呭睘浜庛€宼eleprompter銆嶄粨搴擄紒
# 涓庣幇鏈夌綉绔欎粨搴撴棤浠讳綍浠ｇ爜/閰嶇疆浜ら泦锛屾棤鍐茬獊椋庨櫓锛?#
# 鐢ㄩ€旓細浣跨敤Buildozer灏咾ivy搴旂敤鎵撳寘涓篈ndroid APK
# 鐜锛欸itHub Codespaces / GitHub Actions
# =============================================================================

[app]

# 搴旂敤鍚嶇О锛堟樉绀哄湪瀹夊崜妗岄潰锛?title = English Teleprompter

# 鍖呭悕锛堝敮涓€鏍囪瘑绗︼紝鏍煎紡锛歰rg.缁勭粐鍚?搴旂敤鍚嶏級
package.name = teleprompter

# 鍖呭煙鍚?package.domain = org.teleprompter

# 婧愪唬鐮佺洰褰曪紙褰撳墠鐩綍锛?source.dir = .

# 婧愪唬鐮佹枃浠剁被鍨?source.include_exts = py,png,jpg,kv,atlas,json

# 鎺掗櫎鐨勬枃浠?鐩綍锛堝噺灏廇PK浣撶Н锛?source.exclude_dirs = tests, bin, .git, .github, __pycache__, .venv

# 涓荤▼搴忓叆鍙?source.main = main.py

# 搴旂敤鐗堟湰
version = 1.0.0

# 闇€瑕佺殑Python鍖?# vosk: 绂荤嚎璇煶璇嗗埆寮曟搸
# 娉ㄦ剰锛歷osk浼氬湪鎵撳寘鏃惰嚜鍔ㄥ寘鍚?requirements = python3,kivy==2.2.1,vosk,pyjnius

# 棰勮妯″紡锛氭爣鍑哖ython
presplash.filename = 

# 搴旂敤鍥炬爣锛堝彲閫夛紝浣跨敤榛樿锛?icon.filename = 

# 灞忓箷鏂瑰悜锛氱旱鍚戯紙閫傞厤骞虫澘绔栧睆锛?orientation = portrait

# 鏄惁鍏ㄥ睆
fullscreen = 0

# =============================================================================
# Android 閰嶇疆
# =============================================================================

[app:android]

# Android API鐗堟湰閰嶇疆
android.api = 33
android.minapi = 24
android.ndk = 25b
android.sdk = 33

# 鐩爣鏋舵瀯锛圓RM64锛岀幇浠ｅ畨鍗撹澶囦富娴佹灦鏋勶級
android.archs = arm64-v8a

# 鏉冮檺澹版槑锛堣摑鐗欓害鍏嬮蹇呴渶锛?android.permissions = 
    RECORD_AUDIO,
    BLUETOOTH,
    BLUETOOTH_ADMIN,
    BLUETOOTH_CONNECT,
    BLUETOOTH_SCAN,
    MODIFY_AUDIO_SETTINGS,
    INTERNET

# 鍏佽澶囦唤
android.allow_backup = True

# 浣跨敤SDL2鍚庣
android.bootstrap = sdl2

# 鎺ュ彈SDK璁稿彲鍗忚
android.accept_sdk_license = True

# =============================================================================
# 銆愬叧閿厤缃€戝己鍒朵娇鐢ㄧ郴缁熺骇SDK锛岃В鍐矴itHub Actions璁稿彲闂
# 璇存槑锛欱uildozer榛樿浼氫笅杞界鏈塖DK鍒皛/.buildozer锛屼笌绯荤粺SDK闅旂
#       蹇呴』鏄惧紡鎸囧畾璺緞锛屾墠鑳戒娇鐢ㄥ凡鎺ュ彈璁稿彲鐨勭郴缁烻DK
# =============================================================================
android.sdk_path = /usr/local/lib/android/sdk
android.ndk_path = /usr/local/lib/android/sdk/ndk/25.2.9519653

# Android Gradle鎻掍欢鐗堟湰
android.gradle_dependencies = 

# 棰濆鐨凧ava搴?# android.add_jars = 

# 棰濆鐨凙AR搴?# android.add_aars = 

# 棰濆鐨凣radle浠撳簱
# android.add_gradle_repositories = 

# 棰濆鐨凣radle渚濊禆
# android.gradle_dependencies = 

# 鐗规€у０鏄?android.features = android.hardware.microphone

# 鍏冩暟鎹?android.meta_data = 

# 棰濆鐨勬竻鍗昘ML
# android.extra_manifest_xml = 

# 棰濆鐨勬竻鍗曞簲鐢ㄥ弬鏁?# android.extra_manifest_application_arguments = 

# 璧勬簮鐩綍
# android.add_assets = 

# =============================================================================
# Buildozer 閰嶇疆
# =============================================================================

`nandroid.sdk_path = /usr/local/lib/android/sdk`nandroid.ndk_path = /usr/local/lib/android/sdk/ndk/25.2.9519653[buildozer]

# 鏃ュ織绾у埆锛?=璇︾粏锛?log_level = 2

# 鏋勫缓璀﹀憡妯″紡
warn_on_root = 1

# 鏋勫缓鐩綍
build_dir = ./.buildozer

# 杈撳嚭鐩綍
bin_dir = ./bin


