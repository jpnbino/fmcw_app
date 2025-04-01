from .register_types import TemperatureRegisterField
from .isl94203_constants import *

TEMP_VOLT2CELCIUS_TGAIN1 = ((1000/0.92635))

TEMP_VOLT2CELCIUS_TGAIN0 = ((1000/1.8527))

def internal_temp_to_celsius(value: int) -> float:
    voltage = temperature_from_raw(value)
    return (voltage * TEMP_VOLT2CELCIUS_TGAIN0) - 273.15

def temperature_from_raw(value: int) -> float:
    return value * TEMPERATURE_MULTIPLIER

def temperature_to_raw(value: float) -> int:
    return value/TEMPERATURE_MULTIPLIER

map = [
    ("internal_temperature", 0xA0, Mask.MASK_12BIT, temperature_to_raw, internal_temp_to_celsius),
    ("external_temperature1", 0xA2, Mask.MASK_12BIT, temperature_to_raw, temperature_from_raw),
    ("external_temperature2", 0xA4, Mask.MASK_12BIT, temperature_to_raw,temperature_from_raw),
]

reg = {}
for name, address, bit_mask, to_raw, from_raw in map:
    reg[name] = TemperatureRegisterField(
        name=name,
        address=address,
        bit_mask=bit_mask,
        bit_position=0,
        to_raw=to_raw,
        from_raw=from_raw,
    )
    