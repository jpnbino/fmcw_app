from .cfg_timeout_registers import TimeRegisterField
from bms.isl94203_constants import *

map = [
    ("watchdog_timer", 0x46, 11, Mask.MASK_5BIT, "s"),
    ("idle_doze_timer", 0x48, 0, Mask.MASK_4BIT, "min"),
    ("sleep_mode_timer", 0x18, 4, Mask.MASK_4BIT, "min"),
]

reg = {}
for name, address, bit_position, bit_mask, unit in map:
    reg[name] = TimeRegisterField(
        name=name,
        address=address,
        bit_mask=bit_mask,
        bit_position=bit_position,
        to_raw= lambda x: x,
        from_raw = lambda x: x,
        unit = unit
    )