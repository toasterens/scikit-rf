from enum import Enum


class SweepMode(str, Enum):
    
    HOLD        = "HOLD"
    CONTINUOUS  = "CONT"
    GROUPS      = "GRO"
    SINGLE      = "SING"