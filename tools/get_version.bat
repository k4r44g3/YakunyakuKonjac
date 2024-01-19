@REM ファイル保存時に、エンコーディングを"Shift-JIS"にする

@REM コマンドを表示しない
@echo off

@REM 文字コードを"Shift-JIS"に設定 メッセージは非表示
chcp 932 >nul

@REM 仮想環境が有効でないなら
if not defined VIRTUAL_ENV (
    @REM 仮想環境のルートディレクトリへ移動
    cd ../..
    @REM 仮想環境の有効化
    call Scripts\activate.bat
)


@REM プロジェクトのルートディレクトリへ移動
cd YakunyakuKonjac

@REM 最新のコミットの短縮ハッシュとコミットメッセージのタイトルの出力
git log --pretty=format:"%%h %%s" -n 1

pause