[app]
title = Curtsy
package.name = curtsy
package.domain = org.rob
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 1.0.0
orientation = portrait
fullscreen = 0

# Core Requirements
requirements = python3,kivy,plyer,pillow

# Link Your Staged Icon Image Explicitly
icon.filename = %(source.dir)s/icon.png

# Active Android Permissions
android.permissions = POST_NOTIFICATIONS, SCHEDULE_EXACT_ALARM, WAKE_LOCK

# Modern Android Target Settings & 16 KB Emulator Alignment
android.api = 33
android.minapi = 24
android.ndk = 25b
android.ndk_api = 24
android.extra_lflags = -Wl,-z,max-page-size=16384 -Wl,-z,common-page-size=16384

[buildozer]
log_level = 2
warn_on_root = 1
