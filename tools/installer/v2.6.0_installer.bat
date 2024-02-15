@REM ファイル保存時に、エンコーディングを"Shift-JIS"にする

@REM コマンドを表示しない
@echo off

@REM 文字コードを"Shift-JIS"に設定 メッセージは非表示
chcp 932 >nul

@REM 遅延環境変数 実行時に変数を値に置き換える 変数が使用できるようになる
setlocal enabledelayedexpansion

@REM Gitのユーザー名
set "GitUserName=k4r44g3"
@REM リポジトリ名
set "RepositoryName=YakunyakuKonjac"
@REM Gitのバージョン番号
set "VersionNumber=2.6.0"

@REM GitのリポジトリのURL
set "GitRepositoryUrl=https://github.com/%GitUserName%/%RepositoryName%"
@REM Gitのタグ名
set "TagName=v%VersionNumber%"
@REM Gitのタグの参照先
set "TagReference=refs/tags/%TagName%"
@REM Gitのzipファイルベース名
set "zipFileBaseName=%RepositoryName%-%VersionNumber%"

@REM 仮想環境名
set "VenvName=venv_%RepositoryName%"

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

@REM リポジトリのディレクトリが存在するなら
if exist "%VenvName%/%RepositoryName%" (
    msg * "既にインストール済みのディレクトリが検出されました。再インストールを行う場合は、"^

    "'%VenvName%/%RepositoryName%'ディレクトリを削除してください。"^

    "その後、インストーラーを再実行してください。"
    pause
    exit
)

@REM requirementsのURL
set RequirementsURL="https://raw.githubusercontent.com/%GitUserName%/%RepositoryName%/main/document/venv_backup/requirements/py%PythonMajorVersion%.%PythonMinorVersion%_requirements.txt"

@REM コマンドを表示する
@echo on

@REM 仮想環境作成
py -m venv %VenvName%
cd %VenvName%
call Scripts\activate.bat

echo "パッケージのインストールを開始します。"

@REM パッケージインストール タイムアウトを100秒に変更 インストール中の処理を表示する
pip install -r %RequirementsURL% --verbose --default-timeout=100

@REM エラーが発生したなら(終了コードが0以外なら)
if %errorlevel% neq 0 (
  msg * "パッケージのダウンロードに失敗しました。"^

  "エラーコード: %ERRORLEVEL%""
  pause
  exit
)

echo "ソフトウェアのzipファイルのダウンロードを開始します。"

@REM zipファイルのダウンロード プログレスバー付き
curl -#L "https://github.com/%GitUserName%/%RepositoryName%/archive/%TagReference%.zip" -o "%zipFileBaseName%.zip"
@REM エラーが発生したなら(終了コードが0以外なら)
if %errorlevel% neq 0 (
  msg * "ソフトウェアのzipファイルのダウンロードに失敗しました。"^

  "エラーコード: %ERRORLEVEL%""
  pause
  exit
)

echo "ソフトウェアのzipファイルの解凍を開始します。"

@REM zipファイルの解凍
call powershell -Command "Expand-Archive -Path '%zipFileBaseName%.zip' -DestinationPath '.' -Force"
@REM エラーが発生したなら(終了コードが0以外なら)
if %errorlevel% neq 0 (
  msg * "ソフトウェアのzipファイルの解凍に失敗しました。"^

  "エラーコード: %ERRORLEVEL%""
  pause
  exit
)

@REM ディレクトリ名の変更
rename %zipFileBaseName% %RepositoryName%
@REM エラーが発生したなら(終了コードが0以外なら)
if %errorlevel% neq 0 (
  msg * "ソフトウェアのディレクトリ名の変更に失敗しました。"^

  "エラーコード: %ERRORLEVEL%""
  pause
  exit
)

@REM zipファイルの削除
del /Q %zipFileBaseName%.zip 2>nul
@REM エラーが発生したなら(終了コードが0以外なら)
if %errorlevel% neq 0 (
  msg * "ソフトウェアのzipファイルの削除に失敗しました。"^

  "エラーコード: %ERRORLEVEL%""
  pause
  exit
)

@REM ショートカット作成 VBScript使用

@REM ショートカットの保存先パス
set ShortcutPath="%~dp0\%RepositoryName%.lnk"

@REM ショートカットのリンク先パス
set TargetPath="%cd%\%RepositoryName%\tools\app.bat"

@REM ショートカットのアイコンのパス
set ShortcutIconPath="%cd%\%RepositoryName%\static\icon\app.ico"

@REM 作業フォルダのパス
set WorkingDirectoryPath="%cd%\%RepositoryName%\\tools"

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
@REM エラーが発生したなら(終了コードが0以外なら)
if %errorlevel% neq 0 (
  msg * "ソフトウェアのショートカット作成に失敗しました。"^

  "エラーコード: %ERRORLEVEL%""
  pause
  exit
)

@REM 一時的に作成したVBSファイルを削除
del CreateShortcut.vbs

@REM ソフトウェアの初回起動
start "" %ShortcutPath%

msg * "インストールが完了しました"^

"ソフトウェアを起動します。"
