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
set TagName="v2.5.0"
@REM ���|�W�g����
set DirectoryName="YakunyakuKonjac"

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


@REM ���|�W�g���̃f�B���N�g�������݂���Ȃ�
if exist "%DirectoryName%" (
    msg * "���ɃC���X�g�[���ς݂̃f�B���N�g�������o����܂����B�ăC���X�g�[�����s���ꍇ�́A"^

    "�܂��͎蓮�Ŋ����� '%DirectoryName%'�f�B���N�g�����폜���Ă��������B"^

    "���̌�A�C���X�g�[���[���Ď��s���Ă��������B"
    pause
    exit
)

@REM requirements��URL
set RequirementsURL="https://raw.githubusercontent.com/k4r44g3/YakunyakuKonjac/main/document/venv_backup/requirements/py%PythonMajorVersion%.%PythonMinorVersion%_requirements.txt"

@REM �R�}���h��\������
@echo on

@REM ���z���쐬
py -m venv venv_YakunyakuKonjac
cd venv_YakunyakuKonjac
call Scripts\activate.bat

@REM �p�b�P�[�W�C���X�g�[�� �^�C���A�E�g��100�b�ɕύX
pip install -r %RequirementsURL% --verbose --default-timeout=100

@REM �G���[�����������Ȃ�(�I���R�[�h��0�ȊO�Ȃ�)
if %errorlevel% neq 0 (
  msg * "�p�b�P�[�W�̃_�E�����[�h�Ɏ��s���܂����B"^

  "�G���[�R�[�h: %ERRORLEVEL%""
  pause
  exit
)

@REM ��̃u�����`���_�E�����[�h����
git clone %GitRepositoryUrl% -b empty --depth 1

@REM �G���[�����������Ȃ�(�I���R�[�h��0�ȊO�Ȃ�)
if %errorlevel% neq 0 (
  msg * "�\�t�g�E�F�A�̃_�E�����[�h�Ɏ��s���܂����B"^

  "�G���[�R�[�h: %ERRORLEVEL%""
  pause
  exit
)

@REM REM ���|�W�g���̃f�B���N�g���Ɉړ�
cd YakunyakuKonjac

@REM Git �̃o�b�t�@�T�C�Y�𑝂₷
git config --local http.postBuffer 52428800

@REM HTTP�̃o�[�W������ݒ肷��
git config --local http.version HTTP/1.1

@REM git����N���[��(�w�肵���^�O�̃R�~�b�g�̂�)
git fetch origin refs/tags/%TagName% --depth 1

@REM �G���[�����������Ȃ�(�I���R�[�h��0�ȊO�Ȃ�)
if %errorlevel% neq 0 (
  msg * "�\�t�g�E�F�A�̃_�E�����[�h�Ɏ��s���܂����B"^

  "�G���[�R�[�h: %ERRORLEVEL%""
  pause
  exit
)

@REM �Ō�Ƀt�F�b�`�����R�~�b�g�ֈړ�
git checkout FETCH_HEAD

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