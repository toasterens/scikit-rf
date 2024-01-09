from enum import Enum


class TriggerSource(str, Enum):

    EXTERNAL = "EXT"
    IMMEDIATE = "IMM"
    MANUAL = "MAN"