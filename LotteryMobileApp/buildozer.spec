[app]

# (str) Title of your application
title = 彩票记录与分析工具

# (str) Package name
package.name = lottery.tool

# (str) Package domain (needed for android/ios packaging)
package.domain = org.lottery

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,ttf

# (list) List of inclusions using pattern matching
# source.include_patterns = assets/*,images/*.png

# (list) Source files to exclude (let empty to not exclude anything)
# source.exclude_exts = spec

# (list) List of directory to exclude (let empty to not exclude anything)
source.exclude_dirs = tests, bin, __pycache__, .git, .idea, .vscode, build, dist

# (list) List of exclusions using pattern matching
# source.exclude_patterns = license,images/*/*.jpg

# (str) Application versioning (method 1)
version = 1.0.0

# (str) Application versioning (method 2)
# version.regex = __version__ = ['"](.*)['"]
# version.filename = %(source.dir)s/main.py

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy==2.3.0,requests==2.31.0,plyer==2.4.0,sqlite3

# (str) Custom source folders for requirements
# Sets custom source for any requirements with recipes
# requirements.source.kivy = ../../kivy

# (list) Garden requirements
# garden_requirements =

# (str) Presplash of the application
# presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
# icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (list) List of service to declare
# services = NAME:ENTRYPOINT_TO_PY,NAME2:ENTRYPOINT_TO_PY2

# (str) OSX minimum deployment target (used only for OSX target)
# osx.deployment_target = 10.9

#
# Android specific
#

# (bool) Indicates if the application should be fullscreen or not
fullscreen = 0

# (string) Presplash background color (for android toolchain)
# android.presplash_color = #FFFFFF

# (string) Presplash animation using Lottie format.
# You can create the file using https://lottiefiles.com/ and put the json
# in the data folder
# android.presplash_lottie = "data/presplash.json"

# (str) Adaptive icon of the application (used if Android API level is 26+ at runtime)
# icon.adaptive_foreground.filename = %(source.dir)s/data/icon_adaptive_foreground.png
# icon.adaptive_background.filename = %(source.dir)s/data/icon_adaptive_background.png

# (list) Permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE

# (list) features (adds uses-feature -tags to manifest)
# android.features = android.hardware.usb.host

# (int) Target Android API, should be as high as possible.
# android.api = 31

# (int) Minimum API your APK / AAB will support.
# android.minapi = 21

# (int) Android SDK version to use
# android.sdk = 23

# (str) Android NDK version to use
# android.ndk = 23b

# (int) Android NDK API to use. This is the minimum API your app will support, it should usually match android.minapi.
# android.ndk_api = 21

# (bool) Use --private data storage (True) or --dir public storage (False)
# android.private_storage = True

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
# android.ndk_path =

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
# android.sdk_path =

# (str) ANT directory (if empty, it will be automatically downloaded.)
# android.ant_path =

# (bool) If True, then skip trying to update the Android sdk
# This can be useful to avoid an infinite loop while waiting for user input
# android.skip_update = False

# (bool) If True, then automatically accept SDK license
# android.accept_sdk_license = False

# (str) Android entry point, default is ok for Kivy-based app
# android.entrypoint = org.kivy.android.PythonActivity

# (str) Android app theme, default is ok for Kivy-based app
# android.theme = "@android:style/Theme.NoTitleBar"

# (str) Android logcat filters (default is for Kivy-based app)
# android.logcat_filters = *:S python:D

# (str) Android additional adb arguments (default is empty)
# android.adb_args = -H host.docker.internal

# (bool) Copy library dependencies not found in system Python for Android
# android.copy_libs = 1

# (list) Android Java libraries to add (as Jar files)
# android.add_jar_files =

# (list) Android Java files to add (can be java or a containing directory)
# android.add_java_files =

# (list) Kotlin source files to add (as .kt files)
# android.add_kt_files =

# (list) List of Java classes to add as activities to the manifest.
# android.add_activities =

# (str) OUYA Console category. Should be one of GAME or APP
# If you leave this blank, OUYA support will not be enabled
# android.ouya.category = GAME

# (str) Filename of OUYA Console icon. It must be a 732x412 png image.
# android.ouya.icon.filename = %(source.dir)s/data/ouya_icon.png

