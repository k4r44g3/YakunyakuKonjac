@REM �����R�[�h��"Shift-JIS"�ɐݒ� ���b�Z�[�W�͔�\��
chcp 932 >nul

@REM �����t�H���_�ֈړ�
cd ..\src\history

@REM �����̍폜
del /Q image_after\*
del /Q image_before\*

@REM .gitkeep�̍쐬
echo. > image_after\.gitkeep
echo. > image_before\.gitkeep

@REM �v���W�F�N�g�t�H���_�ֈړ�
cd ..\..

@REM �L���b�V���̍폜
rmdir /s /q src\__pycache__
rmdir /s /q src\package\__pycache__
rmdir /s /q src\package\translation\__pycache__
rmdir /s /q src\package\window\__pycache__
rmdir /s /q src\package\thread\__pycache__

@REM �G���[���O�t�@�C���폜
del log\error_detailed.log
del log\error_simple.log