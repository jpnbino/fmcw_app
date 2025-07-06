# Configuration

This folder contains configuration files for the BMS.

## NTC table file

the `ntc_temp_resistor_table.csv` file contains the temperature and resistance values for the NTC thermistor used in the BMS board.

The program will read the values from this file and use them to calculate the temperature of the thermistor.

If the thermistor is changed in the hardware design. the table has to be updated to the new part added.

## Default Configuration

The `default_config.json` file contains the default configuration for the BMS. The GUI loads the values directly from this file dinamically.

These default values are designed to match the project configuration.