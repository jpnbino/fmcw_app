from .cfg_voltage_registers import VoltageRegisterField, voltage_cell_from_raw, voltage_cell_to_raw
from .cfg_timeout_registers import TimeRegisterField

from .isl94203_constants import *

"""Cell Balance Group """

# Voltage Definitions
v_map = [
    ("cell_balance_min_voltage", 0x1C),
    ("cell_balance_max_voltage", 0x1E),
    ("cell_balance_max_delta", 0x20),
    ("cell_balance_min_delta", 0x22),
    ("cell_balance_min_temp", 0x28),
    ("cell_balance_min_temp_recovery", 0x2A),
    ("cell_balance_max_temp", 0x2C),
    ("cell_balance_max_temp_recovery", 0x2E),
]


v_reg = {}
for name, address in v_map:
    v_reg[name] = VoltageRegisterField(
        name=name,
        address=address,
        bit_mask=Mask.MASK_12BIT,
        bit_position=0,
        to_raw= voltage_cell_to_raw,
        from_raw = voltage_cell_from_raw,
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
        unit_bit_mask=Mask.MASK_2BIT,
        unit_bit_position=10,
        unit_mapping= UNIT_MAPPING,
        to_raw= lambda x: x,
        from_raw = lambda x: x,
    )
