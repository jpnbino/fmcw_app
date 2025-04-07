import os
import sys

def get_resource_path(relative_path):
    """
    Get the absolute path to a resource, whether running as a script or a PyInstaller bundle.
    """
    if getattr(sys, 'frozen', False):  # Check if running as a PyInstaller bundle
        base_path = sys._MEIPASS  # Temporary directory for PyInstaller
    else:
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")) # Script directory
    return os.path.join(base_path, relative_path)

# Basic configurations
APP_NAME = "FMCW Application"
WINDOW_TITLE = "FMCW Radar Control"
UI_FILE_PATH = get_resource_path("qt/fmcw.ui")
ICON_PATH = get_resource_path("images/icons/icon_circle.png")