from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional, Sequence, Union

import re
import sys
from enum import Enum
import itertools

import numpy as np

import skrf
from skrf.vi import vna
from skrf.vi.validators import (
    BooleanValidator,
    DelimitedStrValidator,
    EnumValidator,
    FloatValidator,
    FreqValidator,
    IntValidator,
)
from skrf.vi.vna import VNA, ValuesFormat

# TODO Enum reihenfolge Sortieren?
#region Enums
# Channel

# Display
class DisplayArrange(Enum):
    TILE    = "TILE"    # tiles existing windows
    CASCADE = "CASC"    # overlaps existing windows
    OVERLAY = "OVERl"   # all traces placed in 1 window
    STACK   = "STAC"    # 2 windows
    SPLIT   = "SPL"     # 3 windows
    QUAD    = "QUAD"    # 4 windows
    MEASURE = "MEAS"    # 1 measurement per window
    CHANNEL = "CHAN"    # 1 channel per window
    LTOR    = "LTOR"    # Arrange existing windows as a single row of side-by-side windows.


# Setup

# Meas

# Format
class TraceFormat(Enum):
    LOGMAG              = 'MLOG'
    LinMag              = 'MLIN'
    PHASE               = 'PHAS'
    DELAY               = 'GDEL'
    SMITH               = 'SMIT'
    POLAR               = 'POL'
    SWR                 = 'SWR'
    REAL                = 'REAL'
    IMAG                = 'IMAG'
    UPHASE              = 'UPH'
    PPHASE              = 'PPH'
    INVSMITH            = 'SADM'
    COMPLEX             = 'COMP'
    KELVIN              = 'KELV'
    FAHRENHEIT          = 'FAHR'
    CELSIUS             = 'CELS'


class AveragingMode(Enum):
    POINT = "POIN"
    SWEEP = "SWE"


class SweepMode(Enum):
    HOLD        = "HOLD"
    CONTINUOUS  = "CONT"
    GROUPS      = "GRO"
    SINGLE      = "SING"


class SweepType(Enum):
    LINEAR      = "LIN"
    LOG         = "LOG"
    POWER       = "POW"
    CW          = "CW"
    SEGMENT     = "SEGM"
    PHASE       = "PHAS"



class TriggerSource(Enum):
    EXTERNAL = "EXT"
    IMMEDIATE = "IMM"
    MANUAL = "MAN"


class TriggerScope(Enum):
    ALL = "ALL"
    CURRENT = "CURR"
    ACTIVE = "ACT"


class TriggerMode(Enum):
    CHANNEL = "CHAN"
    SWEEP = "SWE"
    POINT = "POIN"
    TRACE = "TRAC"


class TriggerSeqType(Enum):
    EDGE = "EDGE"
    LEVEL = "LEV"


class TriggerSeqSlope(Enum):
    POSIIVE = "POS"
    NEGATIVE = "NEG"


class TriggeReadyPol(Enum):
    LOW = "LOW"
    HIGH = "HIGH"


class Models(Enum):
    DEFAULT = {"device": "default", "nports": 2, "unsupported": []}
    E8362C  =  {"device": "E8362C", "nports": 2, "unsupported": ["nports", "freq_step", "fast_sweep"]}
    N5227B  = {"device": "N5227B", "nports": 4, "unsupported": []}
    N5244B  = {"device": "N5244B", "nports": 4, "unsupported": []}
    N5247B  = {"device": "N5247B", "nports": 4, "unsupported": []}

#endregion


