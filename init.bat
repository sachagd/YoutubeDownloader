@echo off
SETLOCAL EnableExtensions

:: Checking if pip is available
python -m pip --version >nul 2>&1

if %ERRORLEVEL% neq 0 (
    echo pip is not installed.
    echo pip is necessary to install required Python libraries.
    echo Do you want to install pip now? [Y/N]
    set /p UserInput=

    if /I "%UserInput%"=="Y" (
        echo Installing pip...
        python -m ensurepip
        python -m pip install --upgrade pip

        :: Check if pip installed successfully
        python -m pip --version >nul 2>&1
        if %ERRORLEVEL% neq 0 (
            echo Failed to install pip. Please check your Python installation.
            goto end
        )
        echo pip installed successfully.
    ) else (
        echo pip installation was skipped by user. Exiting setup.
        goto end
    )
)

echo Checking and installing required Python libraries...

:: Set the libraries to install
set "LIBRARIES=pytube beautifulsoup4 requests"

:: Install each library
for %%i in (%LIBRARIES%) do (
    python -c "import %%i" 2>nul
    if errorlevel 1 (
        echo Installing %%i...
        pip install %%i
        echo %%i installed successfully
    ) else (
        echo %%i is already installed.
    )
)

echo All required libraries have been checked and installed if needed.

:: Add the registry key
echo Adding the registry key for the Firefox extension...
set "REG_PATH=HKCU\Software\Mozilla\NativeMessagingHosts\com.sacha.youtubedownloader"
set "DIR=%~dp0"
set "JSON_PATH=%DIR:~0,-1%\native-messaging.json"
reg add "%REG_PATH%" /ve /t REG_SZ /d "%JSON_PATH%" /f

if %ERRORLEVEL% == 0 (
    echo Registry key added successfully.
) else (
    echo Failed to add registry key.
)

:end
pause
ENDLOCAL
start /b "" cmd /c del "%~f0"&exit /b