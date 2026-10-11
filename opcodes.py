from enum import Enum


class OpCodes(Enum):
    HALT = 0
    ADD = 1
    SUB = 2
    STA = 3
    LDA = 5
    BRA = 6
    BRZ = 7
    BRP = 8
    IN = 901
    OUT = 902
