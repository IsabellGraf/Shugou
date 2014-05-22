[app]
# (str) Title of your application
title = Shugou
# (str) Package name
package.name = shugou
# (str) Package domain (needed for android/ios packaging)
package.domain = org.cantor.shugou
# (str) Source code where the main.py live
source.dir = /Users/jerome/dev/Collection/
# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,kv,wav,pkl,ini
# (list) Source files to exclude (let empty to not exclude anything)
source.exclude_exts = generateLogo.py, generateImages.py
# (list) List of directory to exclude (let empty to not exclude anything)
source.exclude_dirs = build
# (list) List of exclusions using pattern matching
#source.exclude_patterns = license,images/*/*.jpg
# (str) Application versioning (method 1)
# version.regex = __version__ = '(.*)'
# version.filename = %(source.dir)s/main.py
# (str) Application versioning (method 2)
version = 0.5
# (list) Application requirements
requirements = kivy
# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png
# (str) Icon of the application
icon.filename = %(source.dir)s/images/LogoI.png
# (str) Supported orientation (one of landscape, portrait or all)
orientation = all
# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

#
# iOS specific
#
# (str) Name of the certificate to use for signing the debug version
# Get a list of available identities: buildozer ios list_identities
ios.codesign.debug = "iPhone Developer: Jerome Lefebvre (MFWFZA33V4)"
# (str) Name of the certificate to use for signing the release version
ios.codesign.release = %(ios.codesign.debug)s
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# -----------------------------------------------------------------------------
# List as sections
#
# You can define all the "list" as [section:key].
# Each line will be considered as a option to the list.
# Let's take [app] / source.exclude_patterns.
# Instead of doing:
#
#     [app]
#     source.exclude_patterns = license,data/audio/*.wav,data/images/original/*
#
# This can be translated into:
#
#     [app:source.exclude_patterns]
#     license
#     data/audio/*.wav
#     data/images/original/*
#
# -----------------------------------------------------------------------------
# Profiles
#
# You can extend section / key with a profile
# For example, you want to deploy a demo version of your application without
# HD content. You could first change the title to add "(demo)" in the name
# and extend the excluded directories to remove the HD content.
#
#     [app@demo]
#     title = My Application (demo)
#
#     [app:source.exclude_patterns@demo]
#     images/hd/*
#