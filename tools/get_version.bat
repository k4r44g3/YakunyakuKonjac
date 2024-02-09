@REM ファイル保存時に、エンコーディングを"Shift-JIS"にする

@REM コマンドを表示しない
@echo off

@REM 文字コードを"Shift-JIS"に設定 メッセージは非表示
chcp 932 >nul

@REM 遅延環境変数 実行時に変数を値に置き換える 変数が使用できるようになる
setlocal enabledelayedexpansion

@REM 仮想環境が有効なら
if defined VIRTUAL_ENV (
    @REM 仮想環境のルートディレクトリへ移動
    cd %VIRTUAL_ENV%

@REM 仮想環境が有効でないなら
) else (
    @REM 仮想環境のルートディレクトリへ移動
    cd ../..
    @REM 仮想環境の有効化
    call Scripts\activate.bat
)

@REM プロジェクトのルートディレクトリへ移動
cd YakunyakuKonjac

@REM 現在のHEADのタグ名を表示
git describe --tags --exact-match HEAD >nul 2>&1

@REM 現在のHEADにタグがついているなら
if %errorlevel% equ 0 (
    @REM 現在のHEADのタグ名を表示
    @REM バッククォート（`）で囲まれた文字列をコマンドとして扱う
    for /f "usebackq delims=" %%A in (`git describe --tags --exact-match HEAD`) do set value=%%A
    set text="現在のバージョン:"
) else (
    @REM 現在のHEADの短縮ハッシュを表示
    @REM バッククォート（`）で囲まれた文字列をコマンドとして扱う
    for /f "usebackq delims=" %%A in (`git rev-parse --short HEAD`) do set value=%%A
    set text="バージョン不明。 ハッシュ値:"
)

@REM ラベルと値の表示
msg * %text% %value%