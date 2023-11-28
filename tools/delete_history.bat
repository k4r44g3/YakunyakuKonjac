@REM 文字コードを"Shift-JIS"に設定 メッセージは非表示
@REM chcp 932 >nul

@REM 履歴フォルダへ移動
cd ..\src\history

@REM 履歴の削除
del /Q image_after\*
del /Q image_before\*

@REM .gitkeepの作成
echo. > image_after\.gitkeep
echo. > image_before\.gitkeep

@REM プロジェクトフォルダへ移動
cd ..\..

@REM キャッシュの削除
rmdir /s /q src\__pycache__
rmdir /s /q src\package\__pycache__
rmdir /s /q src\package\translation\__pycache__
rmdir /s /q src\package\window\__pycache__
rmdir /s /q src\package\thread\__pycache__

@REM エラーログファイル削除
del log\error_detailed.log
del log\error_simple.log

msg * 完了しました