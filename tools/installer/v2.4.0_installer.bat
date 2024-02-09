@REM ファイル保存時に、エンコーディングを"Shift-JIS"にする

@REM コマンドを表示しない
@echo off

@REM 文字コードを"Shift-JIS"に設定 メッセージは非表示
chcp 932 >nul

@REM 遅延環境変数 実行時に変数を値に置き換える 変数が使用できるようになる
setlocal enabledelayedexpansion

@REM GitのリポジトリのURL
set GitRepositoryUrl="https://github.com/k4r44g3/YakunyakuKonjac.git"
@REM Gitのタグ名
set TagName="v2.4.0"

@REM Pythonがインストールされているか確認
py --version >nul 2>&1
if %errorlevel% neq 0 (
  msg * "このアプリケーションを実行するにはPythonが必要です。"^

  "Pythonをインストールしてから再度実行してください。"
  pause
  exit
)

@REM Pythonのバージョンを取得
for /f "delims=" %%i in ('py --version') do set "PythonVersion=%%i"

@REM バージョン番号のみを抽出（"Python X.Y.Z"の形式を想定）
for /f "tokens=2" %%s in ("%PythonVersion%") do set "PythonVersionNumber=%%s"

@REM メジャーバージョンとマイナーバージョンを分離
for /f "tokens=1,2 delims=." %%x in ("%PythonVersionNumber%") do (
    set "PythonMajorVersion=%%x"
    set "PythonMinorVersion=%%y"
)

@REM メジャーバージョンが3以外なら
if %PythonMajorVersion% neq 3 (
    msg * "このアプリケーションを実行するにはPython 3.8以上が必要です。"^

    "Python 3.8以上をインストールしてから再度実行してください。"
    pause
    exit
)

@REM マイナーバージョンが8未満なら
if %PythonMinorVersion% lss 8 (
    msg * "このアプリケーションを実行するにはPython 3.8以上が必要です。"^

    "Python 3.8以上をインストールしてから再度実行してください。"
    pause
    exit
)

@REM Gitがインストールされているか確認
git --version >nul 2>&1
if %errorlevel% neq 0 (
  msg * "このアプリケーションを実行するにはGitが必要です。"^

  "Gitをインストールしてから再度実行してください。"
  pause
  exit
)

@REM コマンドを表示する
@echo on

@REM 仮想環境作成
py -m venv venv_YakunyakuKonjac
cd venv_YakunyakuKonjac
call Scripts\activate.bat

@REM パッケージインストール タイムアウトを100秒に変更

@REM AWS関連
pip --default-timeout=100 install awscli
pip --default-timeout=100 install boto3
@REM OCR関連
pip --default-timeout=100 install easyocr
@REM 翻訳関連
pip --default-timeout=100 install deep-translator
@REM GUI関連
pip --default-timeout=100 install keyboard
pip --default-timeout=100 install pyautogui
pip --default-timeout=100 install PySimpleGUI

@REM パッケージ一覧出力ファイルの作成
pip freeze > requirements.txt

@REM gitからクローン(最新のコミットのみ)
git clone -b !TagName! --depth 1 !GitRepositoryUrl!

@REM エラーが発生したなら(終了コードが0以外なら)
if %errorlevel% neq 0 (
  msg * "ソフトウェアのダウンロードに失敗しました。"^

  "インターネット接続を確認して再試行してください。"
  pause
  exit
)

@REM プロジェクトファイルに移動
cd YakunyakuKonjac

@REM ショートカット作成 VBScript使用

@REM ショートカットのリンク先パス
set ShortcutPath="%~dp0\YakunyakuKonjac.lnk"

@REM ショートカットの保存先パス
set TargetPath="%cd%\tools\app.bat"

@REM ショートカットのアイコンのパス
set ShortcutIconPath="%cd%\static\icon\app.ico"

@REM 作業フォルダのパス
set WorkingDirectoryPath="%cd%\tools"

@REM 一時的なVBScriptファイルの作成
copy nul CreateShortcut.vbs

@REM WScript.Shellオブジェクトの作成
echo Set WScriptShell = WScript.CreateObject("WScript.Shell") >> CreateShortcut.vbs

@REM ショートカットの作成
echo Set Shortcut = WScriptShell.CreateShortcut(%ShortcutPath%) >> CreateShortcut.vbs

@REM ショートカットのリンク先パスの設定
echo Shortcut.TargetPath = %TargetPath% >> CreateShortcut.vbs

@REM 作業フォルダの設定
echo Shortcut.WorkingDirectory = %WorkingDirectoryPath% >> CreateShortcut.vbs

@REM ショートカットアイコンの設定
echo Shortcut.IconLocation = %ShortcutIconPath% >> CreateShortcut.vbs

@REM ショートカットを保存
echo Shortcut.Save >> CreateShortcut.vbs

@REM VBSファイルを実行してショートカットを作成
cscript CreateShortcut.vbs

@REM 一時的に作成したVBSファイルを削除
del CreateShortcut.vbs

msg * インストールが完了しました