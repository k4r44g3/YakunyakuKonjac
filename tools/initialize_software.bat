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

@REM �����̍폜
del /Q YakunyakuKonjac\src\history\image_after\*.png 2>nul
del /Q YakunyakuKonjac\src\history\image_before\*.png 2>nul

@REM �ݒ�t�@�C���폜
del YakunyakuKonjac\src\config\setting.json 2>nul

@REM �L���b�V���̍폜
rmdir /s /q YakunyakuKonjac\src\__pycache__ 2>nul
rmdir /s /q YakunyakuKonjac\src\package\__pycache__ 2>nul
rmdir /s /q YakunyakuKonjac\src\package\translation\__pycache__ 2>nul
rmdir /s /q YakunyakuKonjac\src\package\window\__pycache__ 2>nul
rmdir /s /q YakunyakuKonjac\src\package\thread\__pycache__ 2>nul

@REM �G���[���O�t�@�C������ɂ���(�A�v���P�[�V�������s���͎��s)
copy nul YakunyakuKonjac\log\error_detailed.log >nul 2>&1
copy nul YakunyakuKonjac\log\error_simple.log >nul 2>&1

@REM AWS�̔F�؏���ݒ�t�@�C���̍폜
rmdir /s /q .aws 2>nul

@REM EasyOCR���f���̍폜
rmdir /s /q .EasyOCR 2>nul