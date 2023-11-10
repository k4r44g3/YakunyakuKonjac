@REM 仮想環境作成
py -3.8 -m venv venv_installer
@REM カレントディレクトリを仮想環境のルートディレクトリにする
cd venv_installer
@REM 仮想環境の有効化
call Scripts\activate.bat

@REM パッケージインストール
@REM グラフィカルユーザーインターフェイス(GUI)を簡単に作成するためのツール
pip install PySimpleGUI

@REM Pythonプログラムをスタンドアロンの実行可能ファイル(exe, dmg, etc.)に変換するためのツール
pip install pyinstaller

@REM パッケージ一覧出力ファイルの作成
pip freeze > requirements.txt

@REM srcフォルダの作成
md src

@REM installer.pyのコピー
copy ..\installer.py src

@REM exeファイルの作成
pyinstaller src\installer.py --onefile --noconsole

@REM exeファイルのコピー
copy dist\installer.exe ..\

@REM 仮想環境から抜け出す
call Scripts\deactivate.bat

@REM カレントディレクトリを仮想環境の外にする
cd ..

@REM 仮想環境の削除
RMDIR /S /Q venv_installer

pause