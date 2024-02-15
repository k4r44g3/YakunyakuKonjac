@REM �t�@�C���ۑ����ɁA�G���R�[�f�B���O��"Shift-JIS"�ɂ���

@REM �R�}���h��\�����Ȃ�
@echo off

@REM �����R�[�h��"Shift-JIS"�ɐݒ� ���b�Z�[�W�͔�\��
chcp 932 >nul

@REM �x�����ϐ� ���s���ɕϐ���l�ɒu�������� �ϐ����g�p�ł���悤�ɂȂ�
setlocal enabledelayedexpansion

@REM Git�̃��[�U�[��
set "GitUserName=k4r44g3"
@REM ���|�W�g����
set "RepositoryName=YakunyakuKonjac"
@REM Git�̃o�[�W�����ԍ�
set "VersionNumber=2.6.0"

@REM Git�̃��|�W�g����URL
set "GitRepositoryUrl=https://github.com/%GitUserName%/%RepositoryName%"
@REM Git�̃^�O��
set "TagName=v%VersionNumber%"
@REM Git�̃^�O�̎Q�Ɛ�
set "TagReference=refs/tags/%TagName%"
@REM Git��zip�t�@�C���x�[�X��
set "zipFileBaseName=%RepositoryName%-%VersionNumber%"

@REM ���z����
set "VenvName=venv_%RepositoryName%"

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

@REM ���|�W�g���̃f�B���N�g�������݂���Ȃ�
if exist "%VenvName%/%RepositoryName%" (
    msg * "���ɃC���X�g�[���ς݂̃f�B���N�g�������o����܂����B�ăC���X�g�[�����s���ꍇ�́A"^

    "'%VenvName%/%RepositoryName%'�f�B���N�g�����폜���Ă��������B"^

    "���̌�A�C���X�g�[���[���Ď��s���Ă��������B"
    pause
    exit
)

@REM requirements��URL
set RequirementsURL="https://raw.githubusercontent.com/%GitUserName%/%RepositoryName%/main/document/venv_backup/requirements/py%PythonMajorVersion%.%PythonMinorVersion%_requirements.txt"

@REM �R�}���h��\������
@echo on

@REM ���z���쐬
py -m venv %VenvName%
cd %VenvName%
call Scripts\activate.bat

echo "�p�b�P�[�W�̃C���X�g�[�����J�n���܂��B"

@REM �p�b�P�[�W�C���X�g�[�� �^�C���A�E�g��100�b�ɕύX �C���X�g�[�����̏�����\������
pip install -r %RequirementsURL% --verbose --default-timeout=100

@REM �G���[�����������Ȃ�(�I���R�[�h��0�ȊO�Ȃ�)
if %errorlevel% neq 0 (
  msg * "�p�b�P�[�W�̃_�E�����[�h�Ɏ��s���܂����B"^

  "�G���[�R�[�h: %ERRORLEVEL%""
  pause
  exit
)

echo "�\�t�g�E�F�A��zip�t�@�C���̃_�E�����[�h���J�n���܂��B"

@REM zip�t�@�C���̃_�E�����[�h �v���O���X�o�[�t��
curl -#L "https://github.com/%GitUserName%/%RepositoryName%/archive/%TagReference%.zip" -o "%zipFileBaseName%.zip"
@REM �G���[�����������Ȃ�(�I���R�[�h��0�ȊO�Ȃ�)
if %errorlevel% neq 0 (
  msg * "�\�t�g�E�F�A��zip�t�@�C���̃_�E�����[�h�Ɏ��s���܂����B"^

  "�G���[�R�[�h: %ERRORLEVEL%""
  pause
  exit
)

echo "�\�t�g�E�F�A��zip�t�@�C���̉𓀂��J�n���܂��B"

@REM zip�t�@�C���̉�
call powershell -Command "Expand-Archive -Path '%zipFileBaseName%.zip' -DestinationPath '.' -Force"
@REM �G���[�����������Ȃ�(�I���R�[�h��0�ȊO�Ȃ�)
if %errorlevel% neq 0 (
  msg * "�\�t�g�E�F�A��zip�t�@�C���̉𓀂Ɏ��s���܂����B"^

  "�G���[�R�[�h: %ERRORLEVEL%""
  pause
  exit
)

@REM �f�B���N�g�����̕ύX
rename %zipFileBaseName% %RepositoryName%
@REM �G���[�����������Ȃ�(�I���R�[�h��0�ȊO�Ȃ�)
if %errorlevel% neq 0 (
  msg * "�\�t�g�E�F�A�̃f�B���N�g�����̕ύX�Ɏ��s���܂����B"^

  "�G���[�R�[�h: %ERRORLEVEL%""
  pause
  exit
)

@REM zip�t�@�C���̍폜
del /Q %zipFileBaseName%.zip 2>nul
@REM �G���[�����������Ȃ�(�I���R�[�h��0�ȊO�Ȃ�)
if %errorlevel% neq 0 (
  msg * "�\�t�g�E�F�A��zip�t�@�C���̍폜�Ɏ��s���܂����B"^

  "�G���[�R�[�h: %ERRORLEVEL%""
  pause
  exit
)

@REM �V���[�g�J�b�g�쐬 VBScript�g�p

@REM �V���[�g�J�b�g�̕ۑ���p�X
set ShortcutPath="%~dp0\%RepositoryName%.lnk"

@REM �V���[�g�J�b�g�̃����N��p�X
set TargetPath="%cd%\%RepositoryName%\tools\app.bat"

@REM �V���[�g�J�b�g�̃A�C�R���̃p�X
set ShortcutIconPath="%cd%\%RepositoryName%\static\icon\app.ico"

@REM ��ƃt�H���_�̃p�X
set WorkingDirectoryPath="%cd%\%RepositoryName%\\tools"

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
@REM �G���[�����������Ȃ�(�I���R�[�h��0�ȊO�Ȃ�)
if %errorlevel% neq 0 (
  msg * "�\�t�g�E�F�A�̃V���[�g�J�b�g�쐬�Ɏ��s���܂����B"^

  "�G���[�R�[�h: %ERRORLEVEL%""
  pause
  exit
)

@REM �ꎞ�I�ɍ쐬����VBS�t�@�C�����폜
del CreateShortcut.vbs

@REM �\�t�g�E�F�A�̏���N��
start "" %ShortcutPath%

msg * "�C���X�g�[�����������܂���"^

"�\�t�g�E�F�A���N�����܂��B"
