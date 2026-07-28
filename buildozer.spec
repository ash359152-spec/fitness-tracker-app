[app]

# Title of your application
title = Fitness Tracker

# Package name (no spaces, lowercase)
package.name = fitnesstracker

# Package domain (reverse domain style - just make one up, it doesn't need to be real)
package.domain = org.myapps

# Source code directory
source.dir = .

# Source files to include
source.include_exts = py,png,jpg,kv,atlas,json

# Main file (entry point of the app)
source.main = fitness_tracker_kivy.py

# Application versioning
version = 1.0

# Application requirements
# python3 + kivy are required. json/os/datetime are built into Python already.
requirements = python3,kivy

# Supported orientation (portrait, landscape, or all)
orientation = portrait

# (Optional) Icon and presplash - add these later if you want a custom icon
# icon.filename = %(source.dir)s/icon.png

[buildozer]

# Log level (2 = detailed, useful for debugging build errors)
log_level = 2

# Warn if running as root (usually should NOT run buildozer as root)
warn_on_root = 1

[app:android]

# Minimum Android API level to support
android.minapi = 21

# Target Android API level
android.api = 33

# Android permissions (fitness tracker only needs storage, not internet/camera/etc.)
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
