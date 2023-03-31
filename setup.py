# coding: utf-8
# cx_Freeze 用セットアップファイル

import sys
from cx_Freeze import setup, Executable

packages = []
includes=[]
excludes = []

base = None
if sys.platform == "win32":
    base = "Win32GUI"
exe = Executable(script = "CalibrationTool.py", base= base, icon='cotechworks_icon.ico')

setup(
    name="CalibrationTool",
    version="1.2",
    description="Tension Meter Calibration Tool",
    options={'build_exe': {'includes': includes, 'excludes': excludes, 'packages': packages}},
    executables=[(exe)]
)