from dataclasses import dataclass
from typing import Dict, Callable, Optional

from .isl94203_constants import CURRENT_CELL_MULTIPLIER, CURRENT_GAIN_MAPPING, Mask

def current_to_raw(value: int, resistor: float, gain: int) -> int:
    return (value * gain * resistor) / (CURRENT_CELL_MULTIPLIER )

def current_from_raw(value: int, resistor: float, gain: int) -> float:
    return value * CURRENT_CELL_MULTIPLIER / ( gain * resistor)

@dataclass
class CurrentGainRegisterField:
    name: str
    address: int
    bit_position: int
    bit_mask: int
    mapping: Optional[Dict[int, int]]
    to_raw: Callable[[int], int]
    from_raw: Callable[[int], int]
    unit: str = "x"

map = [
    ("gain", 0x85, 4, Mask.MASK_2BIT, CURRENT_GAIN_MAPPING, None, None, None),
    ("i", 0x8E, 0, Mask.MASK_12BIT, None,current_to_raw, current_from_raw, "A"),
]

reg = {}
for name, address, bit_position, bit_mask, mapping ,to_raw, from_raw, unit in map:
    reg[name] = CurrentGainRegisterField(
        name=name,
        address=address,
        bit_mask=bit_mask,
        bit_position=bit_position,
        mapping=mapping,
        to_raw=to_raw,
        from_raw=from_raw,
        unit=unit,
    )