# (str) XML file to include as an intent filters in <activity> tag
# android.manifest.intent_filters =

# (str) Android screen size to target (one of small, normal, large, xlarge)
# android.screen_size = normal

# (list) Android screen density to target (one of ldpi, mdpi, hdpi, xhdpi, xxhdpi, xxxhdpi)
# android.screen_density = mdpi

# (list) Android ABI to build for (see https://developer.android.com/ndk/guides/abis)
# Default is all supported ABIs
# android.abi = armeabi-v7a,arm64-v8a,x86,x86_64

# (list) Android APK ABI to build for by default (default is all)
# android.apk_abi = armeabi-v7a,arm64-v8a,x86,x86_64

# (bool) Indicate whether the screen should be into immersive mode (fullscreen with navigation and status bar hidden)
# android.immersive_mode = false

# (list) Android additionnal libraries to copy into libs/armeabi
# android.add_libs_armeabi = libs/android/*.so
# android.add_libs_armeabi_v7a = libs/android-v7/*.so
# android.add_libs_arm64_v8a = libs/android-v8/*.so
# android.add_libs_x86 = libs/android-x86/*.so
# android.add_libs_x86_64 = libs/android-x86/*.so

# (bool) Enable auto building of OpenGL ES 2.0 Java code
# android.opengles2_auto = true

# (bool) Enable AndroidX support (default is set to true if target api level is 28+)
# android.enable_androidx = false

# (bool) Enable data binding (default is false)
# android.enable_databinding = false

# (bool) Enable Jetifier (default is true)
# android.jetifier = true

# (bool) Enable Android Multidex (default is false)
# android.multidex = false

# (bool) Disable the compilation of py to pyc/pyo files when packaging
# android.no-compile-pyo = true

#
# iOS specific
#

# (str) Name of the certificate to use for signing the debug version
# Get a list of available identities: buildozer ios list_identities
# ios.codesign.debug = "iPhone Developer: <lastname> <firstname> (<hexstring>)"

# (str) Name of the certificate to use for signing the release version
# ios.codesign.release = %(ios.codesign.debug)s

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is out of date
# warn_on_buildozer_out_of_date = True

# (str) Path to build artifact storage, absolute or relative to spec file
# build_dir = .buildozer

# (str) Path to build output (i.e. .apk, .aab, .ipa) storage
# bin_dir = bin

# -----------------------------------------------------------------------------
# Profile for Android debug build
# -----------------------------------------------------------------------------

[app:debug]

# (bool) Build a debug version of the application
# Default is False
# debug = 1

# (str) Android signing config for debug
# android.debuggable = true

# (str) Keystore for debug signing
# android.keystore.debug = ~/.android/debug.keystore

# -----------------------------------------------------------------------------
# Profile for Android release build
# -----------------------------------------------------------------------------

[app:release]

# (bool) Build a release version of the application
# Default is False
# release = 1

# (str) Android signing config for release
# android.releasable = true

# (str) Keystore for release signing
# android.keystore.release = /path/to/release.keystore

# (str) Keystore password for release signing
# android.keystore.release.password = PASSWORD

# (str) Key alias for release signing
# android.keystore.release.alias = ALIAS

# (str) Key password for release signing
# android.keystore.release.alias.password = ALIAS_PASSWORD

# (list) List of extra files or directories to add to the tarball
# extra_files =

# (bool) Enable Android App Bundle (AAB) instead of APK
# android.aab = false

# (list) Java classes to add as activities to the manifest
# android.add_activities =

# (list) Extra Android manifest placeholders to add
# android.manifest_placeholders =

# (list) Extra Android manifest entries to add
# android.manifest_entries =

# -----------------------------------------------------------------------------
# Profile for iOS debug build
# -----------------------------------------------------------------------------

[app:ios.debug]

# (bool) Build a debug version of the application
# debug = 1

# (str) Code signing identity for debug
# ios.codesign.debug = "iPhone Developer: <lastname> <firstname> (<hexstring>)"

# -----------------------------------------------------------------------------
# Profile for iOS release build
# -----------------------------------------------------------------------------

[app:ios.release]

# (bool) Build a release version of the application
# release = 1

# (str) Code signing identity for release
# ios.codesign.release = %(ios.codesign.debug)s