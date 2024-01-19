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

@REM プロジェクトファイルに移動
cd YakunyakuKonjac

@REM 最終コミット前の状態まで戻す
git reset --hard HEAD

@REM 更新箇所をダウンロードする
git pull origin

@REM 仮想環境のルートディレクトリへ移動
cd ..


msg * "アップデートが完了しました。"^

"アップデート後にバグが発生する場合は、"^

"initialize_software.bat で初期化してみてください。"