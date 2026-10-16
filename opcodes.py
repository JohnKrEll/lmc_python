from enum import Enum


class OpCodes(Enum):
    def __new__(cls, *values):
        obj = object.__new__(cls)
        obj._value_ = values[0]
        obj.all_values = values
        for v in values[1:]:
            cls._value2member_map_[v] = obj
        return obj

    @staticmethod
    def eval_opcode(opcode_name: str) -> int:
        try:
            val = OpCodes[opcode_name]
            if val.value > 10:
                return val.value // 100
            return val.value
        except ValueError:
            raise ValueError(f"Invalid Opcode parsed: {opcode_name}")

    HLT = 0
    ADD = 1
    SUB = 2
    STA = 3
    LDA = 5
    BRA = 6
    BRZ = 7
    BRP = 8
    INP = 901
    OUT = 902
    OTC = 922
