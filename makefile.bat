@ECHO OFF
ECHO Congratulations! Your first batch file executed successfully.
IF EXIST "%~dp0\venv\Scripts\python.exe" (
echo OK
"%~dp0\venv\Scripts\python.exe" "app.py" 
) ELSE (
 ECHO installing pip requirements in venv: python -m venv venv!
 python -m venv venv
 "%~dp0\venv\Scripts\pip" install -r requirements.txt
 
 "%~dp0\venv\Scripts\python.exe" "app.py" 

)

PAUSE
