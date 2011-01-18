from setuptools import setup

import sys
import os

APP = 'src/TicTacToe.py'
APP_NAME = 'Tic-Tac-Toe'
VERSION = '0.1'
DATA = []

def build_with_py2app():
    setup(
        options=dict(
            py2app=dict(
                site_packages=True,
                resources=DATA,
                plist=dict(
                    CFBundleName               = APP_NAME,
                    CFBundleShortVersionString = VERSION,
                    CFBundleGetInfoString      = APP_NAME + ' ' + VERSION,
                    CFBundleExecutable         = APP_NAME,
                    CFBundleIdentifier         = 'com.zrbecker.' + APP_NAME,
                ),
            ),
        ),
        app=[APP]
    )

def build_with_py2exe():
    pass

if __name__ == '__main__':
    if 'py2app' in sys.argv:
        build_with_py2app()
    elif 'py2exe' in sys.argv:
        build_with_py2exe()
    else:
        setup()
