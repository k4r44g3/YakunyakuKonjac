@REM �t�@�C���ۑ����ɁA�G���R�[�f�B���O��"Shift-JIS"�ɂ���

@REM �R�}���h��\�����Ȃ�
@REM @echo off

@REM �����R�[�h��"Shift-JIS"�ɐݒ� ���b�Z�[�W�͔�\��
chcp 932 >nul

@REM ���z���쐬
py -3.8 -m venv venv_installer
@REM �J�����g�f�B���N�g�������z���̃��[�g�f�B���N�g���ɂ���
cd venv_installer
@REM ���z���̗L����
call Scripts\activate.bat

@REM �p�b�P�[�W�C���X�g�[��
@REM �O���t�B�J�����[�U�[�C���^�[�t�F�C�X(GUI)���ȒP�ɍ쐬���邽�߂̃c�[��
pip install PySimpleGUI

@REM Python�v���O�������X�^���h�A�����̎��s�\�t�@�C��(exe, dmg, etc.)�ɕϊ����邽�߂̃c�[��
pip install pyinstaller

@REM �p�b�P�[�W�ꗗ�o�̓t�@�C���̍쐬
pip freeze > requirements.txt

@REM src�t�H���_�̍쐬
md src

@REM �C���X�g�[���̃X�N���v�g�̃R�s�[
copy ..\installer_public.py src

copy ..\installer_private.py src

@REM exe�t�@�C���̍쐬(1�̃t�@�C���ɂ܂Ƃ߂�A�R���\�[����\���A�L���b�V���̍폜, ���O�w��)
pyinstaller src\installer_public.py --onefile --noconsole --clean --name installer_public.exe

@REM exe�t�@�C���̃R�s�[
copy dist\installer_public.exe ..\

@REM exe�t�@�C���̍쐬(1�̃t�@�C���ɂ܂Ƃ߂�A�R���\�[����\���A�L���b�V���̍폜, ���O�w��)
pyinstaller src\installer_private.py --onefile --noconsole --clean --name installer_private.exe

@REM exe�t�@�C���̃R�s�[
copy dist\installer_private.exe ..\

@REM ���z�����甲���o��
call Scripts\deactivate.bat

@REM �J�����g�f�B���N�g�������z���̊O�ɂ���
cd ..

@REM ���z���̍폜
RMDIR /S /Q venv_installer

msg * �C���X�g�[���̍쐬���������܂���