import csv
from datetime import datetime

class LogHandler:
    def __init__(self, log_type):
        self.log_file_path = None
        self.log_type = log_type  # Use to differentiate between log types

    def start_log(self):
        # Create a new log file with a timestamp
        if self.log_file_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            if self.log_type == 'ram':
                self.log_file_path = f'bms_ram_log_{timestamp}.csv'
            elif self.log_type == 'parsed':
                self.log_file_path = f'bms_parsed_log_{timestamp}.csv'

    def write_ram_log(self, ram_values):
        # Write the RAM values to the CSV log
        formatted_values = [f'{value:02X}' for value in ram_values]
        with open(self.log_file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            # Write the header if the file is empty
            if file.tell() == 0:
                writer.writerow(['timestamp'] + [f'{0x80 + i:02X}h' for i in range(len(ram_values))])
            writer.writerow([datetime.now().isoformat()] + formatted_values)

    def write_parsed_log(self, parsed_values):
        # Write parsed values (e.g., Cell1, Cell2, etc.) to the CSV log
        with open(self.log_file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            # Write the header if the file is empty
            if file.tell() == 0:
                headers = ['timestamp', 'Cell1', 'Cell2', 'Cell3', 'CellMin', 'CellMax', 'Icurrent', 'status bit0', 'status bit1', '...']
                writer.writerow(headers)
            writer.writerow([datetime.now().isoformat()] + parsed_values)

    def stop_log(self):
        self.log_file_path = None  # Reset the log file when logging stops
