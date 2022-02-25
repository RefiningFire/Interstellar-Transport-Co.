# This file is imported from __init__.py and exec'd from setup.py

MAJOR = 2
MINOR = 1
MICRO = 0
RELEASE = False

__version__ = '%d.%d.%d' % (MAJOR, MINOR, MICRO)

if not RELEASE:
    # if it's a rcx release, it's not proceeded by a period. If it is a
    # devx release, it must start with a period
    __version__ += 'rc1'


_kivy_git_hash = '87b60702e0bf8eee929ba9ac4db725d12274d7ba'
_kivy_build_date = '20220212'
