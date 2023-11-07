@REM 仮想環境作成
python -m venv venv_installer
cd venv_installer
call Scripts\activate.bat

@REM パッケージインストール
@REM グラフィカルユーザーインターフェイス(GUI)を簡単に作成するためのツール
pip install PySimpleGUI

@REM Pythonプログラムをスタンドアロンの実行可能ファイル(exe, dmg, etc.)に変換するためのツール
pip install pyinstaller

@REM パッケージ一覧出力ファイルの作成
pip freeze > requirements.txt


@REM srcフォルダの作成

@REM installer.pyのコピー

@REM 


@REM gitからクローン
@REM git clone https://github.com/pppp-987/YakunyakuKonjac.git

pause