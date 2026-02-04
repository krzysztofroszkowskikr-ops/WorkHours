[app]

# (str) Title of your application
title = WorkHours

# (str) Package name
package.name = workhours

# (str) Package domain (needed for android/ios packaging)
package.domain = org.workhours

# (source.dir) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,txt,db

# (list) List of inclusions using pattern matching
source.include_patterns = assets/*,images/*

# (str) Application versioning (method 1)
version = 1.0.0

# (str) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy==2.3.0,kivymd==0.104.2,reportlab,plyer,pillow

# (str) Permissions
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,ACCESS_FINE_LOCATION,CAMERA

# (list) Pattern to whitelist for the whole project
android.whitelist = lib-dynload/termios.so

# (list) Application meta-data
android.meta_data = com.google.android.gms.version=@integer/google_play_services_version

# (str) Android app theme
android.theme = "@android:style/Theme.NoTitleBar"

# (bool) Copy library instead of making a libpymodules.so
android.copy_libs = 1

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a

# (bool) Enable AndroidX support
android.enable_androidx = True

# (int) Target Android API level
android.api = 31

# (int) Minimum API level
android.minapi = 21

# (int) Android SDK version to use
android.sdk = 30

# (str) Android NDK version to use
android.ndk = 25b

# (str) Android logcat filters to use
android.logcat_filters = *:S python:D

android.sdk_path = C:\Users\Kris\AppData\Local\Android\Sdk
android.ndk_path = C:\Android\ndk\r27d

# (str) Jack compiler to use
# android.jack = 1

# (str) Android bootloader RAMDISK
# android.bootloader = /path/to/bootloader

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (str) Orientation of all the occurrences of orientation
orientation = portrait

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning on async run or missing support
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
build_dir = .buildozer

# (str) Path to build output (i.e. .apk, .aab, .ipa) storage
bin_dir = ./bin
