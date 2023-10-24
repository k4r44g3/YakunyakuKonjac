cd ../../
call Scripts\activate.bat
pip freeze > requirements.txt
Scripts\python.exe YakunyakuKonjac\src\app.py
pause