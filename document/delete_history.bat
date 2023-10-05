@REM 履歴フォルダへ移動
cd ..\src\history

@REM 履歴の削除
del /Q image_after\*
del /Q image_before\*
del /Q text_after\*
del /Q text_before\*

@REM .gitkeepの作成
echo. > image_after\.gitkeep
echo. > image_before\.gitkeep
echo. > text_after\.gitkeep
echo. > text_before\.gitkeep

