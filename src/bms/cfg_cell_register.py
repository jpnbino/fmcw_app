from dataclasses import dataclass
from typing import Dict, Callable

from .isl94203_constants import CELL_CONFIG_MAPPING, CELL_CONFIG_INT2CODE_MAPPING

@dataclass
class CellConfigRegisterField:
    name: str
    address: int
    bit_position: int
    bit_length: int
    mapping: Dict[int, int]
    int_to_code_mapping: Dict[int, int]
    to_raw: Callable[[int], int]


cell_config = CellConfigRegisterField(
    name="cell_config",
    address=0x00,
    bit_position=0,
    bit_length=8,
    mapping= CELL_CONFIG_MAPPING,
    int_to_code_mapping= CELL_CONFIG_INT2CODE_MAPPING,
    to_raw= lambda x: x,
)