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

@REM �v���W�F�N�g�t�@�C���Ɉړ�
cd YakunyakuKonjac

@REM �ŏI�R�~�b�g�O�̏�Ԃ܂Ŗ߂�
git reset --hard HEAD

@REM �X�V�ӏ����_�E�����[�h����
git pull origin

@REM ���z���̃��[�g�f�B���N�g���ֈړ�
cd ..


msg * "�A�b�v�f�[�g���������܂����B"^

"�A�b�v�f�[�g��Ƀo�O����������ꍇ�́A"^

"initialize_software.bat �ŏ��������Ă݂Ă��������B"