from .cfg_voltage_registers import VoltageRegisterField, voltage_cell_from_raw, voltage_cell_to_raw
from .cfg_time_registers import TimeRegisterField

from .isl94203_constants import *

"""Cell Balance Group """
cell_balance_min_voltage = VoltageRegisterField(
    name="cell_balance_min_voltage",
    address=0x1C,
    bit_length=12,
    bit_position=0,
    to_raw= voltage_cell_to_raw,
    from_raw = voltage_cell_from_raw,
)

cell_balance_max_voltage = VoltageRegisterField(
    name="cell_balance_max_voltage",
    address=0x1E,
    bit_length=12,
    bit_position=0,
    to_raw= voltage_cell_to_raw,
    from_raw = voltage_cell_from_raw,
)

cell_balance_min_delta = VoltageRegisterField(
    name="cell_balance_max_delta",
    address=0x20,
    bit_length=12,
    bit_position=0,
    to_raw= voltage_cell_to_raw,
    from_raw = voltage_cell_from_raw,
)

cell_balance_max_delta = VoltageRegisterField(
    name="cell_balance_min_delta",
    address=0x22,
    bit_length=12,
    bit_position=0,
    to_raw= voltage_cell_to_raw,
    from_raw = voltage_cell_from_raw,
)

cell_balance_on_time = TimeRegisterField(
    name="cell_balance_on_time",
    address=0x24,
    bit_length=8,
    bit_position=0,
    unit_bit_length=2,
    unit_bit_position=10,
    mapping= UNIT_MAPPING,
    to_raw= lambda x: x,
    from_raw = lambda x: x,
)

cell_balance_off_time = TimeRegisterField(
    name="cell_balance_off_time",
    address=0x26,
    bit_length=8,
    bit_position=0,
    unit_bit_length=2,
    unit_bit_position=10,
    mapping= UNIT_MAPPING,
    to_raw= lambda x: x,
    from_raw = lambda x: x,
)

cell_balance_min_temp = VoltageRegisterField(
    name="cell_balance_min_temp",
    address=0x28,
    bit_length=12,
    bit_position=0,
    to_raw= voltage_cell_to_raw,
    from_raw = voltage_cell_from_raw,
)