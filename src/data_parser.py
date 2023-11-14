import csv
from datetime import datetime

# Constants
VOLTAGE_CELL_MULTIPLIER = (1.8 * 8.0) / (4095.0 * 3.0)
EEPROM_BASE_ADDRESS = 0x00
USER_EEPROM_BASE_ADDRESS = 0x50
RAM_BASE_ADDRESS = 0x80
MASK_12BIT = 0x0fff

def print_memory_layout(eeprom, user_eeprom, ram):
    print("EEPROM\nAddr | Data")
    print_memory_section(eeprom, EEPROM_BASE_ADDRESS)

    print("\nUser EEPROM\nAddr | Data")
    print_memory_section(user_eeprom, USER_EEPROM_BASE_ADDRESS)

    print("\nRAM\nAddr | Data")
    print_memory_section(ram, RAM_BASE_ADDRESS)

def print_memory_section(memory, base_address):
    for i in range(0, len(memory), 4):
        address = i + base_address
        data_chunk = memory[i:i+4]
        data_str = ' '.join([f'{value:02X}' for value in data_chunk])
        print(f"  {address:02X} - {data_str}")

def print_cell_voltage (ram):

   # Define the number of cells
    num_cells = 8

    # Loop through each cell and print its voltage
    for i in range(num_cells):
        # Calculate the base address for each cell
        base_address = 0x90 + 2 * i - RAM_BASE_ADDRESS

        # Extract raw voltage value from ram and print it
        raw_voltage = ((ram[base_address + 1] << 8) | ram[base_address])
        raw_voltage &= MASK_12BIT
        
        # Calculate and print the cell voltage
        cell_voltage = raw_voltage * VOLTAGE_CELL_MULTIPLIER
        print(f"Cell {i + 1} Voltage: {cell_voltage}")

# Function to parse a line of data
def parse_line(line):
    # Split the line into individual components
    components = line.strip().split(',')
    
    # Extract timestamp
    timestamp_str = components[0].strip()
    timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
    
    # Extract other data values
    data_values = [int(value, 16) for value in components[1:]]
    
    # Divide the data into eeprom, user_eeprom, and ram
    eeprom = data_values[:0x4C]
    user_eeprom = data_values[0x4C:0x4C + 8]
    ram = data_values[0x4C + 8 :]
    
    return timestamp, eeprom, user_eeprom, ram

# Open the text file and parse each line
file_path = 'values.txt'  # Replace with the actual path to your file
parsed_data = []

with open(file_path, 'r') as file:
    for line in file:
        timestamp, eeprom, user_eeprom, ram = parse_line(line)

        print_memory_layout(eeprom, user_eeprom, ram)
        print_cell_voltage(ram)

        parsed_data.append((timestamp, eeprom, user_eeprom, ram))

# Now you have the parsed data in the 'parsed_data' list
# You can access the timestamp, eeprom, user_eeprom, and ram for each line as needed
for timestamp, eeprom, user_eeprom, ram in parsed_data:

    eeprom_hex = [hex(value) for value in eeprom]
    user_eeprom_hex = [hex(value) for value in user_eeprom]
    ram_hex = [hex(value) for value in ram]
    print(f'Timestamp: {timestamp}, EEPROM: {eeprom_hex}, User EEPROM: {user_eeprom_hex}, RAM: {ram_hex}')
