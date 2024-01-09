from enum import Enum


class SweepType(str, Enum):
    
    LINEAR      = "LIN"
    LOG         = "LOG"
    POWER       = "POW"
    CW          = "CW"
    SEGMENT     = "SEGM"
    PHASE       = "PHAS"