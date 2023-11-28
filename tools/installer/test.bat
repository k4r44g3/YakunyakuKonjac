@REM AWSの設定
@REM aws configure

@REM 仮想環境作成
py -3.8 -m venv venv_YakunyakuKonjac
cd venv_YakunyakuKonjac
call Scripts\activate.bat

@REM パッケージインストール タイムアウトを100秒に変更

@REM AWS関連
pip --default-timeout=100 install pywin32

@REM パッケージ一覧出力ファイルの作成
pip freeze > requirements.txt
pause