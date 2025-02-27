from .register_types import BooleanRegisterField

"""0x4A: Control Register"""
CFPSD_FIELD = BooleanRegisterField(
    name="CFPSD",
    address=0x4A,
    bit_position=7,
    description="Cell Fail PSD",
)

XT2M_FIELD = BooleanRegisterField(
    name="XT2M",
    address=0x4A,
    bit_position=5,
    description="XT2 Monitor Mode",
)

TGAIN_FIELD = BooleanRegisterField(
    name="TGAIN",
    address=0x4A,
    bit_position=4,
    description="External Temp Gain",
)

PCFETE_FIELD = BooleanRegisterField(
    name="PCFETE",
    address=0x4A,
    bit_position=2,
    description="Precharge FET Enable",
)

DOWD_FIELD = BooleanRegisterField(
    name="DOWD",
    address=0x4A,
    bit_position=1,
    description="Disable Open-Wire Scan",
)

OWPSD_FIELD = BooleanRegisterField(
    name="OWPSD",
    address=0x4A,
    bit_position=0,
    description="Open-Wire PSD",
)

"""0x4B: Control Register"""
CBDD_FIELD = BooleanRegisterField(
    name="CBDD",
    address=0x4B,
    bit_position=7,
    description="Cell Balance During Discharge",
)

CBDC_FIELD = BooleanRegisterField(
    name="CBDC",
    address=0x4B,
    bit_position=6,
    description="Cell Balance During Charge",
)

DFODUV_FIELD = BooleanRegisterField(
    name="DFODUV",
    address=0x4B,
    bit_position=5,
    description="DFET On During UV",
)

CFODOV_FIELD = BooleanRegisterField(
    name="CFODOV",
    address=0x4B,
    bit_position=4,
    description="CFET On During OV",
)

UVLOPD_FIELD = BooleanRegisterField(
    name="UVLOPD",
    address=0x4B,
    bit_position=3,
    description="UVLO Power Down",
)

CB_EOC_FIELD = BooleanRegisterField(
    name="CB_EOC",
    address=0x4B,
    bit_position=0,
    description="Cell Balance During EOC",
)