@echo off
echo ����VSCode���ù���������
echo.

if not exist "dist\VSCode���ù���������.exe" (
    echo ����: ��ִ���ļ�������
    pause
    exit /b 1
)

echo ����1: ��ʾ����
"dist\VSCode���ù���������.exe" --help
echo.

echo ����2: ��ʾ·��
"dist\VSCode���ù���������.exe" --show-paths
echo.

echo ����3: �����ò���
echo ע��: �⽫ʵ��ִ�����ò���!
echo ��Ctrl+Cȡ���������������...
pause
"dist\VSCode���ù���������.exe" --reset
echo.

echo �������
pause
