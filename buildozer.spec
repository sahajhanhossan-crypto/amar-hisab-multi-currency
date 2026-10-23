[app]

# (str) Title of your application
title = Amar Hisab

# (str) Package name
package.name = amarhisab

# (str) Package domain (needed for android packaging)
package.domain = org.amarhisab

# (str) Source files to include (let it empty to include all files)
source.include_exts = py,png,jpg,kv,atlas

# (list) Source directories to include (let it empty to include all)
source.include_dir = 

# (str) Application versioning
version = 1.0

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy,sqlite3

# (str) Supported orientations
orientation = portrait

# (int) Whether to be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (int) Android SDK version to use
android.sdk = 30

# (str) python-for-android branch to use
android.accept_sdk_license = True
