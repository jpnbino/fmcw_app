from dataclasses import dataclass
from typing import Dict, Callable

from .isl94203_constants import CELL_CONFIG_MAPPING, CELL_CONFIG_INT2CODE_MAPPING, Mask

@dataclass
class CellConfigRegisterField:
    name: str
    address: int
    bit_position: int
    bit_mask: int
    mapping: Dict[int, int]
    int_to_code_mapping: Dict[int, int]
    to_raw: Callable[[int], int]


reg = CellConfigRegisterField(
    name="cell_config",
    address=0x48,
    bit_position=8,
    bit_mask=Mask.MASK_8BIT,
    mapping= CELL_CONFIG_MAPPING,
    int_to_code_mapping= CELL_CONFIG_INT2CODE_MAPPING,
    to_raw= lambda x: x,
)