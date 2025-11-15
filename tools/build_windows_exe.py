#!/usr/bin/env python3
"""Helper script to package the snake game into a Windows executable."""
from __future__ import annotations

import platform
import shutil
import subprocess
import sys
from pathlib import Path
import zipfile

PROJECT_ROOT = Path(__file__).resolve().parent.parent
GAME_FILE = PROJECT_ROOT / "snake_game.py"
DIST_DIR = PROJECT_ROOT / "dist"
BUILD_DIR = PROJECT_ROOT / "build"
EXECUTABLE_NAME = "SnakeGame.exe"
ZIP_NAME = "SnakeGame_Windows.zip"


def run_pyinstaller() -> Path:
    if not GAME_FILE.exists():
        raise FileNotFoundError(f"Cannot find {GAME_FILE.relative_to(PROJECT_ROOT)}")

    pyinstaller_cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--clean",
        "--onefile",
        "--windowed",
        f"--name={EXECUTABLE_NAME[:-4]}",
        str(GAME_FILE.name),
    ]

    print("Running PyInstaller...")
    subprocess.run(pyinstaller_cmd, cwd=PROJECT_ROOT, check=True)

    exe_path = DIST_DIR / EXECUTABLE_NAME
    if not exe_path.exists():
        # PyInstaller names the executable without the .exe when running on non-Windows systems.
        fallback = DIST_DIR / EXECUTABLE_NAME.replace(".exe", "")
        if fallback.exists():
            fallback.rename(exe_path)
        else:
            raise FileNotFoundError(
                "PyInstaller did not produce the expected executable. "
                "Check the PyInstaller output for details."
            )

    return exe_path


def compress_executable(exe_path: Path) -> Path:
    zip_path = DIST_DIR / ZIP_NAME
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.write(exe_path, exe_path.name)
    return zip_path


def main() -> None:
    if platform.system() != "Windows":
        print(
            "Warning: PyInstaller can only build Windows executables when run on Windows."
        )

    for directory in (DIST_DIR, BUILD_DIR):
        if directory.exists():
            print(f"Removing existing {directory.name} directory...")
            shutil.rmtree(directory)

    exe_path = run_pyinstaller()
    zip_path = compress_executable(exe_path)

    print("\nBuild complete!")
    print(f"Executable available at: {exe_path}")
    print(f"ZIP archive available at: {zip_path}")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as exc:
        print("PyInstaller failed. Please review the error output above.")
        sys.exit(exc.returncode)
    except Exception as exc:  # pragma: no cover - best effort error reporting
        print(f"Error: {exc}")
        sys.exit(1)
