@REM �t�@�C���ۑ����ɁA�G���R�[�f�B���O��"Shift-JIS"�ɂ���

@REM �R�}���h��\�����Ȃ�
@echo off

@REM �����R�[�h��"Shift-JIS"�ɐݒ� ���b�Z�[�W�͔�\��
chcp 932 >nul

@REM �x�����ϐ� ���s���ɕϐ���l�ɒu�������� �ϐ����g�p�ł���悤�ɂȂ�
setlocal enabledelayedexpansion

@REM Git�̃��|�W�g����URL
set GitRepositoryUrl="https://github.com/k4r44g3/YakunyakuKonjac.git"
@REM Git�̃^�O��
set TagName="v2.4.0"

@REM Python���C���X�g�[������Ă��邩�m�F
py --version >nul 2>&1
if %errorlevel% neq 0 (
  msg * "���̃A�v���P�[�V���������s����ɂ�Python���K�v�ł��B"^

  "Python���C���X�g�[�����Ă���ēx���s���Ă��������B"
  pause
  exit
)

@REM Python�̃o�[�W�������擾
for /f "delims=" %%i in ('py --version') do set "PythonVersion=%%i"

@REM �o�[�W�����ԍ��݂̂𒊏o�i"Python X.Y.Z"�̌`����z��j
for /f "tokens=2" %%s in ("%PythonVersion%") do set "PythonVersionNumber=%%s"

@REM ���W���[�o�[�W�����ƃ}�C�i�[�o�[�W�����𕪗�
for /f "tokens=1,2 delims=." %%x in ("%PythonVersionNumber%") do (
    set "PythonMajorVersion=%%x"
    set "PythonMinorVersion=%%y"
)

@REM ���W���[�o�[�W������3�ȊO�Ȃ�
if %PythonMajorVersion% neq 3 (
    msg * "���̃A�v���P�[�V���������s����ɂ�Python 3.8�ȏオ�K�v�ł��B"^

    "Python 3.8�ȏ���C���X�g�[�����Ă���ēx���s���Ă��������B"
    pause
    exit
)

@REM �}�C�i�[�o�[�W������8�����Ȃ�
if %PythonMinorVersion% lss 8 (
    msg * "���̃A�v���P�[�V���������s����ɂ�Python 3.8�ȏオ�K�v�ł��B"^

    "Python 3.8�ȏ���C���X�g�[�����Ă���ēx���s���Ă��������B"
    pause
    exit
)

@REM Git���C���X�g�[������Ă��邩�m�F
git --version >nul 2>&1
if %errorlevel% neq 0 (
  msg * "���̃A�v���P�[�V���������s����ɂ�Git���K�v�ł��B"^

  "Git���C���X�g�[�����Ă���ēx���s���Ă��������B"
  pause
  exit
)

@REM �R�}���h��\������
@echo on

@REM ���z���쐬
py -m venv venv_YakunyakuKonjac
cd venv_YakunyakuKonjac
call Scripts\activate.bat

@REM �p�b�P�[�W�C���X�g�[�� �^�C���A�E�g��100�b�ɕύX

@REM AWS�֘A
pip --default-timeout=100 install awscli
pip --default-timeout=100 install boto3
@REM OCR�֘A
pip --default-timeout=100 install easyocr
@REM �|��֘A
pip --default-timeout=100 install deep-translator
@REM GUI�֘A
pip --default-timeout=100 install keyboard
pip --default-timeout=100 install pyautogui
pip --default-timeout=100 install PySimpleGUI

@REM �p�b�P�[�W�ꗗ�o�̓t�@�C���̍쐬
pip freeze > requirements.txt

@REM git����N���[��(�ŐV�̃R�~�b�g�̂�)
git clone -b !TagName! --depth 1 !GitRepositoryUrl!

@REM �G���[�����������Ȃ�(�I���R�[�h��0�ȊO�Ȃ�)
if %errorlevel% neq 0 (
  msg * "�\�t�g�E�F�A�̃_�E�����[�h�Ɏ��s���܂����B"^

  "�C���^�[�l�b�g�ڑ����m�F���čĎ��s���Ă��������B"
  pause
  exit
)

@REM �v���W�F�N�g�t�@�C���Ɉړ�
cd YakunyakuKonjac

@REM �V���[�g�J�b�g�쐬 VBScript�g�p

@REM �V���[�g�J�b�g�̃����N��p�X
set ShortcutPath="%~dp0\YakunyakuKonjac.lnk"

@REM �V���[�g�J�b�g�̕ۑ���p�X
set TargetPath="%cd%\tools\app.bat"

@REM �V���[�g�J�b�g�̃A�C�R���̃p�X
set ShortcutIconPath="%cd%\static\icon\app.ico"

@REM ��ƃt�H���_�̃p�X
set WorkingDirectoryPath="%cd%\tools"

@REM �ꎞ�I��VBScript�t�@�C���̍쐬
copy nul CreateShortcut.vbs

@REM WScript.Shell�I�u�W�F�N�g�̍쐬
echo Set WScriptShell = WScript.CreateObject("WScript.Shell") >> CreateShortcut.vbs

@REM �V���[�g�J�b�g�̍쐬
echo Set Shortcut = WScriptShell.CreateShortcut(%ShortcutPath%) >> CreateShortcut.vbs

@REM �V���[�g�J�b�g�̃����N��p�X�̐ݒ�
echo Shortcut.TargetPath = %TargetPath% >> CreateShortcut.vbs

@REM ��ƃt�H���_�̐ݒ�
echo Shortcut.WorkingDirectory = %WorkingDirectoryPath% >> CreateShortcut.vbs

@REM �V���[�g�J�b�g�A�C�R���̐ݒ�
echo Shortcut.IconLocation = %ShortcutIconPath% >> CreateShortcut.vbs

@REM �V���[�g�J�b�g��ۑ�
echo Shortcut.Save >> CreateShortcut.vbs

@REM VBS�t�@�C�������s���ăV���[�g�J�b�g���쐬
cscript CreateShortcut.vbs

@REM �ꎞ�I�ɍ쐬����VBS�t�@�C�����폜
del CreateShortcut.vbs

msg * �C���X�g�[�����������܂���