class PNA(VNA):

    # TODO Chante models to ENUM
    _models = {
        "default": {"nports": 2, "unsupported": []},
        "E8362C": {"nports": 2, "unsupported": ["nports", "freq_step", "fast_sweep"]},
        "N5227B": {"nports": 4, "unsupported": []},
    }

    
    class Channel(VNA.Channel):
        def __init__(self, parent, cnum: int, cname: str):
            super().__init__(parent, cnum, cname)

            # TODO add copy channel
            # TODO make default_msmnt changeable 
            # TODO Lösen wie bei R&S
            if cnum != 1:
                default_msmnt = f"CH{self.cnum}_S11_1"
                self.create_measurement(default_msmnt, "S11")

        def _on_delete(self):
            self.write(f"SYST:CHAN:DEL {self.cnum}")

        #region Trace
        # Trace Setup
        
        # TODO Select Trace
            
        # TODO Measure Trace
            
        # TODO Trace Title
            
        # TODO Add Trace --> Change Name
        def create_measurement(self, name: str, parameter: str) -> None:
            self.write(f"CALC{self.cnum}:PAR:EXT '{name}',{parameter}")
            # Not all instruments support DISP:WIND:TRAC:NEXT
            traces = self.query("DISP:WIND:CAT?").replace('"', "")
            traces = [int(tr) for tr in traces.split(",")] if traces != "EMPTY" else [0]
            next_tr = traces[-1] + 1
            self.write(f"DISP:WIND:TRAC{next_tr}:FEED '{name}'")
            # TODO New Trace
            # TODO New Trace + Channel
            # TODO New Trace + Window
            # TODO New Trace + Window + Channel
            # TODO New Traces
        
        # TODO Delete Trace --> Change Name???
        def delete_measurement(self, name: str) -> None:
            self.write(f"CALC{self.cnum}:PAR:DEL '{name}'")

        # TODO Trace Manager --> Return Trace Window, Channel, Format,...
            
        # TODO Trace Hold

        #endregion
            

        #region Channel
        # Channel Setup
        
        # TODO Select Channel
            
        # TODO Add Channel
            # TODO New Trace + Channel
            # TODO New Trace + Channel + Window

        # TODO Copy Channel
            # TODO Copy to active Window
            # TODO Copy to new Window
            # TODO Copy Channel

        # Delete Channel

        #endregion


        #region Display
        # Window Setup
        
        # TODO Select Window
            
        # TODO Window Title
            
        # TODO Add Window
            # TODO New Window
            # TODO New Trace + Window
            # TODO New Trace + Channel + Window
        
        # TODO Delete Window
            
        # TODO Move Window
            
        # TODO Window Layout --> nicht vom Channel abhängig --> nach unten verschieben
        win_layout = VNA.command(
        get_cmd=None,
        set_cmd="DISPARR <arg>",
        doc="""Window arrangement""",
        validator=EnumValidator(DisplayArrange),
        )



        # Sheet Setup
        # TODO Select Sheet
            
        # TODO Sheet Title
            
        # TODO Add Sheet
            # TODO New Sheet
            # TODO New Trace + Sheet
            # TODO New Trace + Channel + Sheet

        # TODO Sheet Layout
            # TODO 1 Sheet
            # TODO 1 Sheet per trace
            # TODO 1 Channel per sheet
            # TODO 1 Window per sheet

        # Display Setup
        # TODO Trace Maximize
        
        # TODO Window Max
            
        # TODO Show Table --> None, Marker, Limit, Ripple, Segment
        
        # TODO Costomize Disply --> Allgemeine Settings
            
        # TODO Touchscreen on/off
            
        # TODO Display Update

        #endregion


        #region Setup
        # Main
        # TODO Sweep Setup --> Fenster mit mehreren Freq. Einstellungen --> gleiches fenster wie im unterpunt sweep

        # TODO Meas Class
            
        # TODO Quick Start ???
            
        # TODO Device Expert
        
        # System Setup
            
        # TODO Sound
            
        # TODO Remote Interface
            
        # TODO LAN Status
            
        # TODO Code Emulation
        
        # Internal Hardware
        
        # TODO RF Path Config
            
        # TODO IF Path Config
            
        # TODO Mechanical Devices
            
        # TODO Interface Control
            
        # TODO Reference
            
        # TODO LF Extension
        
        # External Hardware

        # TODO External Device
            
        # TODO Power Meter Setup
            
        # TODO Multiport
            
        # TODO Milimeter Config

        #endregion


        #region Meas
        # S-Parameter
            # TODO Create S-Parameter Meas
        
        # Balanced
        # TODO Topologie Window
        
        # Receivers
            
        # Waves
            
        # Auxilary
            
        # Meas Setup
        
        # TODO Conversions
        
        # TODO Correction
            
        # TODO Trace Hold
            
        # TODO Equition Editor
            
        # TODO Memory
            
        # TODO Time Domain
            
        # TODO Pulse Setup

        #endregion


        #region Format
        # Format 1
        # TODO Format
            
        # TODO Group Delay Aperature
            
        # Format 2
        # TODO Temperatur


        #endregion
            

        #region Scale
        # Main
        # TODO Autoscale
        
        # TODO Autoscale All
            
        # TODO Scale
            
        # TODO Reference Level
            
        # TODO Reference Position
            
        # TODO Y-Axis Spacing
            
        # TODO Scale Coupling
        
        # Electrical Delay
        # TODO Delay Time
            
        # TODO Delay Distance
            
        # TODO Distance Units
            
        # TODO Velocity Factor
            
        # TODO Media
            
        # TODO Waveguide Cut off
        
        # Constants
        # TODO System Z0
            
        # TODO Phase offset
            
        # TODO Mag offset
            
        # TODO Mag Slope


        #endregion
            

        #region Math
        # Memory
        # TODO Data --> Memory
            
        # TODO Normalize
            
        # TODO Data math
            
        # TODO Display Data Traces
            
        # TODO 8510 Mode
            
        # TODO Interpolate
        
        # Analysis
        # TODO Conversions
            
        # TODO Equition Editor
            
        # TODO Statictics
            
        # TODO AM Distortion
            
        # TODO Trace Deviations
            
        # TODO Uncertainity Analysis
            
        # TODO Limits
            
        # TODO Limit Table

        # Time Domain
        
        # TODO Transform
            
        # TODO Start Time
            
        # TODO Stop Time
            
        # TODO Center Time
            
        # TODO Span Time
            
        # TODO TD Mode
            
        # TODO TD Toolbar
            
        # TODO Time Domain Setup
        
        # Time Gating
        # TODO Gating
            
        # TODO Gate Start
            
        # TODO Gate Stop
            
        # TODO Gate Center
            
        # TODO Gate Span
            
        # TODO Gate Type
            
        # TODO Gate Shape
            
        # TODO Gating Setup

        #endregion


        #region Avg BW
        # Main
        # TODO Averaging

        # TODO Averaging Restart --> Entspricht clear_averaging?
        def clear_averaging(self) -> None:
            self.write(f"SENS{self.cnum}:AVER:CLE")

        # TODO Average Type

        # TODO Stan / Gaus Settings
        if_bandwidth = VNA.command(
            get_cmd="SENS<self:cnum>:BWID?",
            set_cmd="SENS<self:cnum>:BWID <arg>",
            doc="""The IF bandwidth [Hz]""",
            validator=FreqValidator(),
        )
        
        # TODO LF Auto BW
        
        # Smoothing
        # TODO Smoothing
            
        # TODO Smooth Percent
            
        # TODO Smooth Points
            
        # Delay Aperature
        # TODO Aperature Percent
            
        # TODO Aperature Points
            
        # TODO Aperature Freq

        #endregion
            

        #region Cal
        
        # TODO Name und function Anpassen
        @property
        def calibration(self) -> skrf.Calibration:
            raise NotImplementedError()
            # orig_query_fmt = self.parent.query_format
            # self.parent.query_format = ValuesFormat.BINARY_64

            # eterm_re = re.compile(r"(\w+)\((\d),(\d)\)")
            # cset_terms = self.query(f"SENS{self.cnum}:CORR:CSET:ETER:CAT?")
            # terms = re.findall(eterm_re, cset_terms)

            # if len(terms) == 3:
            #     cal = skrf.OnePort
            # elif len(terms) == 12:
            #     # cal = skrf.TwoPort
            #     raise NotImplementedError()
            # else:
            #     # cal = skrf.MultiPort
            #     raise NotImplementedError()

            # coeffs = {}
            # for term in terms:
            #     pna_name = term[0]
            #     skrf_name = re.sub(
            #         r"([A-Z])", lambda pat: f" {pat.group(1).lower()}", pna_name
            #     ).strip()

            #     coeffs[skrf_name] = self.query_values(
            #         f"SENS{self.cnum}:CORR:CSET:ETERM? '{pna_name}({a},{b})'",
            #         complex_values=True,
            #         container=np.array,
            #     )

            # self.parent.query_format = orig_query_fmt

            # freq = self.frequency
            # return cal.from_coefs(freq, coeffs)

        @calibration.setter
        def calibration(self, cal: skrf.Calibration) -> None:
            raise NotImplementedError()
        
        # TODO Parameter in richter reihenfolge für skrf?
        # TODO Passt der Name oder die Position im Program?
        def get_calibration_meas(self):
            orig_query_fmt = self.parent.query_format
            self.parent.query_format = ValuesFormat.BINARY_64

            stand_terms = self.query(f"SENS{self.cnum}:CORR:CSET:STAN:CAT?")
            
            pattern = '(\w+\(\d+,\d+\))'
            terms = re.findall(pattern, stand_terms)
            
            print(terms)
            
            coeffs = {}
            for term in terms:
                data = self.query_values(
                    f"SENS{self.cnum}:CORR:CSET:STAN:DATA? '{term}'",
                    complex_values=True,
                    container=np.array,
                )
                ntw = skrf.Network(s=data,frequency=self.frequency, name=term)
                coeffs[term] = ntw

            self.parent.query_format = orig_query_fmt

            return coeffs                
            
        # TODO Parameter in richtger reihenfolge für skrf?
        # TODO Passt Name oder die Position im Program?
        def get_calibration_error_terms(self):
            '''
            PNA_Error_Terms['12-term skrf np'] = {
            'forward directivity': PNA_Error_Terms['s']['Directivity(1,1)'].s.squeeze(),
            'forward source match': PNA_Error_Terms['s']['SourceMatch(1,1)'].s.squeeze(),
            'forward reflection tracking': PNA_Error_Terms['s']['ReflectionTracking(1,1)'].s.squeeze(),
            'forward transmission tracking': PNA_Error_Terms['s']['TransmissionTracking(1,2)'].s.squeeze(),
            'forward load match': PNA_Error_Terms['s']['LoadMatch(1,2)'].s.squeeze(),
            'forward isolation': PNA_Error_Terms['s']['CrossTalk(1,2)'].s.squeeze(),
            'reverse directivity': PNA_Error_Terms['s']['Directivity(2,2)'].s.squeeze(),
            'reverse load match': PNA_Error_Terms['s']['LoadMatch(2,1)'].s.squeeze(),
            'reverse reflection tracking': PNA_Error_Terms['s']['ReflectionTracking(2,2)'].s.squeeze(),
            'reverse transmission tracking': PNA_Error_Terms['s']['TransmissionTracking(2,1)'].s.squeeze(),
            'reverse source match': PNA_Error_Terms['s']['SourceMatch(2,2)'].s.squeeze(),
            'reverse isolation': PNA_Error_Terms['s']['CrossTalk(2,1)'].s.squeeze()
            }
            '''
               
            orig_query_fmt = self.parent.query_format
            self.parent.query_format = ValuesFormat.BINARY_64

            cset_terms = self.query(f"SENS{self.cnum}:CORR:CSET:ETER:CAT?")
            
            pattern = '(\w+\(\d+,\d+\))'
            terms = re.findall(pattern, cset_terms)

            
            coeffs = {}
            for term in terms:
                data = self.query_values(
                    f"SENS{self.cnum}:CORR:CSET:ETERM? '{term}'",
                    complex_values=True,
                    container=np.array,
                )

                ntw = skrf.Network(s=np.squeeze(data),frequency=self.frequency, name=term)
                coeffs[term] = ntw

            self.parent.query_format = orig_query_fmt

            return coeffs
        
        # TODO Richtiger Platz hier?
        def get_switch_terms(self, ports=(1, 2)):
            p1, p2 = ports

            channel = self.cnum

            forward_name = f"CH{channel}_FS"
            reverse_name = f"CH{channel}_RS"

            self.create_measurement(forward_name, 'a{:}b{:},{:}'.format(p2, p2, p1))
            self.create_measurement(reverse_name, 'a{:}b{:},{:}'.format(p1, p1, p2))

            self.sweep()

            forward = self.get_measurement(name=forward_name)
            forward.name = "forward switch term"
            reverse = self.get_measurement(name=reverse_name)
            reverse.name = "reverse switch term"

            self.delete_measurement(forward_name)
            self.delete_measurement(reverse_name)
            
            return forward, reverse




        
        
        # Main
        # TODO Smart Cal
            
        # TODO Other Cals
            
        # TODO Correction
            
        # TODO SRc Power Correction
            
        # TODO Interpolation
            
        # TODO Correction Methods
            
        # TODO Correction Properties
        
        # Port Extension
        # TODO Select Port
            
        # TODO Port Extension
            
        # TODO Time
            
        # TODO Distance
            
        # TODO Velocity Factor
            
        # TODO DC Loss
            
        # TODO Port Extensions
            
        # TODO Auto Port Extensions
            
        
        # Cal Sets & Cal Kits
        # TODO Cal Set
            
        # TODO Cal Set Viewer
        
        # TODO Cal Kit
            
        # TODO Ecal
            
        # TODO Cal Pod
            
        # TODO Uncertainity Setup

        # Fixtures
        # TODO Apply Fixtures
        
        # TODO Power Comp
            
        # TODO Fixture Setup --> Settings Window
            
        # TODO Cal Plane Manager
            
        # TODO Auto Fixture Removal


        #endregion
            

        #region Marker
        # Marker Setup
        # TODO Marker
        # TODO Reference Marker

        # TODO Delta
        
        # TODO Discrete
            
        # TODO Type
            
        # TODO Format
            
        # TODO Coupled
            
        # TODO Marker Display
            
        # TODO Marker Table
            
        # TODO All off


        #endregion
            

        #region Search
        # Main
        # TODO Max Search
            
        # TODO Min Search
            
        # TODO Search Range
            
        # TODO User Start / Stop
        
        # TODO Tracking
            
        # TODO Search
            
        # Peak
        # TODO Peak Search
        
        # TODO Threshold

        # TODO Excursion

        # TODO Peak Polarity

        # TODO Tracking    
        
        # Target
        # TODO Search Target
            
        # TODO Target Value
            
        # TODO Transition
            
        # TODO Tracking

        # Multi Peak and Target
        # TODO Multi Peak Search
            
        # TODO Peak Threshold
            
        # TODO Peak Ecursion
            
        # TODO Peak Polarity
            
        # TODO Multitarget Search
            
        # TODO Target Value
            
        # TODO Transisiton
            
        # TODO Tracking

        # Bandwith & Notch
        # TODO Bandwith Search

        # TODO BW Ref to

        # TODO BW Level

        # TODO Notch Search

        # TODO Notch Ref to

        # TODO Notch Level

        # TODO Tracking    
        
        # Comp & Sat
        # TODO Compression Search

        # TODO Comp Level

        # TODO Saturation Search

        # TODO Pmax Backoff

        # TODO Tracking    
        
        # Normal Op Pt
        # TODO Normal Op Search
            
        # TODO Backoff
            
        # TODO Pin Offset
            
        # TODO Tracking

        #endregion
            

        #region Freq
        # Main
        freq_start = VNA.command(
            get_cmd="SENS<self:cnum>:FREQ:STAR?",
            set_cmd="SENS<self:cnum>:FREQ:STAR <arg>",
            doc="""The start frequency [Hz]""",
            validator=FreqValidator(),
        )

        freq_stop = VNA.command(
            get_cmd="SENS<self:cnum>:FREQ:STOP?",
            set_cmd="SENS<self:cnum>:FREQ:STOP <arg>",
            doc="""The stop frequency [Hz]""",
            validator=FreqValidator(),
        )

        freq_center = VNA.command(
            get_cmd="SENS<self:cnum>:FREQ:CENT?",
            set_cmd="SENS<self:cnum>:FREQ:CENT <arg>",
            doc="""The frequency span [Hz].""",
            validator=FreqValidator(),
        )

        freq_span = VNA.command(
            get_cmd="SENS<self:cnum>:FREQ:SPAN?",
            set_cmd="SENS<self:cnum>:FREQ:SPAN <arg>",
            doc="""The frequency span [Hz].""",
            validator=FreqValidator(),
        )

        @property
        def freq_step(self) -> int:
            # Not all instruments support SENS:FREQ:STEP
            f = self.frequency
            return int(f.step)

        @freq_step.setter
        def freq_step(self, f: Union[int, float, str]) -> None:
            validator = FreqValidator()
            f = validator.validate_input(f)
            freq = self.frequency
            self.npoints = len(range(int(freq.start), int(freq.stop) + f, f))

        # TODO CW

        @property
        def frequency(self) -> skrf.Frequency:
            f = skrf.Frequency(
                start=self.freq_start,
                stop=self.freq_stop,
                npoints=self.npoints,
                unit="hz",
            )
            return f

        @frequency.setter
        def frequency(self, f: skrf.Frequency) -> None:
            self.freq_start = f.start
            self.freq_stop = f.stop
            self.npoints = f.npoints

        #endregion
            
        
        #region Power
        # Main
        # TODO Power Level
            
        # TODO RF Power On Off
            
        # TODO Start Power
            
        # TODO Stop Power
            
        # TODO Power and Attenuators
        
        # Port Power
        # TODO Port Power
        
        # Leveling & Offsets
        # TODO Leveling & Offsets
        # pna_A.write('SOUR1:POW4:ALC:REC:REF "r4"')
        # pna_A.write('SOUR1:POW4:ALC:REC:TOL 0.1')
        # pna_A.write('SOUR1:POW4:ALC:REC ON')


        # Attenuators
        # TODO Attenuators


        #endregion


        #region Sweep
        
        # TODO Verbessern / Anpassen der sweep function
        def sweep(self) -> None:
            self.parent.trigger_source = TriggerSource.IMMEDIATE
            self.parent._resource.clear()

            sweep_mode = self.sweep_mode
            sweep_time = self.sweep_time
            avg_on = self.averaging_on
            avg_mode = self.averaging_mode

            original_config = {
                "sweep_mode": sweep_mode,
                "sweep_time": sweep_time,
                "averaging_on": avg_on,
                "averaging_mode": avg_mode,
                "timeout": self.parent._resource.timeout,
            }

            if avg_on and avg_mode == AveragingMode.SWEEP:
                self.sweep_mode = SweepMode.GROUPS
                n_sweeps = self.averaging_count
                self.n_sweep_groups = n_sweeps
                n_sweeps *= self.parent.nports
            else:
                self.sweep_mode = SweepMode.SINGLE
                n_sweeps = self.parent.nports

            try:
                sweep_time *= n_sweeps * 1_000  # 1s per port
                self.parent._resource.timeout = max(sweep_time, 5_000)  # minimum of 5s
                self.parent.wait_for_complete()
            finally:
                self.parent._resource.clear()
                self.parent._resource.timeout = original_config.pop("timeout")
                for k, v in original_config.items():
                    setattr(self, k, v)
        
        
        # Main
        # TODO Anpassen des Names?
        npoints = VNA.command(
            get_cmd="SENS<self:cnum>:SWE:POIN?",
            set_cmd="SENS<self:cnum>:SWE:POIN <arg>",
            doc="""The number of frequency points. Sets the frequency step as a
                side effect
            """,
            validator=IntValidator(),
        )

        # TODO Anpassen des Names?
        sweep_type = VNA.command(
            get_cmd="SENS<self:cnum>:SWE:TYPE?",
            set_cmd="SENS<self:cnum>:SWE:TYPE <arg>",
            doc="""The type of sweep (linear, log, etc)""",
            validator=EnumValidator(SweepType),
        )

        # TODO x-axis Type

        # TODO Sweep Setup --> Freq. und Sweep Einstellungen in einem Fenster

        # Sweep Timing
        # TODO sweep_time --> Auto / Manuel?
        # pna_A.write(':SENSe1:SWEep:TIME 1') # in sec

        # TODO Anpassen des Names?
        sweep_time = VNA.command(
            get_cmd="SENS<self:cnum>:SWE:TIME?",
            set_cmd="SENS<self:cnum>:SWE:TIME <arg>",
            doc="""The time in seconds for a single sweep [s]""",
            validator=FloatValidator(decimal_places=3),
        )

        # TODO Dwell Time

        # TODO Sweep Delay

        # TODO Sweep Mode

        # TODO Sweep Sequence

        # TODO Fast Sweep

        # Source Control

        # TODO Frequency Offset

        # TODO Pulse Setup

        # TODO Balanced Source

        # TODO Phase Control

        # TODO DC Source

        # TODO LF Extension

        # TODO Global Source

        # Segment Table

        # TODO Add Segment

        # TODO Insert Segment

        # TODO Delete Segment

        # TODO Delete all Segements

        # TODO Segment Table --> Multiple Segment Settings in one Window

        # TODO Show Table

        #endregion
            

        #region Trigger 

        # TODO noch richtig einsortieren
        trigger_mode = VNA.command(
        get_cmd="SENS<self:cnum>:SWE:TRIG:MODE?",
        set_cmd="SENS<self:cnum>:SWE:TRIG:MODE <arg>",
        doc="""Trigger mode for the specified channel. This determines what each signal will trigger""",
        validator=EnumValidator(TriggerMode),
        )

        # TODO noch richtig einsortieren
        trigger_scope = VNA.command(
        get_cmd="SENSe<self:cnum>:SWEep:TRIGger:DELay?",
        set_cmd="SENSe<self:cnum>:SWEep:TRIGger:DELay <arg>",
        doc="""""",
        validator=FloatValidator(),
        )


        # Main
        sweep_mode = VNA.command(
            get_cmd="SENS<self:cnum>:SWE:MODE?",
            set_cmd="SENS<self:cnum>:SWE:MODE <arg>",
            doc="""This channel's trigger mode""",
            validator=EnumValidator(SweepMode),
        )

        # TODO Manual Trigger
        # TODO Namesgebung?
        trigger_manually = VNA.command(
            get_cmd=None,
            set_cmd="INIT<self:cnum>:IMM",
            doc="""Sends one trigger signal""",
            validator=IntValidator(),
        )

        # TODO Trigger Restart
        # pna_A.ch1.write('ABOR')

        # TODO Trigger Source

        # TODO Trigger --> Window with multiple Trigger Settings

        #endregion





        measurement_numbers = VNA.command(
            get_cmd="SYST:MEAS:CAT? <self:cnum>",
            set_cmd=None,
            doc="""The list of measurement numbers on this channel""",
            validator=DelimitedStrValidator(int),
        )

        averaging_on = VNA.command(
            get_cmd="SENS<self:cnum>:AVER:STATE?",
            set_cmd="SENS<self:cnum>:AVER:STATE <arg>",
            doc="""Whether averaging is on or off""",
            validator=BooleanValidator(),
        )

        averaging_count = VNA.command(
            get_cmd="SENS<self:cnum>:AVER:COUN?",
            set_cmd="SENS<self:cnum>:AVER:COUN <arg>",
            doc="""The number of measurements combined for an average""",
            validator=IntValidator(1, 65536),
        )

        averaging_mode = VNA.command(
            get_cmd="SENS<self:cnum>:AVER:MODE?",
            set_cmd="SENS<self:cnum>:AVER:MODE <arg>",
            doc="""How measurements are averaged together""",
            validator=EnumValidator(AveragingMode),
        )

        n_sweep_groups = VNA.command(
            get_cmd="SENS<self:cnum>:SWE:GRO:COUN?",
            set_cmd="SENS<self:cnum>:SWE:GRO:COUN <arg>",
            doc="""The number of triggers sent for one trigger command""",
            validator=IntValidator(1, int(2e6)),
        )

        @property
        def measurements(self) -> list[tuple[str, str]]:
            msmnts = self.query(f"CALC{self.cnum}:PAR:CAT:EXT?").replace('"', "")
            msmnts = msmnts.split(",")
            return list(zip(msmnts[::2], msmnts[1::2]))

        @property
        def measurement_names(self) -> list[str]:
            return [msmnt[0] for msmnt in self.measurements]



        @property
        def active_trace_sdata(self) -> np.ndarray:
            active_measurement = (
                self.query(f"CALC{self.cnum}:PAR:SEL?").replace('"', "").split(",")[0]
            )
            if active_measurement == "":
                raise RuntimeError("No trace is active. Must select measurement first.")
            return self.query_values(
                f"CALC{self.cnum}:DATA? SDATA", complex_values=True
            )


        def get_measurement(self, name: str, sweep: bool=True) -> skrf.Network:
            if name not in self.measurement_names:
                raise KeyError(f"{name} does not exist")

            self.parent.active_measurement = name
            ntwk = self.get_active_trace(sweep)
            ntwk.name = name
            return ntwk


        def get_active_trace(self, sweep: bool=True) -> skrf.Network:
            if sweep :
                self.sweep()
            
            orig_query_fmt = self.parent.query_format
            self.parent.query_format = ValuesFormat.BINARY_64

            ntwk = skrf.Network()
            ntwk.frequency = self.frequency
            ntwk.s = self.active_trace_sdata

            self.parent.query_format = orig_query_fmt

            return ntwk

        def get_sdata(self, a: int | str, b: int | str) -> skrf.Network:
            self.sweep()
            orig_query_fmt = self.parent.query_format
            self.parent.query_format = ValuesFormat.BINARY_64
            param = f"S{a}{b}"
            self.create_measurement("SKRF_TMP", param)
            self.parent.active_measurement = "SKRF_TMP"

            ntwk = skrf.Network()
            ntwk.frequency = self.frequency
            ntwk.s = self.active_trace_sdata

            self.delete_measurement("SKRF_TMP")
            self.parent.query_format = orig_query_fmt

            return ntwk

        def get_snp_network(
            self,
            ports: Optional[Sequence] = None,
        ) -> skrf.Network:
            if ports is None:
                ports = list(range(1, self.parent.nports + 1))

            orig_query_fmt = self.parent.query_format
            self.parent.query_format = ValuesFormat.BINARY_64
            self.parent.active_channel = self
            orig_snp_fmt = self.query("MMEM:STOR:TRAC:FORM:SNP?")
            self.write("MMEM:STOR:TRACE:FORM:SNP RI") # Expect Real/Imaginary data

            msmnt_params = [f"S{a}{b}" for a, b in itertools.product(ports, repeat=2)]

            names = []
            # Make sure the ports specified are driven
            for param in msmnt_params:
                # Not all models support CALC:PAR:TAG:NEXT
                name = f"CH{self.cnum}_SKRF_{param}"
                names.append(name)
                self.create_measurement(name, param)

            self.sweep()
            port_str = ",".join(str(port) for port in ports)
            raw = self.query_values(
                f"CALC{self.cnum}:DATA:SNP:PORTS? '{port_str}'", container=np.array
            )
            self.parent.wait_for_complete()

            for name in names:
                self.delete_measurement(name)

            # The data is sent back as:
            # [
            #   [frequency points],
            #   [s11.real],
            #   [s11.imag],
            #   [s12.real],
            #   [s12.imag],
            # ...
            # ]
            # but flattened. So we recreate the above shape from the flattened data
            npoints = self.npoints
            nrows = len(raw) // npoints
            nports = len(ports)
            data = raw.reshape((nrows, -1))[1:]

            ntwk = skrf.Network()
            ntwk.frequency = self.frequency
            ntwk.s = np.empty(
                shape=(len(ntwk.frequency), nports, nports), dtype=complex
            )
            real_rows = data[::2]
            imag_rows = data[1::2]
            for n in range(nports):
                for m in range(nports):
                    i = n * nports + m
                    ntwk.s[:, n, m] = real_rows[i] + 1j * imag_rows[i]

            self.parent.query_format = orig_query_fmt
            self.write("MMEM:STOR:TRACE:FORM:SNP %s" % orig_snp_fmt)

            return ntwk






    class Display(VNA):
        def __init__(self):
            super().__init__()
            pass

        def win_create(self):
            pass








    def __init__(self, address: str, backend: str = "@py") -> None:
        super().__init__(address, backend)

        self._resource.read_termination = "\n"
        self._resource.write_termination = "\n"

        # TODO Create Channels for all active channels on PNA-X
        self.create_channel(1, "Channel 1")
        self.active_channel = self.ch1

        self.model = self.id.split(",")[1]
        if self.model not in self._models:
            print(
                f"WARNING: This model ({self.model}) has not been tested with "
                "scikit-rf. By default, all features are turned on but older "
                "instruments might be missing SCPI support for some commands "
                "which will cause errors. Consider submitting an issue on GitHub to "
                "help testing and adding support.",
                file=sys.stderr,
            )



    #region Device Properties
    @property
    def nports(self) -> int:
        if self._supports("nports"):
            return int(self.query("SYST:CAP:HARD:PORT:COUN?"))
        else:
            return self._model_param("nports")

    #endregion


    #region Trace
        
    #endregion


    #region Channel
    channel_numbers = VNA.command(
        get_cmd="SYST:CHAN:CAT?",
        set_cmd=None,
        doc="""The channel numbers currently in use""",
        validator=DelimitedStrValidator(int),
    )


    #endregion


    #region Display
    
    #endregion
        
        
    #region Setup
    
    #endregion


    #region Meas
    
    #endregion

    
    #region Format

    @property
    def format_trace(self, mnum = 0) -> str:
        """Display format for the trace"""
        if mnum == 0:
            mnum = int(self.query("SYST:ACT:TRAC?"))
        format = str(self.query(f"CALCulate:MEASure{mnum}:FORMat?"))
        return getattr(self, format, None)

    @format_trace.setter
    def format_trace(self, form = 'MLOG', mnum = 0) -> None:
        """Display format for the trace"""
        if mnum == 0:
            mnum = int(self.query("SYST:ACT:TRAC?"))
              
        self.write(f"CALCulate:MEASure{mnum}:FORMat {form}")

    @property
    def format_group_delay_aper_freq(self, mnum = 0) -> float:
        """Group delay aperature using a fixed frequency range"""
        if mnum == 0:
            mnum = int(self.query("SYST:ACT:TRAC?"))
        val = float(self.query(f"CALC:MEAS{mnum}:GDEL:FREQ ?"))
        return getattr(self, val, None)

    @format_group_delay_aper_freq.setter
    def format_group_delay_aper_freq(self, freq : float, mnum = 0) -> None:
        """Group delay aperature using a fixed frequency range"""
        if mnum == 0:
            mnum = int(self.query("SYST:ACT:TRAC?"))
              
        self.write(f"CALC:MEAS{mnum}:GDEL:FREQ {freq}")

    @property
    def format_group_delay_aper_percent(self, mnum = 0) -> float:
        """Group delay aperature using a percent of the channel frequency span"""
        if mnum == 0:
            mnum = int(self.query("SYST:ACT:TRAC?"))
        val = float(self.query(f"CALC:MEAS{mnum}:GDEL:PERC?"))
        return getattr(self, val, None)

    @format_group_delay_aper_percent.setter
    def format_group_delay_aper_percent(self, percent : float, mnum = 0) -> None:
        """Group delay aperature using a percent of the channel frequency span"""
        if mnum == 0:
            mnum = int(self.query("SYST:ACT:TRAC?"))
              
        self.write(f"CALC:MEAS{mnum}:GDEL:PERC {percent}")

    @property
    def format_group_delay_aper_points(self, mnum = 0) -> float:
        """Group delay aperature using a fixed number of data points"""
        if mnum == 0:
            mnum = int(self.query("SYST:ACT:TRAC?"))
        val = float(self.query(f"CALC:MEAS{mnum}:GDEL:POIN?"))
        return getattr(self, val, None)

    @format_group_delay_aper_points.setter
    def format_group_delay_aper_points(self, points : float, mnum = 0) -> None:
        """Group delay aperature using a fixed number of data points"""
        if mnum == 0:
            mnum = int(self.query("SYST:ACT:TRAC?"))
              
        self.write(f"CALC:MEAS{mnum}:GDEL:POIN {points}")

    #endregion
        
    
    #region Scale
    
    #endregion
        
    
    #region Math
    
    #endregion
        
    
    #region Avg BW
    
    #endregion
        
    
    #region Cal
    
    #endregion


    #region Marker
    
    #endregion


    #region Search
    
    #endregion


    #region Freq
    
    #endregion


    #region Power
    rf_power = VNA.command(
        get_cmd="OUTPut:STATe?",
        set_cmd="OUTPut:STATe <arg>",
        doc="""Turns RF power from the source on or off""",
        validator= BooleanValidator(),
    )
    #endregion


    #region Sweep

    #endregion


    #region Trigger 

    # TODO Befehl nicht Channel abhängig?
    trigger_source = VNA.command(
        get_cmd="TRIG:SOUR?",
        set_cmd="TRIG:SOUR <arg>",
        doc="""The source of the sweep trigger signal""",
        validator=EnumValidator(TriggerSource),
    )
        
    trigger_scope = VNA.command(
        get_cmd="TRIG:SCOP?",
        set_cmd="TRIG:SCOP <arg>",
        doc="""Specifies whether a trigger signal is sent to all channels or only the current channel""",
        validator=EnumValidator(TriggerScope),
    )

    trigger_delay = VNA.command(
        get_cmd="TRIGger:DELay?",
        set_cmd="TRIGger:DELay <arg>",
        doc="""Trigger delay for ALL channels""",
        validator=FloatValidator(),
    )

    trigger_seq_type = VNA.command(
        get_cmd="TRIGger:TYPE?",
        set_cmd="TRIGger:TYPE <arg>",
        doc="""Specifies the type of EXTERNAL trigger input detection (Meas Trig IN)""",
        validator=EnumValidator(TriggerSeqType),
    )

    trigger_seq_slope = VNA.command(
        get_cmd="TRIGger:SLOPe?",
        set_cmd="TRIGger:SLOPe <arg>",
        doc="""Polarity expected by the external trigger input circuitry""",
        validator=EnumValidator(TriggerSeqSlope),
    )


    trigger_ready_polarity = VNA.command(
        get_cmd="TRIGger:READy:POLarity?",
        set_cmd="TRIGger:READy:POLarity <arg>",
        doc="""Specifies the polarity of Ready for Trigger output""",
        validator= EnumValidator(TriggeReadyPol),
    )

    #endregion



    def _supports(self, feature: str) -> bool:
        model_config = self._models.get(self.model, self._models["default"])
        return feature not in model_config["unsupported"]

    def _model_param(self, param: str):
        model_config = self._models.get(self.model, self._models["default"])
        return model_config[param]


    nerrors = VNA.command(
        get_cmd="SYST:ERR:COUN?",
        set_cmd=None,
        doc="""The number of errors since last cleared (see
            :func:`PNA.clear_errors`)""",
        validator=IntValidator(),
    )




    #region active Channel/Window/Display/Sheet
    @property
    def active_channel(self) -> Optional[Channel]:
        num = int(self.query("SYST:ACT:CHAN?"))
        return getattr(self, f"ch{num}", None)

    @active_channel.setter
    def active_channel(self, ch: Channel) -> None:
        if self.active_channel.cnum == ch.cnum:
            return

        msmnt = ch.measurement_numbers[0]
        self.write(f"CALC{ch.cnum}:PAR:MNUM {msmnt}")

    @property
    def active_measurement(self) -> str:
        return self.query("SYST:ACT:MEAS?").replace('"', "")

    @active_measurement.setter
    def active_measurement(self, name: str) -> None:
        measurements = {
            name: channel
            for channel in self.channels
            for name in channel.measurement_names
        }

        if name not in measurements:
            raise KeyError(f"{name} does not exist")

        if self._supports("fast_sweep"):
            self.write(f"CALC{measurements[name].cnum}:PAR:SEL '{name}',fast")
        else:
            self.write(f"CALC{measurements[name].cnum}:PAR:SEL '{name}'")

    @property
    def active_window(self):
        # TODO Implement function
        raise NotImplementedError()
    
    @active_window.setter
    def active_window(self):
        # TODO Implement function
        raise NotImplementedError()
    
    @property
    def active_sheet(self):
        return self.query("SYST:ACT:SHE?").replace('"', "")
    
    @active_sheet.setter
    def active_sheet(self):
        # TODO Implement function
        raise NotImplementedError()

    #endregion


    #region format propertys
    @property
    def query_format(self) -> vna.ValuesFormat:
        fmt = self.query("FORM?").replace("+", "")
        if fmt == "ASC,0":
            self._values_fmt = vna.ValuesFormat.ASCII
        elif fmt == "REAL,32":
            self._values_fmt = vna.ValuesFormat.BINARY_32
        elif fmt == "REAL,64":
            self._values_fmt = vna.ValuesFormat.BINARY_64
        return self._values_fmt

    @query_format.setter
    def query_format(self, fmt: vna.ValuesFormat) -> None:
        if fmt == vna.ValuesFormat.ASCII:
            self._values_fmt = vna.ValuesFormat.ASCII
            self.write("FORM ASC,0")
        elif fmt == vna.ValuesFormat.BINARY_32:
            self._values_fmt = vna.ValuesFormat.BINARY_32
            self.write("FORM:BORD SWAP")
            self.write("FORM REAL,32")
        elif fmt == vna.ValuesFormat.BINARY_64:
            self._values_fmt = vna.ValuesFormat.BINARY_64
            self.write("FORM:BORD SWAP")
            self.write("FORM REAL,64")
    #endregion



    
