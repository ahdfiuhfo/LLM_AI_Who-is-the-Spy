@echo off
setlocal

:: 使用 PowerShell 打开文件选择对话框
for /f "delims=" %%I in ('powershell -Command "Add-Type -AssemblyName System.Windows.Forms; $f = New-Object System.Windows.Forms.OpenFileDialog; $f.Filter = 'Python Files (*.py)|*.py'; $f.ShowDialog() | Out-Null; $f.FileName"') do set "python_file=%%I"

:: 检查是否选择了文件
if "%python_file%"=="" (
    echo No file selected.
    pause
    exit /b
)

:: 运行选择的 Python 文件
python "%python_file%"

:: 暂停以查看输出
pause
