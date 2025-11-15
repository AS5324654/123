# Snake Game

A simple Snake game implemented with [pygame](https://www.pygame.org/).

## Running the game

1. Create and activate a virtual environment (optional but recommended).
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Start the game:

   ```bash
   python snake_game.py
   ```

Use the arrow keys or WASD to control the snake. Press the space bar to pause/resume.

## Building a Windows executable

> **Note:** PyInstaller must run on Windows to generate a Windows `.exe`.

1. Install PyInstaller alongside the game's dependencies:

   ```bash
   pip install -r requirements.txt
   pip install pyinstaller
   ```

2. From the project root, execute the helper script:

   ```bash
   python tools/build_windows_exe.py
   ```

   The script clears any previous build artifacts, runs PyInstaller with the
   appropriate options, and zips the resulting executable for easy sharing.

3. After the script finishes, you will find two artifacts inside the `dist/`
   folder:

   * `SnakeGame.exe` – the standalone executable.
   * `SnakeGame_Windows.zip` – a compressed archive containing the executable.

Transfer the ZIP file to another machine and extract it to access the game.
