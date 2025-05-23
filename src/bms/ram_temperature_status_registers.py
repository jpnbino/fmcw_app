from .register_types import TemperatureRegisterField
from .isl94203_constants import *


def temperature_from_raw(value: int) -> float:
    return value * TEMPERATURE_MULTIPLIER

def temperature_to_raw(value: float) -> int:
    return value/TEMPERATURE_MULTIPLIER

map = [
    ("internal_temperature", 0xA0, Mask.MASK_12BIT, temperature_to_raw, temperature_from_raw),
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
    