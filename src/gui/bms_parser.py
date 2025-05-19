from datetime import datetime
import logging

from bms.cfg_voltage_registers import voltage_cell_from_raw
from bms.ram_current_registers import current_from_raw

from bms.ram_voltage_status_registers import voltage_vbatt_from_raw

def parse_bms_values(ram_values):
    """Parse raw RAM values into meaningful values."""

    try:
        RAM_BASE_ADDRESS = 0x80  # Base address for RAM values

        cell_min = voltage_cell_from_raw(ram_values[0x80 - RAM_BASE_ADDRESS] + ram_values[0x81 - RAM_BASE_ADDRESS])
        cell_max = voltage_cell_from_raw(ram_values[0x82 - RAM_BASE_ADDRESS] + ram_values[0x83 - RAM_BASE_ADDRESS])
        icurrent = current_from_raw(
            ram_values[0x84 - RAM_BASE_ADDRESS] + ram_values[0x85 - RAM_BASE_ADDRESS],
            0.005,  # Resistor value in ohms,
            1
        )

        # Parse cell voltages (first 8 values)
        cell_values = [
            voltage_cell_from_raw(ram_values[i - RAM_BASE_ADDRESS] + ram_values[i + 1 - RAM_BASE_ADDRESS])
            for i in range(0x90, 0x9F, 2)
        ]

        vbatt = voltage_vbatt_from_raw(ram_values[0xA6 - RAM_BASE_ADDRESS] + ram_values[0xA7 - RAM_BASE_ADDRESS])
        vrgo = voltage_cell_from_raw(ram_values[0xA8 - RAM_BASE_ADDRESS] + ram_values[0xA9 - RAM_BASE_ADDRESS])

        # Parse status bits (address 0x80 to 0x83)
        status_bits = ram_values[0x80 - RAM_BASE_ADDRESS:0x84 - RAM_BASE_ADDRESS]

        # Map status bits to meaningful fields
        status_bits_parsed = {
            "Status1_80h": {
                "OV": (status_bits[0] & 0x01),
                "OVLO": (status_bits[0] & 0x02) >> 1,
                "UV": (status_bits[0] & 0x04) >> 2,
                "UVLO": (status_bits[0] & 0x08) >> 3,
                "DOT": (status_bits[0] & 0x10) >> 4,
                "DUT": (status_bits[0] & 0x20) >> 5,
                "COT": (status_bits[0] & 0x40) >> 6,
                "CUT": (status_bits[0] & 0x80) >> 7,
            },
            "Status2_81h": {
                "IOT": (status_bits[1] & 0x01),
                "COC": (status_bits[1] & 0x02) >> 1,
                "DOC": (status_bits[1] & 0x04) >> 2,
                "DSC": (status_bits[1] & 0x08) >> 3,
                "CELLF": (status_bits[1] & 0x10) >> 4,
                "OPEN": (status_bits[1] & 0x20) >> 5,
                "bit6": (status_bits[1] & 0x40) >> 6,
                "EOCHG": (status_bits[1] & 0x80) >> 7,
            },
            "Status3_82h": {
                "LD_PRSNT": (status_bits[2] & 0x01),
                "CH_PRSNT": (status_bits[2] & 0x02) >> 1,
                "CHING": (status_bits[2] & 0x04) >> 2,
                "DCHING": (status_bits[2] & 0x08) >> 3,
                "ECC_USED": (status_bits[2] & 0x10) >> 4,
                "ECC_FAIL": (status_bits[2] & 0x20) >> 5,
                "INT_SCAN": (status_bits[2] & 0x40) >> 6,
                "LVCHG": (status_bits[2] & 0x80) >> 7,
            },
            "Status4_83h": {
                "CBOT": (status_bits[3] & 0x01),
                "CBUT": (status_bits[3] & 0x02) >> 1,
                "CBOV": (status_bits[3] & 0x04) >> 2,
                "CBUV": (status_bits[3] & 0x08) >> 3,
                "IN_IDLE": (status_bits[3] & 0x10) >> 4,
                "IN_DOZE": (status_bits[3] & 0x20) >> 5,
                "IN_SLEEP": (status_bits[3] & 0x40) >> 6,
                "bit7": (status_bits[3] & 0x80) >> 7,
            },
        }

        # Construct the parsed data as a dictionary
        parsed_data = {
            "timestamp": datetime.now().isoformat(),
            "vbatt": vbatt,
            "vrgo": vrgo,
            "cell_min": cell_min,
            "cell_max": cell_max,
            "cell_voltages": cell_values,
            "current": icurrent,
            "status_bits": status_bits_parsed,
        }

        return parsed_data

    except Exception as e:
        logging.error(f"Failed to parse RAM values: {e}")
        return {}