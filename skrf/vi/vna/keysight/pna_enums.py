from enum import Enum

#region Trace
class TraceHold(Enum):
    OFF     = 'OFF'
    MINIMUM = 'MIN'
    MAXIMUM = 'MAX'


class TopologyType(Enum):
    BALANCED = "BAL"
    """1 port balanced device (2 ports)"""
    BBALANCED = "BBAL"
    """Balanced - Balanced device (4 ports)"""
    BALSENDED = "BALS"
    """Balanced-Single-ended device (3 ports)"""
    SBALANCED  = "SBAL"
    """Single-ended -Balanced device (3 ports)"""
    SSBALANCED = "SSB"
    """Single-ended - Single-ended - Balanced device (4 ports)"""
    BSSENDED = "BSS"
    """Balanced - Single-ended - Single-ended device (4 ports)"""
    CUST = "CUST"
    """Define custom device type for systems with greater than 4 ports"""

#endregion


# Channel


#region Display
class WindowLayout(Enum):
    TILE    = "TILE"
    """tiles existing windows"""
    CASCADE = "CASC"
    """overlaps existing windows""" 
    OVERLAY = "OVERl"
    """all traces placed in 1 window"""
    STACK   = "STAC"
    """2 windows""" 
    SPLIT   = "SPL"
    """3 windows"""
    QUAD    = "QUAD"
    """4 windows"""
    MEASURE = "MEAS"
    """1 measurement per window"""
    CHANNEL = "CHAN"
    """1 channel per window"""
    LTOR    = "LTOR"
    """Arrange existing windows as a single row of side-by-side windows."""


class SheetLayout(Enum):
    WINDOW  = "WIND"
    CHANnel = "CHAN"
    TRACe   = "TRAC"
    ONE     = "ONE"


class WindowMax(Enum):
    MAX  = "MAX"
    NORM = "NORM"


class DisplayTable(Enum):
    OFF         = "OFF"
    MARKER      = "MARK"
    LIMIT       = "LIM"
    SEGMENT     = "SEGM"
    RLIMIT      = "RLIM"
    DISTORTION  = "DIST"
#endregion


# Setup


#region Meas
class MeasConvertion(Enum):
    OFF         = "OFF"
    ZREFLECTION = "ZREF"
    ZTRANSMIT   = "ZTR"
    ZTSHUNT     = "ZTSH"
    YREFLECTION = "YREF"
    YTRANSMIT   = "YTR"
    YTSHUNT     = "YTS"
    INVERSION   = "INV"
    CONJUGATION = "CONJ"
#endregion


#region Format
class TraceFormat(Enum):
    LOGMAG              = "MLOG"
    LINMag              = "MLIN"
    PHASE               = "PHAS"
    DELAY               = "GDEL"
    SMITH               = "SMIT"
    POLAR               = "POL"
    SWR                 = "SWR"
    REAL                = "REAL"
    IMAG                = "IMAG"
    UPHASE              = "UPH"
    PPHASE              = "PPH"
    INVSMITH            = "SADM"
    COMPLEX             = "COMP"
    KELVIN              = "KELV"
    FAHRENHEIT          = "FAHR"
    CELSIUS             = "CELS"
#endregion


#region Scale
class ScaleSpacing(Enum):
    LINEAR       = "LIN"
    LOGARITHMIC  = "LOG"


class ScaleCoupling(Enum):
    OFF     = 'OFF'
    WINDOW  = 'WIND'
    ALL     = 'ALL'


class ScaleDelayDisUnits(Enum):
    METER = "MET"
    FEET = "FEET"
    INCH = "INCH"


class ScaleDelayMedia(Enum):
    COAX        = "COAX"
    WAVEGUIDE   = "WAVE"
#endregion


#region Math
class MathFunctions(Enum):
    NORMAL      = "NORM"
    ADD         = "ADD"
    SUBSTRACT   = "SUBT"
    MULTIPLY    = "MULT"
    DIVIDE      = "DIV"
#endregion


#region Avg Bw
class AveragingType(Enum):
    POINT = "POIN"
    SWEEP = "SWE"


class IfType(Enum):
    STANDARD = "STAN"
    GAUSSIAN = "GAUS"
#endregion


# Cal
    

# Marker


# Search
    

# Power
    

#region Sweep
class SweepType(Enum):
    LINEAR      = "LIN"
    LOG         = "LOG"
    POWER       = "POW"
    CW          = "CW"
    SEGMENT     = "SEGM"
    PHASE       = "PHAS"

class SweepMode(Enum):
    HOLD        = "HOLD"
    CONTINUOUS  = "CONT"
    GROUPS      = "GRO"
    SINGLE      = "SING"
#endregion


#region Trigger
class TriggerSource(Enum):
    EXTERNAL    = "EXT"
    IMMEDIATE   = "IMM"
    MANUAL      = "MAN"


class TriggerScope(Enum):
    ALL     = "ALL"
    CURRENT = "CURR"
    ACTIVE  = "ACT"


class TriggerMode(Enum):
    CHANNEL = "CHAN"
    SWEEP   = "SWE"
    POINT   = "POIN"
    TRACE   = "TRAC"


class TriggerSeqType(Enum):
    EDGE    = "EDGE"
    LEVEL   = "LEV"


class TriggerSeqSlope(Enum):
    POSIIVE = "POS"
    NEGATIVE = "NEG"


class TriggeReadyPol(Enum):
    LOW = "LOW"
    HIGH = "HIGH"
#endregion


# Device Settings Enum
class Models(Enum):
    DEFAULT = {"device": "default", "nports": 2, "unsupported": []}
    E8362C  =  {"device": "E8362C", "nports": 2, "unsupported": ["nports", "freq_step", "fast_sweep"]}
    N5227B  = {"device": "N5227B", "nports": 4, "unsupported": []}
    N5244B  = {"device": "N5244B", "nports": 4, "unsupported": []}
    N5247B  = {"device": "N5247B", "nports": 4, "unsupported": []}

#endregion
