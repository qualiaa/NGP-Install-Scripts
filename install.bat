@echo off
:: Next Generation Programmers (NGP) installer script
::
:: This script installs Python, and then executes the python install
:: script which should be located in [install_dir]\scripts\.
:: All installers must be located in [install_dir]\files\.
:: A log is stored at [install_dir]\install.log by default 
:: After the installation, the script requests to reboot.
::
:: Both scripts should be safe to run more than once, but this will
:: clear the logfile.
::
:: Any questions can be sent to j.bayne@warwick.ac.uk

setlocal
setlocal enabledelayedexpansion

:: Default install dir
set install_dir=%HOMEDRIVE%\NGP
set file_dir=files
set script_dir=scripts

:: Installer folder, eg C:\, C:\NGP_Installer
set root_drive=%~d0
set root_dir=%~dp0

:: Keep a log in install folder
set log_file=%root_dir%install.log

:: Check for administrator privileges
net session >nul 2>&1
if %errorlevel% NEQ 0 (
    echo Must run script as administrator
    echo Must run script as administrator >"%log_file%"
    goto End
)



echo:
echo =======================================================
echo:
echo   NGP Installer Script, version 2.0
echo:
echo   Log file is "%log_file%".
echo   If an error occurs, please contact 
echo:
echo       nextgenprogrammers@gmail.com
echo:
echo   attaching your log file
echo: 
echo =======================================================
echo: 

set /P install_dir="Enter installation directory (Default: %install_dir%): "

if not "%install_dir:~1,2%" == ":\" (
	echo %install_dir:~1,2%
	echo Installation path must be absolute 
	echo Must include drive e.g. "C:\" in "C:\NGP"
	goto End
)

echo Starting install script
>"%log_file%"  2>&1 (
	echo Entering %root_drive%, %root_dir%
	%root_drive%
	cd "%root_dir%"
	echo Working directory is !CD!

	if not exist "!install_dir!" (
		echo Directory does not exist. Creating it
		md "!install_dir!"
		if not exist !install_dir! (
			echo Could not create directory "!install_dir!"
			goto Failure
		)
	)

	if not exist "!install_dir!\Python" (
		echo Python not found
		echo Installing Python to !install_dir!\Python
		echo msiexec /i "%file_dir%\python-2.7.10.msi" /quiet TargetDir="!install_dir!\Python"
		msiexec /i "%file_dir%\python-2.7.10.msi" /quiet TargetDir="!install_dir!\Python"
		if !ERRORLEVEL! GTR 0 (
			echo Failed to install Python
			goto Failure
		)
	)
	
	
	set python="!install_dir!\Python\python"
	echo Python: !python!

	echo Starting Python install script
)

%python% "%script_dir%\installer.py"
if !ERRORLEVEL! NEQ 0 goto Failure

choice /m "Restart required. Restart now? "
if !ERRORLEVEL! EQU 1 shutdown /r

goto Success

:Failure
echo:
echo =======================================================
echo:
echo   FAILURE
echo   Some part of installation failed.
echo:
echo   For assistance, contact nextgenprogrammers@gmail.com
echo   Please attach the file 
echo     "%log_file%"
echo:
echo =======================================================
echo:

echo Installation Failed! >> "%log_file%"
goto :End

:Success
echo:
echo =======================================================
echo:
echo   SUCCESS
echo   All components appear to have installed successfully
echo:
echo =======================================================
echo:

echo Installation Successful! >> "%log_file%"

:End
pause
cd ..
echo Exiting script >> "%log_file%"

endlocal
