from dataclasses import dataclass
from bms.isl94203_constants import *
from bms.cfg_voltage_registers import VoltageRegisterField, voltage_cell_from_raw, voltage_cell_to_raw

MAX_NUM_CELLS = 8

def voltage_vbatt_from_raw(value: int) -> float:
    return (value * VOLTAGE_PACK_MULTIPLIER)

def voltage_vbatt_to_raw(value: float) -> int:
    return int((value / VOLTAGE_PACK_MULTIPLIER))

def voltage_vrgo_from_raw(value: int) -> float:
    return (value * VOLTAGE_VRGO_MULTIPLIER)

def voltage_vrgo_to_raw(value: float) -> int:
    return int((value / VOLTAGE_VRGO_MULTIPLIER))

map = [
    ("vcell_min", 0x8A, 0, Mask.MASK_12BIT, voltage_cell_to_raw, voltage_cell_from_raw),
    ("vcell_max", 0x8C, 0, Mask.MASK_12BIT, voltage_cell_to_raw, voltage_cell_from_raw),
    ("vcell1", 0x90, 0, Mask.MASK_12BIT, voltage_cell_to_raw, voltage_cell_from_raw),
    ("vcell2", 0x92, 0, Mask.MASK_12BIT, voltage_cell_to_raw, voltage_cell_from_raw),
    ("vcell3", 0x94, 0, Mask.MASK_12BIT, voltage_cell_to_raw, voltage_cell_from_raw),
    ("vcell4", 0x96, 0, Mask.MASK_12BIT, voltage_cell_to_raw, voltage_cell_from_raw),
    ("vcell5", 0x98, 0, Mask.MASK_12BIT, voltage_cell_to_raw, voltage_cell_from_raw),
    ("vcell6", 0x9A, 0, Mask.MASK_12BIT, voltage_cell_to_raw, voltage_cell_from_raw),
    ("vcell7", 0x9C, 0, Mask.MASK_12BIT, voltage_cell_to_raw, voltage_cell_from_raw),
    ("vcell8", 0x9E, 0, Mask.MASK_12BIT, voltage_cell_to_raw, voltage_cell_from_raw),
    ("vbatt" , 0xA6, 0, Mask.MASK_12BIT, voltage_vbatt_to_raw, voltage_vbatt_from_raw),
    ("vrgo"  , 0xA8, 0, Mask.MASK_12BIT, voltage_vrgo_to_raw, voltage_vrgo_from_raw),
]
    
reg = {}
for name, address, bit_position, bit_mask, to_raw, from_raw in map:
    reg[name] = VoltageRegisterField(
        name=name,
        address=address,
        bit_mask=bit_mask,
        bit_position=bit_position,
        to_raw=  to_raw,
        from_raw = from_raw ,
    )