@REM �t�@�C���ۑ����ɁA�G���R�[�f�B���O��"Shift-JIS"�ɂ���

@REM �R�}���h��\�����Ȃ�
@echo off

@REM �����R�[�h��"Shift-JIS"�ɐݒ� ���b�Z�[�W�͔�\��
chcp 932 >nul

@REM ���z�����L���łȂ��Ȃ�
if not defined VIRTUAL_ENV (
    @REM ���z���̃��[�g�f�B���N�g���ֈړ�
    cd ../..
    @REM ���z���̗L����
    call Scripts\activate.bat
)


@REM �v���W�F�N�g�̃��[�g�f�B���N�g���ֈړ�
cd YakunyakuKonjac

@REM ���݂�HEAD�̃^�O����\��
git describe --tags --exact-match HEAD 2>nul

@REM ���݂�HEAD�Ƀ^�O�����Ă��Ȃ��Ȃ�
if %errorlevel% neq 0 (
    @REM ���݂�HEAD�̒Z�k�n�b�V����\��
    git rev-parse --short HEAD
)

pause