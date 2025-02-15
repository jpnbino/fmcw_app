
    
import logging


def convert_to_hex(value, multiplier):
    """
    Converts a given value to hexadecimal representation.

    Args:
        value (float or str): The value to be converted.

    Returns:
        int: The hexadecimal representation of the value.

    Raises:
        None
    config_type:

    """
    try:
        return int(float(value) / multiplier)
    except ValueError:
        logging.error(f"Error converting {value} to hex.")
        raise

def convert_time_to_hex(time, scaling_factor):
    """
    Convert a given time value to a hexadecimal value by right-shifting it by a scaling factor.

    Args:
        time (int or str): The time value to be converted.
        scaling_factor (int): The factor by which to right-shift the time value.

    Returns:
        int: The hexadecimal representation of the time value.

    Raises:
        ValueError: If the time value cannot be converted to an integer.
    """
    try:
        return int(time) >> scaling_factor
    except ValueError as e:
        logging.error(f"Error converting {time} to hex: {e}")
    raise