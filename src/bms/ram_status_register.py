from dataclasses import dataclass, field
from typing import Callable

@dataclass
class BooleanStatusRegisterField:
    name: str
    address: int
    bit_position: int
    description: str
    from_raw: Callable[[int], bool] = lambda raw: bool(raw)

@dataclass
class CellBalanceControlRegisterField:
    name: str
    address: int
    bit_position: int
    description: str
    to_raw: Callable[[bool], int] = lambda value: 1 if value else 0
    from_raw: Callable[[int], bool] = lambda raw: bool(raw)

status_bit_map = {
    0x80: [
        ("cut", 7, "Charge Under-Temp"),
        ("cot", 6, "Charge Over-Temp"),
        ("dut", 5, "Discharge Under-Temp"),
        ("dot", 4, "Discharge Over-Temp"),
        ("uvlo", 3, "Undervoltage Lockout"),
        ("uv", 2, "Undervoltage"),
        ("ovlo", 1, "Overvoltage Lockout"),
        ("ov", 0, "Overvoltage"),
    ],
    0x81: [
        ("eochg", 7, "End of Charge"),
        ("open", 5, "Open Wire"),
        ("cellf", 4, "Cell Fail"),
        ("dsc", 3, "Discharge Short-Circuit"),
        ("doc", 2, "Discharge Overcurrent"),
        ("coc", 1, "Charge Overcurrent"),
        ("iot", 0, "Internal Over-Temp"),
    ],
    0x82: [
        ("lvchg", 7, "Low Voltage Charge"),
        ("int_scan", 6, "Internal Scan In-Progress"),
        ("ecc_fail", 5, "EEPROM Error Correct Fail"),
        ("ecc_used", 4, "EEPROM Error Correct"),
        ("dching", 3, "Discharging"),
        ("ching", 2, "Charging"),
        ("ch_prsnt", 1, "Chrgr Present"),
        ("ld_prsnt", 0, "Load Present"),
    ],
    0x83: [
        ("in_sleep", 6, "In Sleep Mode"),
        ("in_doze", 5, "In Doze Mode"),
        ("in_idle", 4, "In Idle Mode"),
        ("cbuv", 3, "Cell Balance Undervoltage"),
        ("cbov", 2, "Cell Balance Overvoltage"),
        ("cbut", 1, "Cell Balance Under-Temp"),
        ("cbot", 0, "Cell Balance Over-Temp"),
    ],
}

status_bit_reg = {}
for address, fields in status_bit_map.items():
    for name, bit_position, description in fields:
        status_bit_reg[name] = BooleanStatusRegisterField(
            name=name,
            address=address,
            bit_position=bit_position,
            description=description,
        )

cb_bit_map = [
    ("cb8on", 7, "Cell Balance 8 On"),
    ("cb7on", 6, "Cell Balance 7 On"),
    ("cb6on", 5, "Cell Balance 6 On"),
    ("cb5on", 4, "Cell Balance 5 On"),
    ("cb4on", 3, "Cell Balance 4 On"),
    ("cb3on", 2, "Cell Balance 3 On"),
    ("cb2on", 1, "Cell Balance 2 On"),
    ("cb1on", 0, "Cell Balance 1 On"),
]

cb_bit_reg = {}
for name, bit_position, description in cb_bit_map:
    cb_bit_reg[name] = CellBalanceControlRegisterField(
        name=name,
        address=0x84,
        bit_position=bit_position,
        description=description,
    )
