
@echo off

@REM �����ŁA���d�N���h�~�`�F�b�N�p�̃Z�N�V�����̌Ăяo��
@REM ���݂̃o�b�`�t�@�C���t�@�C���̔r�����b�N�����݂�
Call :_���d�N���h�~ %* 4>>"%~dpnx0"

@REM �������d�N���h�~�`�F�b�N���G���[��Ԃ����ꍇ(�r�����b�N�Ɏ��s�����ꍇ)�A�o�b�`�t�@�C�����I�����܂��B
@REM ���O�Ɏ��s���ꂽ�R�}���h�̏I���R�[�h��0�ȊO(�G���[)�Ȃ�
if %errorlevel% neq 0 (
    @REM �o�b�`�t�@�C���̎��s���I��
    exit /b
)

@REM ���d�N���h�~�`�F�b�N�p�̃Z�N�V�������I��
goto :eof

@REM ���d�N���h�~�`�F�b�N�p�̃Z�N�V����
:_���d�N���h�~


echo a

pause


@REM @REM �t�@�C���ۑ����ɁA�G���R�[�f�B���O��"Shift-JIS"�ɂ���

@REM @REM �R�}���h��\�����Ȃ�
@REM @echo off

@REM @REM �����R�[�h��"Shift-JIS"�ɐݒ� ���b�Z�[�W�͔�\��
@REM chcp 932 >nul

@REM @REM ���z�����L���łȂ��Ȃ�
@REM if not defined VIRTUAL_ENV (
@REM     @REM ���z���̃��[�g�f�B���N�g���ֈړ�
@REM     cd ../..
@REM     @REM ���z���̗L����
@REM     call Scripts\activate.bat
@REM )

@REM echo �N����

@REM @REM AWS�̐ݒ�̕ۑ���̎w��
@REM set AWS_SHARED_CREDENTIALS_FILE=.aws\credentials
@REM @REM AWS�̔F�؏��̕ۑ���̎w��
@REM set AWS_CONFIG_FILE=.aws\config

@REM @REM �A�v���P�[�V�����̎��s
@REM Scripts\python.exe YakunyakuKonjac\src\app.py