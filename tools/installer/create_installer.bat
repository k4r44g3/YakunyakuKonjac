@REM 仮想環境作成
py -3.8 -m venv venv_installer
cd venv_installer
call Scripts\activate.bat

@REM pipのバージョンアップ
python Scripts\pip.exe install --upgrade pip


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
copy ..\installer.py .\src

@REM exeファイルの作成
pyinstaller .\src\installer.py --onefile --noconsole
@REM pyinstaller .\src\installer.py --onefile

pause