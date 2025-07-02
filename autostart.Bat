@echo off
setlocal

REM 1. Verificar si Python está instalado
where python >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python no está instalado. Iniciando descarga...
    powershell -Command "Invoke-WebRequest https://www.python.org/ftp/python/3.11.8/python-3.11.8-amd64.exe -OutFile python_installer.exe"
    echo Instalando Python...
    python_installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    echo Esperando a que termine la instalación...
    timeout /t 20
    del python_installer.exe
)

REM 2. Verificar que pip esté disponible
python -m ensurepip --upgrade
python -m pip install --upgrade pip

REM 3. Instalar las dependencias
pip install -r requirements.txt

REM 4. Ejecutar la aplicación
echo Ejecutando la plataforma...
streamlit run DBH_plataform.py

pause
