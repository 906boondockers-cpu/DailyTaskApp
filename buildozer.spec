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

# Active Android Permissions
android.permissions = POST_NOTIFICATIONS, SCHEDULE_EXACT_ALARM, WAKE_LOCK

# Modern Android Target Settings (DO NOT ADD DUPLICATES)
android.api = 33
android.minapi = 24
android.ndk = 25b

[buildozer]
log_level = 2
warn_on_root = 1
