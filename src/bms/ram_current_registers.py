from dataclasses import dataclass
from typing import Dict, Callable

from .isl94203_constants import CURRENT_GAIN_MAPPING, Mask

@dataclass
class CurrentGainRegisterField:
    name: str
    address: int
    bit_position: int
    bit_mask: int
    mapping: Dict[int, int]
    to_raw: Callable[[int], int]
    from_raw: Callable[[int], int]

current_gain = CurrentGainRegisterField(
    name="current_gain",
    address=0x85,
    bit_position=4,
    bit_mask=Mask.MASK_2BIT,
    mapping= CURRENT_GAIN_MAPPING,
    to_raw= lambda x: x,
    from_raw = lambda x: x,
)