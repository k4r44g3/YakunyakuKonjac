@REM �t�@�C���ۑ����ɁA�G���R�[�f�B���O��"Shift-JIS"�ɂ���

@REM �R�}���h��\�����Ȃ�
@echo off

@REM �����R�[�h��"Shift-JIS"�ɐݒ� ���b�Z�[�W�͔�\��
chcp 932 >nul

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


@REM �ݒ�t�@�C���폜
del YakunyakuKonjac\src\config\setting.json 2>nul