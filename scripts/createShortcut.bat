@echo off
setlocal

SET dest=%1
SET target=%2
SET script=CreateShortcut.vbs

set dest=%dest:"=%
set target=%target:"=%

echo Set oWS = WScript.CreateObject("WScript.Shell") > %script% 
echo sLinkFile = "%dest%" >> %script%
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> %script%
echo oLink.TargetPath = "%target%" >> %script%
echo oLink.Save >> %script%
cscript //nologo .\%script%
del %script% /f /q
endlocal