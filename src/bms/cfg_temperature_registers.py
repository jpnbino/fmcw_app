from dataclasses import dataclass
from .isl94203_constants import TEMPERATURE_MULTIPLIER, Mask

def voltage_temp_from_raw(value: int) -> int:
    return value*TEMPERATURE_MULTIPLIER

def voltage_temp_to_raw(value: float) -> int:
    return int(value/TEMPERATURE_MULTIPLIER)

@dataclass
class TemperatureRegisterField:
    name: str
    address: int
    bit_mask: int
    bit_position: int
    to_raw: int
    from_raw: int
    unit: str = "mV"

map = [
    ("Charge OT Voltage", 0x30, Mask.MASK_12BIT),
    ("Charge OT Recovery", 0x32, Mask.MASK_12BIT),
    ("Charge UT Voltage", 0x34, Mask.MASK_12BIT),
    ("Charge UT Recovery", 0x36, Mask.MASK_12BIT),
    ("Discharge OV Voltage", 0x38, Mask.MASK_12BIT),
    ("Discharge OV Recovery", 0x3A, Mask.MASK_12BIT),
    ("Discharge UT Voltage", 0x3C, Mask.MASK_12BIT),
    ("Discharge UT Recovery", 0x3E, Mask.MASK_12BIT),
    ("Internal OV Voltage", 0x40, Mask.MASK_12BIT),
    ("Internal OV Recovery", 0x42, Mask.MASK_12BIT),
]

reg = {}
for name, address, bit_mask in map:
    reg[name] = TemperatureRegisterField(
        name=name,
        address=address,
        bit_mask=bit_mask,
        bit_position=0,
        to_raw=voltage_temp_to_raw,
        from_raw=voltage_temp_from_raw,
        
    )