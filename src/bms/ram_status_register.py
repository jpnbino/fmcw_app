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

"""0x80: Status Register"""
CUT_FIELD = BooleanStatusRegisterField(
    name="CUT",
    address=0x80,
    bit_position=7,
    description="Charge Under-Temp",
)

COT_FIELD = BooleanStatusRegisterField(
    name="COT",
    address=0x80,
    bit_position=6,
    description="Charge Over-Temp",
)

DUT_FIELD = BooleanStatusRegisterField(
    name="DUT",
    address=0x80,
    bit_position=5,
    description="Discharge Under-Temp",
)

DOT_FIELD = BooleanStatusRegisterField(
    name="DOT",
    address=0x80,
    bit_position=4,
    description="Discharge Over-Temp",
)

UVLO_FIELD = BooleanStatusRegisterField(
    name="UVLO",
    address=0x80,
    bit_position=3,
    description="Undervoltage Lockout",
)

UV_FIELD = BooleanStatusRegisterField(
    name="UV",
    address=0x80,
    bit_position=2,
    description="Undervoltage",
)

OVLO_FIELD = BooleanStatusRegisterField(
    name="OVLO",
    address=0x80,
    bit_position=1,
    description="Overvoltage Lockout",
)

OV_FIELD = BooleanStatusRegisterField(
    name="OV",
    address=0x80,
    bit_position=0,
    description="Overvoltage",
)

"""0x81: Fault Register"""
EOCHG_FIELD = BooleanStatusRegisterField(
    name="EOCHG",
    address=0x81,
    bit_position=7,
    description="End of Charge",
)

OPEN_FIELD = BooleanStatusRegisterField(
    name="OPEN",
    address=0x81,
    bit_position=5,
    description="Open Wire",
)

CELLF_FIELD = BooleanStatusRegisterField(
    name="CELLF",
    address=0x81,
    bit_position=4,
    description="Cell Fail",
)

DSC_FIELD = BooleanStatusRegisterField(
    name="DSC",
    address=0x81,
    bit_position=3,
    description="Discharge Short-Circuit",
)

DOC_FIELD = BooleanStatusRegisterField(
    name="DOC",
    address=0x81,
    bit_position=2,
    description="Discharge Overcurrent",
)

COC_FIELD = BooleanStatusRegisterField(
    name="COC",
    address=0x81,
    bit_position=1,
    description="Charge Overcurrent",
)

IOT_FIELD = BooleanStatusRegisterField(
    name="IOT",
    address=0x81,
    bit_position=0,
    description="Internal Over-Temp",
)

LVCHG_FIELD = BooleanStatusRegisterField(
    name="LVCHG",
    address=0x82,
    bit_position=7,
    description="Low Voltage Charge",
)

INT_SCAN_FIELD = BooleanStatusRegisterField(
    name="INT_SCAN",
    address=0x82,
    bit_position=6,
    description="Internal Scan In-Progress",
)

ECC_FAIL_FIELD = BooleanStatusRegisterField(
    name="ECC_FAIL",
    address=0x82,
    bit_position=5,
    description="EEPROM Error Correct Fail",
)

ECC_USED_FIELD = BooleanStatusRegisterField(
    name="ECC_USED",
    address=0x82,
    bit_position=4,
    description="EEPROM Error Correct",
)

DCHING_FIELD = BooleanStatusRegisterField(
    name="DCHING",
    address=0x82,
    bit_position=3,
    description="Discharging",
)

CHING_FIELD = BooleanStatusRegisterField(
    name="CHING",
    address=0x82,
    bit_position=2,
    description="Charging",
)

CH_PRSNT_FIELD = BooleanStatusRegisterField(
    name="CH_PRSNT",
    address=0x82,
    bit_position=1,
    description="Chrgr Present",
)

LD_PRSNT_FIELD = BooleanStatusRegisterField(
    name="LD_PRSNT",
    address=0x82,
    bit_position=0,
    description="Load Present",
)

IN_SLEEP_FIELD = BooleanStatusRegisterField(
    name="IN_SLEEP",
    address=0x83,
    bit_position=6,
    description="In Sleep Mode",
)

IN_DOZE_FIELD = BooleanStatusRegisterField(
    name="IN_DOZE",
    address=0x83,
    bit_position=5,
    description="In Doze Mode",
)

IN_IDLE_FIELD = BooleanStatusRegisterField(
    name="IN_IDLE",
    address=0x83,
    bit_position=4,
    description="In Idle Mode",
)

CBUV_FIELD = BooleanStatusRegisterField(
    name="CBUV",
    address=0x83,
    bit_position=3,
    description="Cell Balance Undervoltage",
)

CBOV_FIELD = BooleanStatusRegisterField(
    name="CBOV",
    address=0x83,
    bit_position=2,
    description="Cell Balance Overvoltage",
)

CBUT_FIELD = BooleanStatusRegisterField(
    name="CBUT",
    address=0x83,
    bit_position=1,
    description="Cell Balance Under-Temp",
)

CBOT_FIELD = BooleanStatusRegisterField(
    name="CBOT",
    address=0x83,
    bit_position=0,
    description="Cell Balance Over-Temp",
)

CB8ON_FIELD = CellBalanceControlRegisterField(
    name="CB8ON",
    address=0x84,
    bit_position=7,
    description="Cell Balance 8 On",
)

CB7ON_FIELD = CellBalanceControlRegisterField(
    name="CB7ON",
    address=0x84,
    bit_position=6,
    description="Cell Balance 7 On",
)

CB6ON_FIELD = CellBalanceControlRegisterField(
    name="CB6ON",
    address=0x84,
    bit_position=5,
    description="Cell Balance 6 On",
)

CB5ON_FIELD = CellBalanceControlRegisterField(
    name="CB5ON",
    address=0x84,
    bit_position=4,
    description="Cell Balance 5 On",
)

CB4ON_FIELD = CellBalanceControlRegisterField(
    name="CB4ON",
    address=0x84,
    bit_position=3,
    description="Cell Balance 4 On",
)

CB3ON_FIELD = CellBalanceControlRegisterField(
    name="CB3ON",
    address=0x84,
    bit_position=2,
    description="Cell Balance 3 On",
)

CB2ON_FIELD = CellBalanceControlRegisterField(
    name="CB2ON",
    address=0x84,
    bit_position=1,
    description="Cell Balance 2 On",
)

CB1ON_FIELD = CellBalanceControlRegisterField(
    name="CB1ON",
    address=0x84,
    bit_position=0,
    description="Cell Balance 1 On",
)