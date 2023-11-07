@REM 仮想環境作成
cd src

pyinstaller installer.py --onefile --noconsole

pyinstaller test.py --onefile --noconsole

pyinstaller test.py --onefile

pause