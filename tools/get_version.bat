@REM �t�@�C���ۑ����ɁA�G���R�[�f�B���O��"Shift-JIS"�ɂ���

@REM �R�}���h��\�����Ȃ�
@echo off

@REM �����R�[�h��"Shift-JIS"�ɐݒ� ���b�Z�[�W�͔�\��
chcp 932 >nul

@REM �x�����ϐ� ���s���ɕϐ���l�ɒu�������� �ϐ����g�p�ł���悤�ɂȂ�
setlocal enabledelayedexpansion

@REM ���z�����L���Ȃ�
if defined VIRTUAL_ENV (
    @REM ���z���̃��[�g�f�B���N�g���ֈړ�
    cd %VIRTUAL_ENV%

@REM ���z�����L���łȂ��Ȃ�
) else (
    @REM ���z���̃��[�g�f�B���N�g���ֈړ�
    cd ../..
    @REM ���z���̗L����
    call Scripts\activate.bat
)

@REM �v���W�F�N�g�̃��[�g�f�B���N�g���ֈړ�
cd YakunyakuKonjac

@REM ���݂�HEAD�̃^�O����\��
git describe --tags --exact-match HEAD >nul 2>&1

@REM ���݂�HEAD�Ƀ^�O�����Ă���Ȃ�
if %errorlevel% equ 0 (
    @REM ���݂�HEAD�̃^�O����\��
    @REM �o�b�N�N�H�[�g�i`�j�ň͂܂ꂽ��������R�}���h�Ƃ��Ĉ���
    for /f "usebackq delims=" %%A in (`git describe --tags --exact-match HEAD`) do set value=%%A
    set text="���݂̃o�[�W����:"
) else (
    @REM ���݂�HEAD�̒Z�k�n�b�V����\��
    @REM �o�b�N�N�H�[�g�i`�j�ň͂܂ꂽ��������R�}���h�Ƃ��Ĉ���
    for /f "usebackq delims=" %%A in (`git rev-parse --short HEAD`) do set value=%%A
    set text="�o�[�W�����s���B �n�b�V���l:"
)

@REM ���x���ƒl�̕\��
msg * %text% %value%