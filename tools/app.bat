@echo off

@REM ファイル保存時に、エンコーディングを"Shift-JIS"にする

@REM 文字コードを"Shift-JIS"に設定 メッセージは非表示
chcp 932 >nul

@REM 仮想環境が有効でないなら
if not defined VIRTUAL_ENV (
    @REM 仮想環境の有効化
    cd ../../
    call Scripts\activate.bat
)

@REM AWSの設定の保存先の指定
set AWS_SHARED_CREDENTIALS_FILE=.\.aws\credentials
@REM AWSの認証情報の保存先の指定
set AWS_CONFIG_FILE=.\.aws\config

@REM アプリケーションの実行
Scripts\python.exe YakunyakuKonjac\src\app.py