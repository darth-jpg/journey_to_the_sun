# Raquel's Journey to the Sun

A platformer game where Raquel embarks on a journey to find the sun in the darkness, narrated by Ricardo.

## Description
In this 3-minute adventure, you play as Raquel, a girl with golden hair and slightly tanned skin, who must overcome various challenges to find the sun. The story is narrated by Ricardo, who has dark hair and fair skin.

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