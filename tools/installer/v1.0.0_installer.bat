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
set TagName="v1.0.0"

REM Python�̃o�[�W�������m�F
py -3.8 --version >nul 2>&1

REM Python 3.8���C���X�g�[������Ă��邩�m�F
if %errorlevel% neq 0 (
  msg * "���̃A�v���P�[�V���������s����ɂ�Python 3.8���K�v�ł��B"^

  "Python 3.8���C���X�g�[�����Ă���ēx���s���Ă��������B"
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
py -3.8 -m venv venv_YakunyakuKonjac
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