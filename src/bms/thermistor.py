import os
import sys
import logging

'''
This script is used to parse a CSV file containing NTC thermistor data and calculate the
temperature based on the resistance of the thermistor.
It uses linear interpolation to find the temperature corresponding to a given resistance value.
'''

# Constants for the NTC circuit
# These values are specific to the hardware configuration and should be adjusted accordingly.
VREG = 2.5  # Reference voltage of the NTC circuit. Values in Volts
R1 = 22000  # Resistor connected between the NTC and the TEMPO pin. Values in Ohms
Rp = 10000  # Parallel resistor to the NTC. Values in Ohms

if getattr(sys, 'frozen', False):  # Check if running as a bundled executable
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.getcwd()


CONFIG_DIR = os.path.join(BASE_DIR, '..', 'config')
NTC_FILE = os.path.join(CONFIG_DIR, 'ntc_temp_resistor_table.csv')
CSV_DELIMITER = ';'
CSV_HEADER = '"T[°C]"'

logging.basicConfig(level=logging.INFO)

_ntc_data_cache: list[tuple[float, float]] = None

def load_ntc_data(file_path: str) -> list[tuple[float, float]]:
    """Loads and prepares the NTC data."""
    global _ntc_data_cache
    if _ntc_data_cache is None:  # Load the data only if it hasn't been loaded yet
        ntc_data = parse_ntc_data(file_path)
        if not ntc_data:
            raise ValueError("No NTC data loaded. Please check the data file.")
        ntc_data.sort(key=lambda x: x[1])
        _ntc_data_cache = calculate_parallel_resistance(ntc_data, Rp)
    return _ntc_data_cache

def parse_ntc_data(filename: str) -> list[tuple[float, float]]:
    """
    Parses the NTC resistance-temperature data from the given file.

    Args:
        filename (str): The name of the file containing the NTC data.

    Returns:
        list of tuples: A list where each tuple is (temperature, resistance).
                      Returns an empty list if there's an error during parsing.
    """
    ntc_data = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith(CSV_HEADER):
                    parts = line.split(CSV_DELIMITER)
                    try:
                        temp = float(parts[0].strip('"'))
                        resistance = float(parts[1].strip('"'))
                        ntc_data.append((temp, resistance))
                    except (ValueError, IndexError):
                        logging.warning(f"Skipping line: {line} - Invalid format")
    except FileNotFoundError:
        logging.error(f"File '{filename}' not found.")
    return ntc_data

def get_temperature(resistance: float, ntc_table: list[tuple[float, float]]) -> float | None:
    """
    Finds the temperature corresponding to a given resistance using linear interpolation.

    Args:
        resistance (float): The resistance value.
        ntc_table (list of tuples): A sorted list where each tuple is (temperature, resistance).

    Returns:
        float: The interpolated temperature in degrees Celsius, or None if the
               resistance is outside the table range.

    Example:
        ntc_table = [(25.0, 10000.0), (50.0, 5000.0)]
        get_temperature(7500.0, ntc_table) -> 37.5
    """
    if resistance >= ntc_table[-1][1]:
        return ntc_table[-1][0]
    if resistance <= ntc_table[0][1]:
        return ntc_table[0][0]
    for i in range(len(ntc_table) - 1):
        t_low, r_low = ntc_table[i]
        t_high, r_high = ntc_table[i + 1]
        if r_low <= resistance <= r_high:
            slope = (t_high - t_low) / (r_high - r_low)
            return t_low + (resistance - r_low) * slope
    return None

def calculate_parallel_resistance(ntc_table: list[tuple[float, float]], parallel_resistor: float) -> list[tuple[float, float]]:
    """
    Calculates the equivalent resistance of each NTC resistance in parallel with a given resistor.

    Args:
        ntc_table (list of tuples): A list where each tuple is (temperature, resistance).
        parallel_resistor (float): The resistance value of the parallel resistor.

    Returns:
        list of tuples: A new list where each tuple is (temperature, equivalent_resistance).
    """
    parallel_ntc_data: list[tuple[float, float]] = []
    for temp, resistance in ntc_table:
        try:
            equivalent_resistance = 1 / (1 / resistance + 1 / parallel_resistor)
            parallel_ntc_data.append((temp, equivalent_resistance))
        except ZeroDivisionError:
            logging.warning(f"Skipping calculation for temperature {temp} due to zero resistance.")
            continue
    return parallel_ntc_data

def calculate_resistance(measured_voltage: float) -> float:
    """Calculates the parallel resistance using the voltage divider formula."""
    if measured_voltage >= VREG:
        raise ValueError("Measured voltage cannot be greater than or equal to VREG.")
    return (R1 * measured_voltage) / (VREG - measured_voltage)

def estimate_temperature(measured_voltage: float) -> float:      
    """Estimates the temperature based on the measured voltage."""
    global ntc_data
    if 'ntc_data' not in globals():
        ntc_data = load_ntc_data(NTC_FILE)
    r_parallel = calculate_resistance(measured_voltage)
    return get_temperature(r_parallel, ntc_data)

def main():
    try:
        measured_voltage = 0.463
        temperature = estimate_temperature(measured_voltage)
        logging.info(f"Measured voltage: {measured_voltage:.3f} V")
        logging.info(f"Estimated temperature: {temperature:.2f} °C")
    except ValueError as e:
        logging.error(f"Error: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()


