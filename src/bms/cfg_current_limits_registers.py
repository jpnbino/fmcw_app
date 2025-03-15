from .register_types import TimeRegisterField
from .register_types import VoltageMappedRegisterField

from .isl94203_constants import DOC_MAPPING, COC_MAPPING, DSC_MAPPING, UNIT_MAPPING, Mask

def reverse_mapping(mapping: dict) -> dict:
    return {v: k for k, v in mapping.items()}

def voltage_to_raw(voltage: str, mapping: dict) -> int:
    reversed_mapping = reverse_mapping(mapping)
    return reversed_mapping[voltage]

def voltage_from_raw(raw: int, mapping: dict) -> str:
    return mapping[raw]

voltage_map = [
    ("discharge_oc_current",0x16, DOC_MAPPING),
    ("charge_oc_current",0x18,COC_MAPPING),
    ("discharge_sc_current",0x1A, DSC_MAPPING),
]

time_map = [
    ("discharge_oc_delay", 0x16),
    ("charge_oc_delay", 0x18),
    ("discharge_sc_delay", 0x1A),
]

pulse_map = [
    ("charge_detect_pulse_width", 0x00),
    ("discharge_detect_pulse_width", 0x02),
]

reg = {}

for name, address, mapping in voltage_map:
    reg[name] = VoltageMappedRegisterField(
        name=name,
        address=address,
        bit_mask=Mask.MASK_3BIT,
        bit_position=12,
        mapping=mapping,
        to_raw=voltage_to_raw,
        from_raw=voltage_from_raw,
    )

for name, address in time_map:
    reg[name] = TimeRegisterField(
        name=name,
        address=address,
        bit_mask=Mask.MASK_10BIT,
        bit_position=0,
        to_raw=lambda x: x,
        from_raw=lambda x: x,
        unit_bit_position=10,
        unit_bit_mask=Mask.MASK_2BIT,
        unit_mapping=UNIT_MAPPING,
    )

def pulse_width_to_raw(value: int) -> int:
    return int(value)

def pulse_width_from_raw(value: int) -> int:
    return int(value)

for name, address in pulse_map:
    reg[name] = TimeRegisterField(
        name=name,
        address=address,
        bit_mask=Mask.MASK_4BIT,
        bit_position=0,
        to_raw=pulse_width_to_raw,
        from_raw=pulse_width_from_raw,
        unit = "ms",
    )