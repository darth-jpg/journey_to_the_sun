# Raquel's Journey to the Sun

Pequeno jogo em Python com Pygame.

## Requisitos
- Python 3.10+ no Windows
- Internet (para instalar dependências na primeira vez)

## Como executar em modo desenvolvimento
```powershell
cd "$Env:USERPROFILE\.cursor\raquel_journey"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

## Como gerar o executável para Windows (simples, onefile)
O script abaixo cria um executável único e inclui automaticamente um ícone caso `assets\sprites\icon.ico` exista.

```powershell
cd "$Env:USERPROFILE\.cursor\raquel_journey"
.\build_windows.bat
```

- Saída esperada: `dist\RaquelsJourney.exe`
- Duplo clique no `.exe` para jogar.

## Estrutura de assets
Os assets são carregados via um helper que funciona tanto em modo dev quanto empacotado:
- `assets/audio/background_music.ogg`
- `assets/sprites/start_screen.png`
- `assets/sprites/background_day.png`
- `assets/sprites/background_night.png`
- `assets/sprites/imagem.png`

Se adicionar novos assets, coloque-os dentro de `assets/` e, ao carregar no código, use o helper `resource_path("assets", "subpasta", "arquivo.ext")`.

## Ícone do executável (opcional)
- Coloque `assets\sprites\icon.ico`
- O build usa automaticamente `--icon` se o ficheiro existir

## Problemas comuns
- Erro ao carregar assets no `.exe`: verifique se o caminho no código usa `resource_path(...)`.
- Áudio sem tocar: confirme `background_music.ogg` em `assets/audio/` e que o volume não está a 0.
- SmartScreen do Windows: clique em “Mais informações” > “Executar assim mesmo”.

## Licença
MIT (ver `LICENSE` no repositório principal, se aplicável).
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
