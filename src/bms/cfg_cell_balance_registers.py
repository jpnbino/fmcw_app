
from bms.cfg_current_limits_registers import unit_from_raw, unit_to_raw
from .cfg_voltage_registers import VoltageRegisterField, voltage_cell_from_raw, voltage_cell_to_raw
from .cfg_timeout_registers import TimeRegisterField, TimeUnitRegisterField

from .isl94203_constants import *


def voltage_temperature_from_raw(value: int) -> float:
    return value * TEMPERATURE_MULTIPLIER

def voltage_temperature_to_raw(value: float) -> int:
    return int(value / TEMPERATURE_MULTIPLIER)
"""Cell Balance Group """


# Voltage Definitions
v_map = [
    ("cell_balance_min_voltage", 0x1C, voltage_cell_from_raw, voltage_cell_to_raw),
    ("cell_balance_max_voltage", 0x1E, voltage_cell_from_raw, voltage_cell_to_raw),
    ("cell_balance_max_delta", 0x22, voltage_cell_from_raw, voltage_cell_to_raw),
    ("cell_balance_min_delta", 0x20, voltage_cell_from_raw, voltage_cell_to_raw),
    ("cell_balance_min_temp", 0x28, voltage_temperature_from_raw, voltage_temperature_to_raw),
    ("cell_balance_min_temp_recovery", 0x2A, voltage_temperature_from_raw, voltage_temperature_to_raw),
    ("cell_balance_max_temp", 0x2C, voltage_temperature_from_raw, voltage_temperature_to_raw),
    ("cell_balance_max_temp_recovery", 0x2E, voltage_temperature_from_raw, voltage_temperature_to_raw),
]

v_reg = {}
for name, address, from_raw, to_raw in v_map:
    v_reg[name] = VoltageRegisterField(
        name=name,
        address=address,
        bit_mask=Mask.MASK_12BIT,
        bit_position=0,
        to_raw=to_raw,
        from_raw=from_raw,
    )

# Time Definitions
t_map = [

    ("cell_balance_on_time", 0x24),
    ("cell_balance_off_time", 0x26)
]

t_reg = {}
for name, address in t_map:
    t_reg[name] = TimeRegisterField(
        name=name,
        address=address,
        bit_mask=Mask.MASK_8BIT,
        bit_position=0,
        to_raw= lambda x: x,
        from_raw = lambda x: x,
    )

    t_reg[f"{name}_unit"] = TimeUnitRegisterField(
        name=name,
        address=address,
        bit_mask=Mask.MASK_2BIT,
        bit_position=10,
        to_raw=unit_to_raw,
        from_raw=unit_from_raw,
        unit_mapping=UNIT_MAPPING,
        unit="ms"
    )