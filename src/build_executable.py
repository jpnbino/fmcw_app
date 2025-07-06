import subprocess
import os
import sys

def build_executable():
    # Change to the script directory to ensure relative paths work correctly
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Add the src directory to Python path for module discovery
    src_path = os.path.abspath('.')
    
    command = [
        "pyinstaller",
        "--noconfirm",
        "--windowed",
        "--onefile",  # Creates a single executable file
        "--name", "FMCW_Radar",
        "--paths", src_path,  # Add src directory to Python path
        "main.py",
        "--icon", "../images/icons/icon_circle.png",
        "--add-data", "../qt/fmcw.ui;qt/",
        "--add-data", "../qt/resources/stylesheet.qss;qt/resources/",
        "--add-data", "../qt/resources/images/;qt/resources/images/",
        "--add-data", "../qt/fonts/;qt/fonts/",
        "--add-data", "../config/;config/",
        "--add-data", "../images/;images/",
        "--add-data", "../extras/isl94203/;extras/isl94203/",
        # Add all source modules explicitly
        "--add-data", "./config/;config/",
        "--add-data", "./bms/;bms/",
        "--add-data", "./gui/;gui/",
        "--add-data", "./logger/;logger/",
        "--add-data", "./serialbsp/;serialbsp/",
        "--add-data", "./simdevice/;simdevice/",
        "--hidden-import", "config.app_config",
        "--hidden-import", "serial",
        "--hidden-import", "yaml",
        "--hidden-import", "PySide6.QtUiTools",
        "--hidden-import", "logging.config",
        "--hidden-import", "bms.isl94203_driver",
        "--hidden-import", "gui.tabbms",
        "--hidden-import", "gui.tabmain",
        "--hidden-import", "gui.global_log_manager",
        "--hidden-import", "gui.global_status_bar_manager",
        "--hidden-import", "gui.userlog",
        "--hidden-import", "logger.logging_config",
        "--hidden-import", "serialbsp.serial_manager",
        "--hidden-import", "serialbsp.protocol_fmcw",
        "--collect-submodules", "serialbsp",
        "--collect-submodules", "bms",
        "--collect-submodules", "gui",
        "--collect-submodules", "logger",
        "--collect-submodules", "config",
        # Windows-specific
        "--console",  # Temporarily enable console for debugging
    ]

    print("Running PyInstaller with the following command:")
    print(" ".join(command))
    print()

    try:
        subprocess.run(command, check=True)
        print("\nPyInstaller build finished!")
        print("The executable should be in the 'dist' folder.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\nError during PyInstaller build: {e}")
        return False
    except FileNotFoundError:
        print("\nError: PyInstaller command not found. Make sure it's installed and in your PATH.")
        return False

def build_executable_alternative():
    """Alternative build method that creates a directory-based distribution"""
    # Change to the script directory to ensure relative paths work correctly
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Add the src directory to Python path for module discovery
    src_path = os.path.abspath('.')
    
    command = [
        "pyinstaller",
        "--noconfirm",
        "--windowed",
        # Remove --onefile for better compatibility
        "--name", "FMCW_Radar",
        "--paths", src_path,  # Add src directory to Python path
        "--distpath", "dist",
        "--workpath", "build",
        "main.py",
        "--icon", "../images/icons/icon_circle.png",
        "--add-data", "../qt/fmcw.ui;qt/",
        "--add-data", "../qt/resources/stylesheet.qss;qt/resources/",
        "--add-data", "../qt/resources/images/;qt/resources/images/",
        "--add-data", "../qt/fonts/;qt/fonts/",
        "--add-data", "../config/;config/",
        "--add-data", "../images/;images/",
        "--add-data", "../extras/isl94203/;extras/isl94203/",
        # Include source modules as data
        "--add-data", "./config/;./config/",
        "--add-data", "./bms/;./bms/",
        "--add-data", "./gui/;./gui/",
        "--add-data", "./logger/;./logger/",
        "--add-data", "./serialbsp/;./serialbsp/",
        "--add-data", "./simdevice/;./simdevice/",
        # Specific hidden imports
        "--hidden-import", "config.app_config",
        "--hidden-import", "serial",
        "--hidden-import", "yaml",
        "--hidden-import", "PySide6.QtUiTools",
        "--hidden-import", "logging.config",
        "--hidden-import", "bms.isl94203_driver",
        "--hidden-import", "gui.tabbms",
        "--hidden-import", "gui.tabmain", 
        "--hidden-import", "gui.global_log_manager",
        "--hidden-import", "gui.global_status_bar_manager",
        "--hidden-import", "gui.userlog",
        "--hidden-import", "logger.logging_config",
        "--hidden-import", "serialbsp.serial_manager",
        "--hidden-import", "serialbsp.protocol_fmcw",
        "--collect-all", "config",
        "--collect-all", "bms",
        "--collect-all", "gui", 
        "--collect-all", "logger",
        "--collect-all", "serialbsp",
        "--collect-all", "simdevice",
        # Enable console for debugging
        "--console",
    ]

    print("Running PyInstaller (Alternative Method) with the following command:")
    print(" ".join(command))
    print()

    try:
        subprocess.run(command, check=True)
        print("\nPyInstaller build (Alternative Method) finished!")
        print("The executable should be in the 'dist/FMCW_Radar' folder.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\nError during PyInstaller build: {e}")
        return False
    except FileNotFoundError:
        print("\nError: PyInstaller command not found. Make sure it's installed and in your PATH.")
        return False

if __name__ == "__main__":
    print("Choose build method:")
    print("1. Single file executable (--onefile)")
    print("2. Directory distribution (recommended for troubleshooting)")
    choice = input("Enter choice (1 or 2), or press Enter for default (1): ").strip()
    
    if choice == "2":
        print("Using alternative method (directory distribution)...")
        success = build_executable_alternative()
    else:
        print("Using standard method (single file)...")
        success = build_executable()
        
        if not success:
            print("\nSingle file build failed. Trying alternative method...")
            success = build_executable_alternative()
    
    if success:
        print("\nBuild completed successfully!")
    else:
        print("\nBuild failed. Check the error messages above.")
    # Uncomment the following line to use the alternative build method
    # build_executable_alternative()