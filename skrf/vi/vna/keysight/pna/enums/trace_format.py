from enum                 import Enum


class TraceFormat(str, Enum):

    magnitude_dB = 'MLOG'
    phase_deg    = 'PHAS'
    smith_chart  = 'SMIT'
    polar        = 'POL'
    vswr         = 'SWR'
    unwrapped_phase_deg = 'UPH'
    magnitude    = 'MLIN'
    inverse_smith_chart = 'ISM'
    real         = 'REAL'
    imaginary    = 'IMAG'
    group_delay  = 'GDEL'
