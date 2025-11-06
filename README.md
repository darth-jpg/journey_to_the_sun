# Raquel's Journey to the Sun

Disclaimer: This was just a testgame that I wanted to create, be aware that can have some bugs, have fun :)

## How to Play (Recommended)
1. Open the executable: `dist\RaquelsJourney.exe`
2. If Windows shows a warning (SmartScreen), click "More info" > "Run anyway".

## How to Run from Source (Optional)
Requires Python 3.10+.

```powershell
cd "$Env:USERPROFILE\.cursor\raquel_journey"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

## How to Build the Executable (if you want to recompile)
```powershell
cd "$Env:USERPROFILE\.cursor\raquel_journey"
.\build_windows.bat
```
Output: `dist\RaquelsJourney.exe`

## Controls
- **Left/Right Arrow**: Move
- **Space**: Jump
- **Enter**: Confirm/Advance dialogue

## Troubleshooting
- Missing assets: Delete `dist/` and `build/` folders, then run the build again.
- No sound: Check your audio device and system volume.
