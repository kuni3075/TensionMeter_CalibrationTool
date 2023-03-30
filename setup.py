# coding: utf-8
# cx_Freeze 用セットアップファイル
 
import sys
from cx_Freeze import setup, Executable
 
base = None
includes=["config"]

# GUI=有効, CUI=無効 にする
if sys.platform == 'win32' : base = 'Win32GUI'
 
# exe にしたい python ファイルを指定
exe = Executable(script = 'CalibrationTool.py', base = base, icon='cotechworks_icon.ico')
 
# セットアップ
setup(name = 'CalibrationTool',
      version = '1.2',
      description = 'CalibrationTool',
      options={"build exe":{"includes":includes}},
      executables = [exe])