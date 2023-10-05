@REM # AWSの設定(先生のを使用)
@REM aws configure

@REM # 仮想環境作成
@REM cd Desktop
python -m venv venv_YakunyakuKonjac
cd venv_YakunyakuKonjac
call Scripts\activate.bat

@REM # インストール
pip install PySimpleGUI
pip install pyautogui
pip install awscli
pip install boto3
pip install black
pip freeze > requirements.txt

@REM # gitからクローン
git clone https://github.com/pppp-987/YakunyakuKonjac.git
@REM cd YakunyakuKonjac

@REM VScodeで開く
@REM # インタプリタを .\Scripts\python.exeに設定