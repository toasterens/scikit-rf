from enum import Enum


# _models = {
#     'default': {'nports': 2, 'unsupported': []},
#     'E8362C': {'nports': 2, 'unsupported': ['nports', 'freq_step', 'fast_sweep']},
#     'N5227B': {'nports': 4, 'unsupported': []},
# }

# Variable for ony_supported
# Add Software Version for PNA?? should be better then device
# Dont make sense to list all models

class Model(str, Enum):

    # PNA Models:
    E8361A = {'device': 'E8361A', 'nports': 0, 'unsupported': []}
    E8362B = {'device': 'E8362B', 'nports': 0, 'unsupported': []}
    N5221A = {'device': 'N5221A', 'nports': 0, 'unsupported': []}
    N5222A = {'device': 'N5222A', 'nports': 0, 'unsupported': []}
    N5224A = {'device': 'N5224A', 'nports': 0, 'unsupported': []}
    N5225A = {'device': 'N5225A', 'nports': 0, 'unsupported': []}
    N5227A = {'device': 'N5227A', 'nports': 0, 'unsupported': []}
    N5224B = {'device': 'N5224B', 'nports': 0, 'unsupported': []}
    N5222B = {'device': 'N5222B', 'nports': 0, 'unsupported': []}
    N5227B = {'device': 'N5227B', 'nports': 2, 'unsupported': []}
    N5225B = {'device': 'N5225B', 'nports': 0, 'unsupported': []}
    N5221B = {'device': 'N5221B', 'nports': 0, 'unsupported': []}
    E8356A = {'device': 'E8356A', 'nports': 0, 'unsupported': []}
    E8357A = {'device': 'E8357A', 'nports': 0, 'unsupported': []}
    E8358A = {'device': 'E8358A', 'nports': 0, 'unsupported': []}
    E8361C = {'device': 'E8361C', 'nports': 0, 'unsupported': []}
    E8362A = {'device': 'E8362A', 'nports': 0, 'unsupported': []}
    E8362C = {'device': 'E8362C', 'nports': 2, 'unsupported': ['nports', 'freq_step', 'fast_sweep']}
    E8363A = {'device': 'E8363A', 'nports': 0, 'unsupported': []}
    E8363B = {'device': 'E8363B', 'nports': 0, 'unsupported': []}
    E8363C = {'device': 'E8363C', 'nports': 0, 'unsupported': []}
    E8364A = {'device': 'E8364A', 'nports': 0, 'unsupported': []}
    E8364B = {'device': 'E8364B', 'nports': 0, 'unsupported': []}
    E8364C = {'device': 'E8364C', 'nports': 0, 'unsupported': []}
    E8801A = {'device': 'E8801A', 'nports': 0, 'unsupported': []}
    E8802A = {'device': 'E8802A', 'nports': 0, 'unsupported': []}
    E8803A = {'device': 'E8803A', 'nports': 0, 'unsupported': []}
    N3381A = {'device': 'N3381A', 'nports': 0, 'unsupported': []}
    N3382A = {'device': 'N3382A', 'nports': 0, 'unsupported': []}
    N3383A = {'device': 'N3383A', 'nports': 0, 'unsupported': []}
    N5250C = {'device': 'N5250C', 'nports': 0, 'unsupported': []}

    # PNA-L Models:
    N5230A = {'device': 'N5230A', 'nports': 0, 'unsupported': []}
    N5230C = {'device': 'N5230C', 'nports': 0, 'unsupported': []}
    N5231A = {'device': 'N5231A', 'nports': 0, 'unsupported': []}
    N5232A = {'device': 'N5232A', 'nports': 0, 'unsupported': []}
    N5234A = {'device': 'N5234A', 'nports': 0, 'unsupported': []}
    N5235A = {'device': 'N5235A', 'nports': 0, 'unsupported': []}
    N5239A = {'device': 'N5239A', 'nports': 0, 'unsupported': []}
    N5234B = {'device': 'N5234B', 'nports': 0, 'unsupported': []}
    N5235B = {'device': 'N5235B', 'nports': 0, 'unsupported': []}
    N5231B = {'device': 'N5231B', 'nports': 0, 'unsupported': []}
    N5232B = {'device': 'N5232B', 'nports': 0, 'unsupported': []}
    N5239B = {'device': 'N5239B', 'nports': 0, 'unsupported': []}

    # PNA-X Models:
    N5241A = {'device': 'N5241A', 'nports': 0, 'unsupported': []}
    N5242A = {'device': 'N5242A', 'nports': 0, 'unsupported': []}
    N5244A = {'device': 'N5244A', 'nports': 0, 'unsupported': []}
    N5245A = {'device': 'N5245A', 'nports': 0, 'unsupported': []}
    N5247A = {'device': 'N5247A', 'nports': 0, 'unsupported': []}
    N5249A = {'device': 'N5249A', 'nports': 0, 'unsupported': []}
    N5247B = {'device': 'N5247B', 'nports': 0, 'unsupported': []}
    N5245B = {'device': 'N5245B', 'nports': 0, 'unsupported': []}
    N5244B = {'device': 'N5244B', 'nports': 0, 'unsupported': []}
    N5242B = {'device': 'N5242B', 'nports': 2, 'unsupported': []}
    N5241B = {'device': 'N5241B', 'nports': 0, 'unsupported': []}
    N5249B = {'device': 'N5249B', 'nports': 0, 'unsupported': []}
    N5264A = {'device': 'N5264A', 'nports': 0, 'unsupported': []}
    N5264B = {'device': 'N5264B', 'nports': 0, 'unsupported': []}


    # unknown model
    UNKNOWN = ''


