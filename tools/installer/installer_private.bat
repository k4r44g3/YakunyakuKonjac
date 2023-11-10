@REM AWSの設定
@REM aws configure

@REM 仮想環境作成
py -3.8 -m venv venv_YakunyakuKonjac
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

@REM pip install black

@REM パッケージ一覧出力ファイルの作成
pip freeze > requirements.txt

@REM gitからクローン
git clone https://github.com/pppp-987/YakunyakuKonjac.git

@REM プロジェクトファイルに移動
cd YakunyakuKonjac

@REM ブランチ変更
git checkout environment

@REM ディレクトリ構成ファイルの作成
@REM tree /f > directory_tree.txt

@REM VScodeで開く
@REM インタプリタを .\Scripts\python.exeに設定

pause