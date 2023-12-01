
@echo off

@REM ここで、多重起動防止チェック用のセクションの呼び出し
@REM 現在のバッチファイルファイルの排他ロックを試みる
Call :_多重起動防止 %* 4>>"%~dpnx0"

@REM もし多重起動防止チェックがエラーを返した場合(排他ロックに失敗した場合)、バッチファイルを終了します。
@REM 直前に実行されたコマンドの終了コードが0以外(エラー)なら
if %errorlevel% neq 0 (
    @REM バッチファイルの実行を終了
    exit /b
)

@REM 多重起動防止チェック用のセクションを終了
goto :eof

@REM 多重起動防止チェック用のセクション
:_多重起動防止


echo a

pause


@REM @REM ファイル保存時に、エンコーディングを"Shift-JIS"にする

@REM @REM コマンドを表示しない
@REM @echo off

@REM @REM 文字コードを"Shift-JIS"に設定 メッセージは非表示
@REM chcp 932 >nul

@REM @REM 仮想環境が有効でないなら
@REM if not defined VIRTUAL_ENV (
@REM     @REM 仮想環境のルートディレクトリへ移動
@REM     cd ../..
@REM     @REM 仮想環境の有効化
@REM     call Scripts\activate.bat
@REM )

@REM echo 起動中

@REM @REM AWSの設定の保存先の指定
@REM set AWS_SHARED_CREDENTIALS_FILE=.aws\credentials
@REM @REM AWSの認証情報の保存先の指定
@REM set AWS_CONFIG_FILE=.aws\config

@REM @REM アプリケーションの実行
@REM Scripts\python.exe YakunyakuKonjac\src\app.py