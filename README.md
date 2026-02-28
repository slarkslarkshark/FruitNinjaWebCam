# FruitNinjaWebCam

Turn your room into an arcade arena and slice flying fruit with real hand movements.
**FruitNinjaWebCam** combines fast reflex gameplay with **live webcam tracking**, making every swipe feel physical and satisfying.

![Main Menu Screenshot](https://res.cloudinary.com/dztnoej5d/image/upload/v1772270145/main_menu_dtqlr0.png)

Your **index finger** becomes the blade:
- Slice fruits in mid-air to score points
- Avoid bombs to stay alive
- Reach the target score to win
- Pick your challenge: Easy, Medium, Hard

![Gameplay Screenshot](https://res.cloudinary.com/dztnoej5d/image/upload/v1772270204/game_rpp6ix.png)

## Why It Feels Different

This is not a standard mouse-controlled game.
Your body is the controller. Every slash is captured in real time, creating a fresh motion-gaming twist on a classic arcade idea.

## Gameplay Highlights

- Real-time hand tracking via webcam
- Dynamic fruit and bomb spawning
- Smooth slicing trail and visual effects
- Multiple difficulty levels
- Victory and game-over screens with quick replay flow

## Start Game

### Option 1: .exe for Windows

- Download .exe file
- Run game

### Option 2: Using `uv`

```bash
uv sync
uv run python main.py
```

### Option 3: Using `requirements.txt` + venv

```bash
pip install -r requirements.txt
python main.py
```

## Build own .exe (Windows)

Use the installer module from a Windows machine:

```powershell
python installer\windows_setup.py --build --onefile
```


