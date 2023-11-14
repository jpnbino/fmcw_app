import serial
import time

def receive_and_log_data(serial_port, log_file_path="C:/Users/bino/Desktop/fmcw/python/log.txt"):
    # Open the serial port
    with serial.Serial(serial_port, 115200, timeout=1) as ser:
        # Open the log file in append mode
        with open(log_file_path, "a") as log_file:
            while True:
                # Check if there is data available to be read
                if ser.in_waiting > 0:
                    # Read the data from the serial port
                    data = ser.readline().decode("utf-8").strip()

                    # Add a timestamp
                    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                    data_with_timestamp = f"{timestamp}, {data}"

                    # Log the data to the file
                    log_file.write(data_with_timestamp + "\n")

                    # Parse the data
                    parsed_data = parse_data(data)

                    print("Data with timestamp:", data_with_timestamp)
                    print("Parsed data:", parsed_data)

                # Wait for 10 seconds before the next iteration
                time.sleep(10)

def parse_data(data):
    # Split the data into individual values
    values = data.split(",")

    # Example parsing - adjust based on your data format
    parsed_data = {
        "Voltage": int(values[0], 16) << 8 | int(values[1], 16),
        "Current": int(values[2], 16),
        "OtherValue": int(values[3], 16),
        # Add more fields based on your data format
    }

    return parsed_data

if __name__ == "__main__":
    serial_port = "COM25"  # Change this to the correct serial port on your system

    receive_and_log_data(serial_port)
