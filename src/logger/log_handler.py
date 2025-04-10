import os
import sys
import json
from datetime import datetime


class LogHandler:
    def __init__(self, log_type, log_dir=None):
        """
        Initialize the LogHandler.

        Args:
            log_type (str): The type of log ('ram' or 'parsed').
            log_dir (str): The directory where logs will be stored. Defaults to the current directory.
        """
        self.log_file_path = None
        self.log_type = log_type
        self.log_dir = log_dir or self.get_default_log_dir()
        self.data = [] # Store all log entries in memory

    def get_default_log_dir(self):
        """Determine the default log directory, compatible with executables."""
        if getattr(sys, 'frozen', False):  # Check if running as an executable
            base_dir = sys._MEIPASS  # Temporary directory used by PyInstaller
        else:
            base_dir = os.getcwd()  # Development environment
        return os.path.join(base_dir, "logs")
    
    def start_log(self):
        """Create a new log file with a timestamp in the specified directory."""
        if self.log_file_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f'bms_log_{timestamp}.json'
            os.makedirs(self.log_dir, exist_ok=True)
            self.log_file_path = os.path.join(self.log_dir, file_name)
            print(f"Log file created: {self.log_file_path}")  # Debugging log

    def write_log_entry(self, raw_data, parsed_data):
        """
        Write a single log entry to the in-memory data list.

        Args:
            raw_data (list[int]): The raw 44-byte payload as a list of integers.
            parsed_data (dict): The parsed values (e.g., cell voltages, status bits).
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "raw_data": raw_data,
            **parsed_data  # Merge parsed data into the entry
        }
        self.data.append(entry)

    def save_to_file(self):
        """Save all logged data to the JSON file."""
        with open(self.log_file_path, mode='w') as file:
            json.dump({"data": self.data}, file, indent=2)

    def stop_log(self):
        """Stop logging and save all data to the file."""
        if self.log_file_path is None:
            raise ValueError("Log file path is not set. Did you call start_log before stop_log?")
        print(f"Saving log to: {self.log_file_path}")  # Debugging log
        self.save_to_file()
        self.log_file_path = None
        self.data = []  # Clear in-memory data