@echo off
setlocal

REM Cria venv local
python -m venv .venv

REM Atualiza pip e instala dependencias de build
".venv\Scripts\python.exe" -m pip install --upgrade pip
".venv\Scripts\pip.exe" install -r requirements.txt

REM Define icone opcional se existir
set ICON=assets\sprites\icon.ico
set ICON_FLAG=
if exist "%ICON%" (
  set ICON_FLAG=--icon "%ICON%"
)

REM Build com PyInstaller (onefile para um unico executavel)
".venv\Scripts\pyinstaller.exe" --noconfirm --clean --onefile --windowed --name "RaquelsJourney" ^
  --add-data "assets;assets" %ICON_FLAG% ^
  main.py

echo.
echo Build concluido. O executavel esta em dist\RaquelsJourney\RaquelsJourney.exe
endlocal

