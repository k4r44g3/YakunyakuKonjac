@echo off

@REM �t�@�C���ۑ����ɁA�G���R�[�f�B���O��"Shift-JIS"�ɂ���

@REM �����R�[�h��"Shift-JIS"�ɐݒ� ���b�Z�[�W�͔�\��
chcp 932 >nul

@REM ���z�����L���łȂ��Ȃ�
if not defined VIRTUAL_ENV (
    @REM ���z���̗L����
    cd ../../
    call Scripts\activate.bat
)

@REM AWS�̐ݒ�̕ۑ���̎w��
set AWS_SHARED_CREDENTIALS_FILE=.\.aws\credentials
@REM AWS�̔F�؏��̕ۑ���̎w��
set AWS_CONFIG_FILE=.\.aws\config

echo AWS�ݒ���
echo ���f����ꍇ�ACtrl + Z�������Ă��������B

@REM AWS�̐ݒ�
aws configure

pause

@REM �o�b�`�t�@�C�����I������
exit