import subprocess
import os

def build_executable():
    command = [
        "pyinstaller",
        "--windowed",
        "--name","Fmcw Radar",
        "main.py",
        "--icon","../images/icons/icon_circle.png",
        "--add-data", "../qt/;qt/",
        "--add-data", "../qt/resources;qt/resources",
        "--add-data", "../qt/fonts;qt/fonts",
        "--add-data", "../config;config",
        "--add-data", "../images;images",
        "--add-data", "../../docs/isl94203/datasheet;datasheet",
        "--hidden-import", "config",
        "--hidden-import", "serial",
        "--hidden-import", "serialbsp",
        "--hidden-import", "bms",
        "--hidden-import", "logger",
        "--hidden-import", "PySide6.QtCore",
        "--hidden-import", "PySide6.QtGui",
        "--hidden-import", "PySide6.QtWidgets",
        "--hidden-import", "yaml",
    ]

    print("Running PyInstaller with the following command:")
    print(" ".join(command))
    print()

    try:
        subprocess.run(command, check=True)
        print("\nPyInstaller build finished!")
        print("The executable should be in the 'dist' folder.")
    except subprocess.CalledProcessError as e:
        print(f"\nError during PyInstaller build: {e}")
    except FileNotFoundError:
        print("\nError: PyInstaller command not found. Make sure it's installed and in your PATH.")

if __name__ == "__main__":
    build_executable()