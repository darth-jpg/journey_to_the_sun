# Raquel's Journey to the Sun

Jogo em Python (Pygame).

## Como jogar (recomendado)
1) Abra o executável: `dist\RaquelsJourney.exe`
2) Se o Windows alertar (SmartScreen), clique em “Mais informações” > “Executar assim mesmo”.

## Como executar pelo código (opcional)
Requer Python 3.10+.

```powershell
cd "$Env:USERPROFILE\.cursor\raquel_journey"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

## Como gerar o executável (se quiser recompilar)
```powershell
cd "$Env:USERPROFILE\.cursor\raquel_journey"
.\build_windows.bat
```
Saída: `dist\RaquelsJourney.exe`

## Controlos
- Setas Esquerda/Direita: mover
- Espaço: saltar
- Enter: confirmar/avançar diálogo

## Problemas comuns
- Faltam assets: apague `dist/` e `build/` e volte a correr o build.
- Sem som: verifique dispositivo de áudio e volume do sistema.

Licença: MIT.
# Rachel's Journey to the Sun

Disclaimer: This was just a testgame, something I had fun creating, please be advised that can exist some bugs.

## Description
In this 3-minute adventure, you play as Rachel, a girl with golden hair and slightly tanned skin, who must overcome various challenges to find the sun.

## Controls
- **Left Arrow**: Move left
- **Right Arrow**: Move right
- **Space**: Jump

## Installation & Setup

### Development Setup
1. Make sure you have Python 3.x installed
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the game:
   ```bash
   python main.py
   ```
   Or use the batch file:
   ```bash
   run_game.bat
   ```

### Playing the Game
For Windows users, you can download the executable from the `release/` folder:
- Extract the `release/` folder
- Run `RaquelBeta.exe`
- All assets are included

## Features
- Platformer gameplay
- Puzzle elements
- Story-driven narrative
- Pixel art style
- Multiple challenges
- Dynamic lighting system
- Parallax backgrounds
- Sound effects and music

## Project Structure
```
raquel_journey/
├── main.py              # Main game file
├── game_objects.py      # Game objects (platforms, obstacles)
├── level_manager.py     # Level management
├── lighting.py          # Lighting system
├── sprites.py           # Sprite handling
├── story.py             # Story and dialogue
├── sound_manager.py     # Audio management
├── visual_effects.py    # Visual effects
├── assets/              # Game assets (sprites, audio)
└── release/             # Windows executable (not in git)
```

## Requirements
- Python 3.x
- pygame
- See `requirements.txt` for full list

## License
This project is open source and available for personal use. 
