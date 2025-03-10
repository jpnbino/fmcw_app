from dataclasses import dataclass
from typing import Dict, Callable

from .isl94203_constants import CELL_CONFIG_MAPPING, CELL_CONFIG_INT2CODE_MAPPING, Mask

@dataclass
class CellConfigRegisterField:
    name: str
    address: int
    bit_position: int
    bit_mask: int
    from_raw: Callable[[int], int]
    to_raw: Callable[[int], int]
    unit: str = "Cells"


reg = CellConfigRegisterField(
    name="cell_config",
    address=0x48,
    bit_position=8,
    bit_mask=Mask.MASK_8BIT,
    from_raw= lambda x: CELL_CONFIG_MAPPING.get(x, x),
    to_raw= lambda x: CELL_CONFIG_INT2CODE_MAPPING.get(x, x),
)