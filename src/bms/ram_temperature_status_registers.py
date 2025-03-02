from .register_types import TemperatureRegisterField
from .isl94203_constants import *

def temperature_from_raw(value: int) -> float:
    return value

def temperature_to_raw(value: float) -> int:
    return value


internal_temperature = TemperatureRegisterField(
    name="internal_temperature",
    address=0xA0,
    bit_mask=Mask.MASK_8BIT,
    bit_position=0,
    to_raw= lambda x: x,
    from_raw = lambda x: x,
)

external_temperature1 = TemperatureRegisterField(
    name="external_temperature1",
    address=0xA2,
    bit_mask=Mask.MASK_8BIT,
    bit_position=0,
    to_raw= lambda x: x,
    from_raw = lambda x: x,
)

external_temperature2 = TemperatureRegisterField(
    name="external_temperature2",
    address=0xA4,
    bit_mask=Mask.MASK_8BIT,
    bit_position=0,
    to_raw= lambda x: x,
    from_raw = lambda x: x,
)