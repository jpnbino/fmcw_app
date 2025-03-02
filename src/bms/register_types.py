from dataclasses import dataclass
from typing import Optional, Dict, Callable

from .isl94203_constants import Mask

@dataclass
class VoltageRegisterField:
    name: str
    address: int
    bit_mask: int
    bit_position: int # bit position of LSB
    to_raw: Callable[[float],int] # Function to convert GUI value to raw
    from_raw: Callable[[int],float] # Function to convert raw to GUI value
    unit: str = "V"

@dataclass
class VoltageMappedRegisterField:
    name: str
    address: int
    bit_mask: int
    bit_position: int
    mapping: Dict[int, str]
    to_raw: Callable[[str], int]
    from_raw: Callable[[int], str]

@dataclass
class TimeRegisterField:
    name: str
    address: int
    bit_position: int
    bit_mask: int
    to_raw: Callable[[int], int]
    from_raw: Callable[[int], int]
    unit_bit_position: Optional[int] = None
    unit_bit_mask: Optional[int] = None
    unit_mapping: Optional[Dict[int, str]] = None

@dataclass
class BooleanRegisterField:
    name: str
    address: int
    bit_position: int
    description: str
    bit_mask: int = Mask.MASK_1BIT
    to_raw: Callable[[bool], int] = lambda value: 1 if value else 0
    from_raw: Callable[[int], bool] = lambda raw: bool(raw)

@dataclass
class TemperatureRegisterField:
    name: str
    address: int
    bit_mask: int
    bit_position: int
    to_raw: Callable[[int], int]
    from_raw: Callable[[int], int]