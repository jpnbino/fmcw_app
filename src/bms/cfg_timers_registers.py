from .cfg_timeout_registers import TimeRegisterField
from bms.isl94203_constants import *

map = [
    ("watchdog_timer", 0x46, 11, Mask.MASK_5BIT, None, None, "s"),
    ("idle_doze_timer", 0x48, 0, Mask.MASK_4BIT, Mask.MASK_2BIT, 10, "min"),
    ("sleep_mode_timer", 0x18, 4, Mask.MASK_4BIT, None, None, "min"),
]

reg = {}
for name, address, bit_position, bit_mask, unit_bit_mask, unit_bit_position, unit in map:
    reg[name] = TimeRegisterField(
        name=name,
        address=address,
        bit_mask=bit_mask,
        bit_position=bit_position,
        unit_bit_mask=unit_bit_mask,
        unit_bit_position=unit_bit_position,
        to_raw= lambda x: x,
        from_raw = lambda x: x,
        unit = unit
    )