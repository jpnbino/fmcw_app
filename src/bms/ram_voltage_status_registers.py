from dataclasses import dataclass
from typing import Optional, Dict, Callable
from bms.isl94203_constants import *
from bms.cfg_voltage_registers import VoltageRegisterField, voltage_cell_from_raw, voltage_cell_to_raw

MAX_NUM_CELLS = 8

cell_voltage_min = VoltageRegisterField(
    name="cell_min_voltage",
    address=0x8A,
    bit_length=12,
    bit_position=0,
    to_raw=voltage_cell_to_raw,
    from_raw=voltage_cell_from_raw,
)

cell_voltage_max = VoltageRegisterField(
    name="cell_max_voltage",
    address=0x8C,
    bit_length=12,
    bit_position=0,
    to_raw=voltage_cell_to_raw,
    from_raw=voltage_cell_from_raw,
)

cell_voltages = [
    VoltageRegisterField(
        name=f"cell{i+1}_voltage",
        address=0x90 + i * 0x02,
        bit_length=12,
        bit_position=0,
        to_raw=voltage_cell_to_raw,
        from_raw=voltage_cell_from_raw,
    )
    for i in range(MAX_NUM_CELLS)
]




def voltage_vbatt_from_raw(value: int) -> float:
    return (value * VOLTAGE_PACK_MULTIPLIER)

def voltage_vbatt_to_raw(value: float) -> int:
    return int((value / VOLTAGE_PACK_MULTIPLIER))

'''Pack Voltage'''
vbatt_voltage = VoltageRegisterField(
    name="vbatt_voltage",
    address=0xA6,
    bit_length=12,
    bit_position=0,
    to_raw=voltage_cell_to_raw,
    from_raw=voltage_cell_from_raw,
)

vrgon_voltage = VoltageRegisterField(
    name="vrgon_voltage",
    address=0xA8,
    bit_length=12,
    bit_position=0,
    to_raw=voltage_cell_to_raw,
    from_raw=voltage_cell_from_raw,
)