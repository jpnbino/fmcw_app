import matplotlib.pyplot as plt

# Define constants
VOLTAGE_CELL_MULTIPLIER = ((1.8 * 8.0) / (4095.0 * 3.0))
MASK_12_BIT = 0x0FFF

# Function to parse and process the data
def parse_and_plot(file_path):
    timestamps = []
    voltages = []

    with open(file_path, 'r') as file:
        for line in file:
            # Split the line into individual values
            values = line.strip().split(',')

            # Extract timestamp and voltage values
            timestamp = values[0]
            voltage_bytes = values[1:3]

            # Convert voltage bytes to an integer and apply the fix
            voltage = (int(voltage_bytes[1], 16) << 8 | int(voltage_bytes[0], 16)) | MASK_12_BIT

            # Convert voltage to actual voltage using the multiplier
            voltage = voltage * VOLTAGE_CELL_MULTIPLIER

            # Append to the lists
            timestamps.append(timestamp)
            voltages.append(voltage)

    # Plot the data
    plt.plot(range(len(voltages)), voltages, label='Voltage')
    plt.xlabel('Timestamp')
    plt.ylabel('Voltage (V)')
    plt.legend()
    plt.show()

# Use the function with your data file
parse_and_plot('app/data/log.txt')
