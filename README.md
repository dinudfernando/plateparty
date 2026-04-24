# Plate Party

![Plate Party Logo](https://github.com/dinudfernando/plateparty/blob/main/src/assets/plate_party_logo.png)

University game project for **CS196**.

## Overview

**Plate Party** is a 2D arcade-style balancing game built with Python and the Arcade library.

You play as Pete, a character who catches flying plates while trying to keep a growing stack balanced. As the game goes on, wind and weather make the stack harder to control, turning simple movement into a balancing challenge.

## Gameplay

The goal is to catch as many plates as possible without losing control of the stack.

Each plate you catch is added to the pile above Pete. As the stack grows, movement and weather effects make it harder to stay balanced. If the stack leans too far, the plates spill and the game ends.

### Core mechanics

- Catch moving plates before they hit the ground.
- Build and maintain a stack of plates.
- Balance the stack while moving left and right.
- Survive changing weather conditions.
- Restart after a game over and try to beat your score.

## Features

- Main menu UI.
- In-game pause button.
- Animated player sprite.
- Plate catching and stacking system.
- Balance meter.
- Wind and weather system.
- Game over state with restart.
- Background music and sound effects.

## Controls

- **Left Arrow / A** — Move left
- **Right Arrow / D** — Move right
- **R** — Restart after game over
- **Pause Button** — Pause or resume the game

## Tech Stack

- **Python**
- **Arcade**
- **arcade.gui**

## Project Structure

```text
plateparty/
├── src/
│   ├── main.py
│   └── assets/
│       ├── bg.png
│       ├── croissant.png
│       ├── cracked_plate.png
│       ├── pause_icon.png
│       ├── pause_icon_dark.png
│       ├── pete_walk1.png
│       ├── pete_walk2.png
│       ├── pete_walk3.png
│       ├── plate.png
│       ├── plate_party_logo.png
│       ├── PressStart2P-Regular.ttf
│       ├── click_button.mp3
│       ├── hover_button.mp3
│       ├── game_ost.mp3
│       ├── game_over.mp3
│       ├── game_start.mp3
│       ├── menu_ost.mp3
│       ├── running_sound.mp3
│       ├── wind_gust.mp3
│       └── glass_shatter.mp3
└── README.md
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/dinudfernando/plateparty.git
   cd plateparty
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
   
   On Windows:
   ```bash
   .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install arcade
   ```

4. Run the game:
   ```bash
   python src/main.py
   ```

## Audio

Plate Party includes both OSTs and sound effects to support gameplay and menu interactions.

### Music
- `menu_ost.mp3` — Main menu music
- `game_ost.mp3` — Gameplay music

### Sound effects
- `click_button.mp3`
- `hover_button.mp3`
- `game_start.mp3`
- `game_over.mp3`
- `running_sound.mp3`
- `wind_gust.mp3`
- `glass_shatter.mp3`

## Art and Assets

The project uses custom game assets for:
- Backgrounds
- Player animation
- Plate sprites
- UI icons
- Logo
- Pixel-style font

## Current Gameplay Loop

1. Start from the main menu.
2. Control Pete and catch incoming plates.
3. Build a stack and keep it balanced.
4. Respond to wind and weather changes.
5. Avoid losing the stack.
6. Restart and play again after game over.

### Audio issues
If some audio files do not play correctly on your machine, try converting them to `.wav` files and updating the file names in the code.

### Missing assets
Make sure all required files are inside the `src/assets/` folder.

## Credits

Developed as a **CS196 University Game Project**.

### Built with
- Python
- Arcade
- arcade.gui

## License

This project is for educational use unless otherwise specified.

## AI Usage
- Readme File
- Sprites and Image Assets
- Plate Balancing Logic Guidance
