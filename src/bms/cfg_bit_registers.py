
from .register_types import BooleanRegisterField


map = {
    0x4A: [
        ("cfpsd", 7, "Cell Fail PSD"),
        ("xt2m", 5, "XT2 Monitor Mode"),
        ("tgain", 4, "External Temp Gain"),
        ("pcfete", 2, "Precharge FET Enable"),
        ("dowd", 1, "Disable Open-Wire Scan"),
        ("owpsd", 0, "Open-Wire PSD"),
    ],
    0x4B: [
        ("cbdd", 7, "Cell Balance During Discharge"),
        ("cbdc", 6, "Cell Balance During Charge"),
        ("dfoduv", 5, "DFET On During UV"),
        ("cfodov", 4, "CFET On During OV"),
        ("uvlopd", 3, "UVLO Power Down"),
        ("cb_eoc", 0, "Cell Balance During EOC"),
    ],
}

reg = {}
for address, fields in map.items():
    for name, bit_position, description in fields:
        reg[name] = BooleanRegisterField(
            name=name,
            address=address,
            bit_position=bit_position,
            description=description,
        )