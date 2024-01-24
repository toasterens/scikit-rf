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
from skrf.vi.vna.keysight.pna_enums import *


def additional_name_decorator(name: str):
    def decorator(function):
        function.__name__ = name
        return function
    return decorator


class PNA(VNA):

    # TODO Chante models to ENUM
    _models = {
        "default": {"nports": 2, "unsupported": []},
        "E8362C": {"nports": 2, "unsupported": ["nports", "freq_step", "fast_sweep"]},
        "N5227B": {"nports": 4, "unsupported": []},
    }

    
    class Channel(vna.Channel):
        def __init__(self, parent, cnum: int, cname: str):
            super().__init__(parent, cnum, cname)

            # TODO add copy channel
            # TODO make default_msmnt changeable 
            if cnum != 1:
                default_msmnt = f"CH{self.cnum}_S11_1"
                self.create_measurement(default_msmnt, "S11")

        def _on_delete(self):
            self.write(f"SYST:CHAN:DEL {self.cnum}")

        #region Trace
        # Trace Setup
        def create_measurement(self, name: str, parameter: str) -> None:
            """create measurement trace in active window"""
            bal_str = ['dd', 'dc', 'cd', 'cc']
            pattern = re.compile('|'.join(map(re.escape, bal_str)), re.IGNORECASE)
            
            if bool(pattern.search(parameter)):
                # bal s-parameter meas
                self._create_meas_bal_bal(name, parameter)
            else:
                self.write(f"CALC{self.cnum}:PAR:EXT '{name}',{parameter}")
                # Not all instruments support DISP:WIND:TRAC:NEXT
                traces = self.query("DISP:WIND:CAT?").replace('"', "")
                traces = [int(tr) for tr in traces.split(",")] if traces != "EMPTY" else [0]
                next_tr = traces[-1] + 1
                wnum = self.active_window
                self.write(f"DISP:WIND{wnum}:TRAC{next_tr}:FEED '{name}'")

        trace_new = additional_name_decorator("trace_new")(create_measurement)
        
        def _create_meas_bal_bal(self, name: str, parameter: str) -> None:
            """Create a diff. trace in active window"""
            # TODO true differential???
            self.write(f"CALC{self.cnum}:PAR:DEF:EXT '{name}',S11")
            self.write(f"CALC{self.cnum}:PAR:SEL '{name}'")
            self.write(f"CALC{self.cnum}:FSIM:BAL:PAR:STATe ON")
            self.write(f"CALC{self.cnum}:FSIM:BAL:PAR:BBAL:DEF '{parameter}'")
                        
            traces = self.query("DISP:WIND:CAT?").replace('"', "")
            traces = [int(tr) for tr in traces.split(",")] if traces != "EMPTY" else [0]
            next_tr = traces[-1] + 1
            wnum = self.active_window
            self.write(f"DISP:WIND{wnum}:TRAC{next_tr}:FEED '{name}'")       

        def _create_meas_bal_sing(self):
            return NotImplemented




        def trace_delete(self, name: str = '') -> None:
            """delete active trace"""
            if name == '':
                name = self.active_trace
                self.write(f"CALC{self.cnum}:PAR:DEL '{name}'")
            else:
                self.write(f"CALC{self.cnum}:PAR:DEL '{name}'")
            
        # TraceHold Enum
        @property
        def trace_hold(self) -> str:
            """active trace type of hold"""
            mnum = int(self.query("SYST:ACT:TRAC?"))
            hold_type = str(self.query(f"CALC{self.cnum}:MEAS{mnum}:HOLD:TYPE?"))
            return getattr(self, hold_type, None)

        @trace_hold.setter
        def trace_hold(self, hold_type: str) -> None:
            mnum = int(self.query("SYST:ACT:TRAC?"))
            self.write(f"CALC{self.cnum}:MEAS{mnum}:HOLD:TYPE {hold_type}")

        def trace_hold_restart(self) -> None:
            """active trace reset currently-stored data points and restarts Trace Hold type"""
            mnum = int(self.query("SYST:ACT:TRAC?"))
            self.write(f"CALC{self.cnum}:MEAS{mnum}:HOLD:CLE")




        #region Topology Winwow

        # ALC:FSIM:BAL:PAR:CUST:DEF "SDD33"
        # balanced_setup_topology_type = VNA.command(
        # get_cmd=None,
        # set_cmd="CALC<self:cnum>:FSIM:BAL:DEV <arg>",
        # doc="""Selects the device type for the balanced measurement""",
        # validator=EnumValidator(TopologyType),
        # )


        def balanced_setup(self, device : str, topology : str | list[int]):
            """Balanced / Single Measurement Setup
            B - Balanced port --> requires 2 physical port numbers: <nPos>, <nNeg>
            S - Single-ended port --> requires 1 physical port number
             
            Parameters
            ----------
            device : str
                _description_
            topology : str | list[int]
                Physical port numbers mapped to the logical ports

            Example
            -------
            
            Examples
            --------
            CALC:FSIM:BAL:TOP:XXXXX command.

            'The following example sets up 6 physical ports into 5 logical ports:
            'Logical port 1 is a single ended port mapped to physical port 1
            'Logical port 2 is a single ended port mapped to physical port 2
            'Logical port 3 is a balanced port mapped to physical ports 4 and 5
            'Logical port 4 is a single ended port mapped to physical port 3
            'Logical port 5 is a single ended port mapped to physical port 6


            'Example 1
            CALC:FSIM:BAL:DEV CUST
            CALC:DTOP "SSBSS",1,2,4,5,3,6
            CALC:MEAS:PAR "SDD33"

            'Example 2
            CALC:PAR:COUN 1
            CALC:FSIM:BAL:DEV CUST
            CALC:FSIM:BAL:PAR:STATE ON
            CALC:DTOPology "SSBSS",1,2,4,5,3,6
            CALC:FSIM:BAL:PAR:CUST:DEF "SDD33"
            """
            self.write(f"CALC{self.cnum}:FSIM:BAL:DEV CUST")
            self.write(f"CALC{self.cnum}:FSIM:BAL:PAR:STATE ON")
            self.write(f"CALC:DTOPology '{device}'', {topology}")

        def create_bal_meas(self):
            pass



        #endregion




        #endregion
            

        #region Channel
        # Channel Setup        
        # TODO Add Channel
            # TODO New Trace + Channel
            # TODO New Trace + Channel + Window

        # TODO Copy Channel
            # TODO Copy to active Window
            # TODO Copy to new Window
            # TODO Copy Channel

        # Delete Channel

        #endregion


        #region Setup       
        # Internal Hardware
        int_hard_reset_settings = VNA.command(
            get_cmd=None,
            set_cmd="SENS:PATH:CONF:SEL 'default'",
            doc="""Reset internal hardware settings""",
            validator=DelimitedStrValidator(),
        ) 
        
    
        # TODO richtiger validator?
        int_hard = VNA.command(
            get_cmd="SENS<self:cnum>:PATH:CONF:ELEM:SEL? <arg>",
            set_cmd="SENS<self:cnum>:PATH:CONF:ELEM:SEL <arg>",
            doc="""setting of a specified element in the current configuration""",
            validator=DelimitedStrValidator(),
        )
        
        
        # TODO RF Path Config
            
        # TODO IF Path Config
            
        # TODO Mechanical Devices
            
        # TODO Interface Control
            
        # TODO Reference
            
        # TODO LF Extension
        
        # External Hardware

        # TODO External Device
            
        # TODO Power Meter Setup
                
        # TODO Milimeter Config

        #endregion


        #region Meas
        # S-Parameter
            # TODO Create S-Parameter Meas
        
        # Balanced
        # TODO Topologie Window
                  
        #endregion


        #region Format

        #endregion
            

        #region Scale
        
        # Electrical Delay
        @property
        def scale_delay_time(self) -> float:
            """active trace electrical delay [s]"""
            mnum = int(self.query("SYST:ACT:TRAC?"))
            time = float(self.query(f"CALC{self.cnum}:MEAS{mnum}:CORR:EDEL:TIME?"))
            return getattr(self, time, None)

        @scale_delay_time.setter
        def scale_delay_time(self, delay: float) -> None:
            mnum = int(self.query("SYST:ACT:TRAC?"))  
            self.write(f"CALC{self.cnum}:MEAS{mnum}:CORR:EDEL:TIME {delay}")

        @property
        def scale_delay_distance(self) -> float:
            """active trace electrical delay [s]"""
            mnum = int(self.query("SYST:ACT:TRAC?"))
            dis = float(self.query(f"CALC{self.cnum}:MEAS{mnum}:CORR:EDEL:DIST?"))
            return getattr(self, dis, None)

        @scale_delay_distance.setter
        def scale_delay_distance(self, dis: float) -> None:
            mnum = int(self.query("SYST:ACT:TRAC?"))  
            self.write(f"CALC{self.cnum}:MEAS{mnum}:CORR:EDEL:DIST {dis}")

        @property
        def scale_delay_distance_unit(self) -> str:
            """units for electrical dealy in physical length (distance)"""
            mnum = int(self.query("SYST:ACT:TRAC?"))
            unit = str(self.query(f"CALC{self.cnum}:MEAS{mnum}:CORR:EDEL:UNIT?"))
            return getattr(self, unit, None)

        @scale_delay_distance_unit.setter
        def scale_delay_distance_unit(self, unit : str) -> None:
            mnum = int(self.query("SYST:ACT:TRAC?"))  
            self.write(f"CALC{self.cnum}:MEAS{mnum}:CORR:EDEL:UNIT {unit}")

        scale_delay_velocity = VNA.command(
            get_cmd="SENS<self:cnum>:CORR:RVEL:COAX?",
            set_cmd="SENS<self:cnum>:CORR:RVEL:COAX <arg>",
            doc="""velocity factor the be used with eelectrical delay and port extension""",
            validator=FloatValidator(min=0, max=10, decimal_places=2),
        )
        
        # TODO ScaleDelayMedia Enum
        @property
        def scale_delay_media(self) -> str:
            """active trace media used when calculating the electrical delay"""
            mnum = int(self.query("SYST:ACT:TRAC?"))
            unit = str(self.query(f"CALC{self.cnum}:MEAS{mnum}:CORR:EDEL:MED?"))
            return getattr(self, unit, None)

        @scale_delay_media.setter
        def scale_delay_media(self, unit: str) -> None:
            mnum = int(self.query("SYST:ACT:TRAC?"))  
            self.write(f"CALC{self.cnum}:MEAS{mnum}:CORR:EDEL:MED {unit}")

        # TODO Add frequency validator
        @property
        def scale_delay_cutoff(self) -> float:
            """active trace waveguide cutoff frequency used when the electrical delay media is set to WAVEGUIDE"""
            mnum = int(self.query("SYST:ACT:TRAC?"))
            unit = float(self.query(f"CALC{self.cnum}:MEAS{mnum}:CORR:EDEL:WGC?"))
            return getattr(self, unit, None)

        @scale_delay_cutoff.setter
        def scale_delay_cutoff(self, freq : float) -> None:
            mnum = int(self.query("SYST:ACT:TRAC?"))  
            self.write(f"CALC{self.cnum}:MEAS{mnum}:CORR:EDEL:WGC {freq}")

        # Constants
        @property
        def scale_const_offset_mag(self) -> float:
            """active trace offset magnitude data"""
            mnum = int(self.query("SYST:ACT:TRAC?"))
            mag = float(self.query(f"CALC{self.cnum}:MEAS{mnum}:OFFS:MAGN?"))
            return getattr(self, mag, None)

        @scale_const_offset_mag.setter
        def scale_const_offset_mag(self, mag : float) -> None:
            mnum = int(self.query("SYST:ACT:TRAC?"))  
            self.write(f"CALC{self.cnum}:MEAS{mnum}:OFFS:MAGN {mag}")

        @property
        def scale_const_offset_mag_slope(self) -> float:
            """active trace offsets the data trace magnitude to a value that changes linearly with frequency"""
            mnum = int(self.query("SYST:ACT:TRAC?"))
            slope = float(self.query(f"CALC{self.cnum}:MEAS{mnum}:OFFS:MAGN:SLOP?"))
            return getattr(self, slope, None)

        # TODO frequency validator?
        @scale_const_offset_mag_slope.setter
        def scale_const_offset_mag_slope(self, slope : float) -> None:
            mnum = int(self.query("SYST:ACT:TRAC?"))  
            self.write(f"CALC{self.cnum}:MEAS{mnum}:OFFS:MAGN:SLOP {slope}")

        @property
        def scale_const_offset_phase(self) -> float:
            """active trace offset magnitude data"""
            mnum = int(self.query("SYST:ACT:TRAC?"))
            phase = float(self.query(f"CALC{self.cnum}:MEAS{mnum}:OFFS:PHAS?"))
            return getattr(self, phase, None)

        @scale_const_offset_phase.setter
        def scale_const_offset_phase(self, phase : float) -> None:
            mnum = int(self.query("SYST:ACT:TRAC?"))  
            self.write(f"CALC{self.cnum}:MEAS{mnum}:OFFS:PHAS {phase}")

        #endregion
            

        #region Math
        @property
        def math_interpolate(self) -> bool:
            """active trace memory data interpolation"""
            mnum = int(self.query("SYST:ACT:TRAC?"))
            state = bool(self.query(f"CALC{self.cnum}:MEAS{mnum}:MATH:INT:STAT?"))
            return getattr(self, state, None)

        @math_interpolate.setter
        def math_interpolate(self, state : bool) -> None:
            mnum = int(self.query("SYST:ACT:TRAC?"))  
            self.write(f"CALC{self.cnum}:MEAS{mnum}:MATH:INT:STAT {state}")

        #endregion


        #region Avg BW
        # Main
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

        def averaging_restart(self) -> None:
            self.write(f"SENS{self.cnum}:AVER:CLE")

        averaging_type = VNA.command(
            get_cmd="SENS<self:cnum>:AVER:MODE?",
            set_cmd="SENS<self:cnum>:AVER:MODE <arg>",
            doc="""How measurements are averaged together""",
            validator=EnumValidator(AveragingType),
        )

        if_bandwidth = VNA.command(
            get_cmd="SENS<self:cnum>:BWID?",
            set_cmd="SENS<self:cnum>:BWID <arg>",
            doc="""The IF bandwidth [Hz]""",
            validator=FreqValidator(),
        )

        if_type= VNA.command(
            get_cmd="SENS<self:cnum>:IF:BAND:FILT?",
            set_cmd="SENS<self:cnum>:IF:BAND:FILT <arg>",
            doc="""Sets and returns the IF bandwidth filter shape""",
            validator=EnumValidator(IfType),
        ) 

        # Applicable Models: N522xB, N5234B, N5235B, N524xB, E5080A/B
        lf_auto_bW_on = VNA.command(
            get_cmd="SENS<self:cnum>:BWID:TRAC:FORC?",
            set_cmd="SENS:BWID:TRAC:FORC <arg>",
            doc="""Reduce IF BW at Low Frequencies feature in segments with IFBW arbitrary""",
            validator=BooleanValidator(),
        )       

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

        freq_cw = VNA.command(
            get_cmd="SENS<self:cnum>:FREQ:CW?",
            set_cmd="SENS<self:cnum>:FREQ:CW <arg>",
            doc="""Fixed Frequency [Hz]. Need Sweep in CW mode""",
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

        trigger_manually = VNA.command(
            get_cmd=None,
            set_cmd="INIT<self:cnum>:IMM",
            doc="""Sends one manual trigger signal""",
            validator=IntValidator(),
        )

        trigger_restart = VNA.command(
            get_cmd=None,
            set_cmd="ABOR",
            doc="""stops all sweep, then resume per current trigger settings""",
            validator=IntValidator(),
        )


        # TODO Trigger Source

        # TODO Trigger --> Window with multiple Trigger Settings


        #endregion





        measurement_numbers = VNA.command(
            get_cmd="SYST:MEAS:CAT? <self:cnum>",
            set_cmd=None,
            doc="""The list of measurement numbers on this channel""",
            validator=DelimitedStrValidator(int),
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


        def get_measurement(self, name: str, sweep: bool = True) -> skrf.Network:
            if name not in self.measurement_names:
                raise KeyError(f"{name} does not exist")

            self.parent.active_measurement = name
            ntwk = self.get_active_trace(sweep)
            ntwk.name = name
            return ntwk


        def get_active_trace(self, sweep: bool = True) -> skrf.Network:
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
    @property
    def trace_title(self) -> list:
        """active trace title"""
        wnum = self.active_window
        tnum = int(self.query("SYST:ACT:TRAC?"))
        title = str(self.query(f"DISP:WIND{wnum}:TRAC{tnum}:TITL:DATA?"))
        state = bool(self.query(f"DISP:WIND{wnum}:TRAC{tnum}:TITL:STAT?"))

        return getattr(self, [title, state], None)

    @trace_title.setter
    def trace_title(self, title = '', state = True) -> None:
        wnum = self.active_window
        tnum = int(self.query("SYST:ACT:TRAC?"))
        self.write(f"DISP:WIND{wnum}:TRAC{tnum}:TITL:DATA {title}")
        self.write(f"DISP:WIND{wnum}:TRAC{tnum}:TITL:STAT {state}")


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
    # Window Setup
    @property
    def win_title(self) -> list:
        """active trace window title"""
        wnum = self.active_window
        title = str(self.query(f"DISP:WIND{wnum}:TITL:DATA?"))
        state = bool(self.query(f"DISP:WIND{wnum}:TITL:STAT?"))

        return getattr(self, [title, state], None)

    @win_title.setter
    def win_title(self, title = '', state = True) -> None:
        wnum = self.active_window
        self.write(f"DISP:WIND{wnum}:TITL:DATA {title}")
        self.write(f"DISP:WIND{wnum}:TITL:STAT {state}")

    # TODO Auf welchem sheet wird das window erstellt?
    def win_create(self):
        """create new window"""
        wnum = self.query("SYST:WIND:CAT?")
        wnum = [int(x) for x in wnum.split(',')]
        wnum_new = wnum[-1] + 1
        self.query(f"DISP:WIND{wnum_new}:STAT 1")

    def win_delete(self, wnum = -1) -> None:
        """delete active window on the screen"""
        if wnum == -1:
            wnum = self.active_window
        self.query(f"DISP:WIND{wnum}:STAT 0")
        
    # TODO Move selected trace to window
    # TODO Input trace namen
    # TODO Get Trace Window Nummber of trace names
    def win_move(self, fromWin : int, tnum : int, toWin : int) -> None:
        """Moves a trace from one window to another window"""
        self.query(f"DISP:WIND{fromWin}:TRAC{tnum}:MOVE {toWin}")

    # TODO Welches Fenster wird hier überhaupt ausgewählt?
    win_layout = VNA.command(
        get_cmd=None,
        set_cmd="DISPARR <arg>",
        doc="""Window arrangement""",
        validator=EnumValidator(WindowLayout),
        )

    # Sheet Setup
    @property
    def sheet_title(self) -> list:
        """active trace sheet title"""
        snum = int(self.query("SYST:ACT:SHE?"))
        title = str(self.query(f"DISP:SHE{snum}:TITL:DATA?"))
        return getattr(self, title, None)

    @win_title.setter
    def sheet_title(self, title = '', snum = -1) -> None:
        if snum == -1:
            snum = int(self.query("SYST:ACT:SHE?")) 
        self.write(f"DISP:SHE{snum}:TITL:DATA {title}")

    def sheet_create(self):
        """Add new Sheet"""
        snum = self.query("SYST:SHE:CAT?")
        snum = [int(x) for x in snum.split(',')]
        snum_new = snum[-1] + 1
        self.query(f"DISP:SHE{snum_new}:STAT 1")

    def sheet_delete(self, snum = -1) -> None:
        """delete active sheet on the screen"""
        if snum == -1:
            snum = int(self.query("SYST:ACT:SHE?"))
        self.query(f"DISP:SHE{snum}:STAT 0")

    def sheet_layout(self, layout : str, snum = -1) -> None:
        """Sheet window arrangement"""
        if snum == -1:
            snum = int(self.query("SYST:ACT:SHE?"))
        self.write(f"DISP:SHE{snum}:ARR {layout}")

    # Display Setup
    trace_maximize = VNA.command(
        get_cmd="DISP:TMAX?",
        set_cmd="DISP:TMAX <arg>",
        doc="""active trace maximize (isolates) in active window""",
        validator=BooleanValidator(),
    )

    @property
    def win_max(self) -> list:
        """active trace window setting of maximized or normal"""
        wnum = self.active_window
        win_size = str(self.query(f"DISP:WIND{wnum}:SIZE?"))
        return getattr(self, win_size, None)

    # TODO WindowMax ENUM
    @win_max.setter
    def win_max(self, win_size : str) -> None:
        wnum = self.active_window
        self.write(f"DISP:WIND{wnum}:SIZE {win_size}")

    # TODO DisplayTable ENUM
    @property
    def win_table(self) -> None:
        """active window show table at the bottom of the analyzer screen"""
        wnum = self.active_window
        self.write(f"DISP:WIND{wnum}:TABL?")
    
    @win_table.setter
    def win_table(self, table : str,  wnum = -1) -> None:
        if wnum == -1:
            wnum = self.active_window
        self.write(f"DISP:WIND{wnum}:TABL {table}")       
    
    touchscreen = VNA.command(
        get_cmd="SYST:TOUC:STAT?",
        set_cmd="SYST:TOUC:STAT <arg>",
        doc="""enables and disables touchscreen""",
        validator=BooleanValidator(),
    )

    @property
    def disp_update(self) -> bool:
        """"""
        state = bool(self.query("DISP:UPD:STAT?"))
        return getattr(self, state, None)

    @disp_update.setter
    def disp_update(self, state : bool) -> None:
        self.write(f"DISP:UPD:STAT {state}")
        
        if state:
            self.write("DISP:UPD:IMM")

    #endregion
        
        
    #region Setup
    
    #endregion


    #region Meas
    # TODO MeasConvertion Enum
    @property
    def meas_conversion(self) -> str:
        """active trace measurement conversion"""
        mnum = int(self.query("SYST:ACT:TRAC?"))
        conv = str(self.query(f"CALC:MEAS{mnum}:CONV:FUNC?"))
        return getattr(self, conv, None)

    @meas_conversion.setter
    def meas_conversion(self, conv : str) -> None:
        mnum = int(self.query("SYST:ACT:TRAC?"))
        self.write(f"CALC:MEAS{mnum}:CONV:FUNC {conv}")

    #endregion

    
    #region Format
    @property
    def format_trace(self) -> str:
        """active trace display format"""
        mnum = int(self.query("SYST:ACT:TRAC?"))
        format = str(self.query(f"CALC:MEAS{mnum}:FORM?"))
        return getattr(self, format, None)

    @format_trace.setter
    def format_trace(self, form = 'MLOG') -> None:
        mnum = int(self.query("SYST:ACT:TRAC?"))
        self.write(f"CALC:MEAS{mnum}:FORM {form}")

    @property
    def format_group_delay_aper_freq(self) -> float:
        """active trace group delay aperature using a fixed frequency range"""
        mnum = int(self.query("SYST:ACT:TRAC?"))
        val = float(self.query(f"CALC:MEAS{mnum}:GDEL:FREQ ?"))
        return getattr(self, val, None)

    @format_group_delay_aper_freq.setter
    def format_group_delay_aper_freq(self, freq : float) -> None:
        mnum = int(self.query("SYST:ACT:TRAC?"))
        self.write(f"CALC:MEAS{mnum}:GDEL:FREQ {freq}")

    @property
    def format_group_delay_aper_percent(self) -> float:
        """atvie trace group delay aperature using a percent of the channel frequency span"""
        mnum = int(self.query("SYST:ACT:TRAC?"))
        val = float(self.query(f"CALC:MEAS{mnum}:GDEL:PERC?"))
        return getattr(self, val, None)

    @format_group_delay_aper_percent.setter
    def format_group_delay_aper_percent(self, percent : float) -> None:
        mnum = int(self.query("SYST:ACT:TRAC?"))
        self.write(f"CALC:MEAS{mnum}:GDEL:PERC {percent}")

    @property
    def format_group_delay_aper_points(self) -> float:
        """active trace group delay aperature using a fixed number of data points"""
        mnum = int(self.query("SYST:ACT:TRAC?"))
        val = float(self.query(f"CALC:MEAS{mnum}:GDEL:POIN?"))
        return getattr(self, val, None)

    @format_group_delay_aper_points.setter
    def format_group_delay_aper_points(self, points : float) -> None:
        mnum = int(self.query("SYST:ACT:TRAC?"))  
        self.write(f"CALC:MEAS{mnum}:GDEL:POIN {points}")

    #endregion
        
    
    #region Scale
    # Main
    def scale_autoscale(self) -> None:
        """active trace autoscale"""
        mnum = int(self.query("SYST:ACT:TRAC?"))
        self.write(f"DISP:MEAS{mnum}:Y:AUTO")

    def scale_autoscale_all(self) -> None:
        """active trace scale all traces in window"""
        wnum = self.active_window
        self.write(f"DISP:WIND{wnum}:Y:AUTO")
    
    @property
    def scale_div(self) -> float:
        """active trace Y axis scale per division associated with the specified measurement"""
        mnum = int(self.query("SYST:ACT:TRAC?"))
        scale = float(self.query(f"DISP:MEAS{mnum}:Y:SCAL:PDIV?"))
        return getattr(self, scale, None)

    @scale_div.setter
    def scale_div(self, scale : float) -> None:
        mnum = int(self.query("SYST:ACT:TRAC?"))  
        self.write(f"DISP:MEAS{mnum}:Y:SCAL:PDIV {scale}")

    @property
    def scale_ref_lv(self) -> float:
        """active trace reference level"""
        mnum = int(self.query("SYST:ACT:TRAC?"))
        scale = float(self.query(f"DISP:MEAS{mnum}:Y:SCAL:RLEV?"))
        return getattr(self, scale, None)

    @scale_ref_lv.setter
    def scale_ref_lv(self, scale : float) -> None:
        mnum = int(self.query("SYST:ACT:TRAC?"))  
        self.write(f"DISP:MEAS{mnum}:Y:SCAL:RLEV {scale}")

    @property
    def scale_ref_pos(self) -> float:
        """active trace scale reference position"""
        mnum = int(self.query("SYST:ACT:TRAC?"))
        scale = float(self.query(f"DISP:MEAS{mnum}:Y:SCAL:RPOS?"))
        return getattr(self, scale, None)

    @scale_ref_pos.setter
    def scale_ref_pos(self, scale : float) -> None:
        mnum = int(self.query("SYST:ACT:TRAC?"))  
        self.write(f"DISP:MEAS{mnum}:Y:SCAL:RPOS {scale}")

    # TODO Y-Axis Spacing
    @property
    def scale_y_axis_spacing(self) -> str:
        # """active trace Y axis format type, linear or logarithmic"""
        # ENUM ScaleSpacing
        # wnum = self.active_window
        # tnum = 
        # scale = str(self.query(f"DISP:WIND{wnum}:TRACe{tnum}:Y:SPAC?"))
        # return getattr(self, scale, None)
        return NotImplementedError()

    @scale_y_axis_spacing.setter
    def scale_y_axis_spacing(self, scale : float) -> None:
        # wnum = self.active_window
        # tnum = 
        # self.write(f"DISP:WIND{wnum}:TRACe{tnum}:Y:SPAC {scale}")
        return NotImplementedError()

    scale_coupling_method = VNA.command(
        get_cmd="DISP:WIND:TRAC:Y:SCAL:COUP:METH?",
        set_cmd="DISP:WIND:TRAC:Y:SCAL:COUP:METH <arg>",
        doc="""method of scale coupling""",
        validator=EnumValidator(ScaleCoupling),
    )

    # TODO Scale Coupling
    def scale_coupling(self, coupling_method = 'OFF', ) -> None:
        self.scale_coupling_method(coupling_method)
        
        # Window
        # DISPlay:WINDow<wnum>:TRACe:Y[:SCALe]:COUPle[:STATe] <bool>
        return NotImplementedError()


    # constants
    system_impedance = VNA.command(
        get_cmd="SENS:CORR:IMP:INP:MAGN?",
        set_cmd="SENS:CORR:IMP:INP:MAGN <arg>",
        doc="""System impedance value for the analyzer""",
        validator=FloatValidator(min=0.001, max=1000, decimal_places=3),
    )


    #endregion
        
    
    #region Math
    # Memory
    def math_data2mem(self, conv : str) -> None:
        """active trace data to memory"""
        mnum = int(self.query("SYST:ACT:TRAC?"))
        self.write(f"CALC:MEAS{mnum}:MATH:MEM")

    # TODO Testen, wenn kein math_data2mem vorher gemacht worden ist
    # TODO MathFunctions Enum
    def math_data_math(self) -> str:
        """active trace sets math operation"""
        mnum = int(self.query("SYST:ACT:TRAC?"))
        math = str(self.query(f"CALC:MEAS{mnum}:MATH:FUNC?"))
        return getattr(self, math, None)

    @math_data_math.setter
    def math_data_math(self, math = 'NORM') -> None:
        mnum = int(self.query("SYST:ACT:TRAC?"))
        self.write(f"CALC:MEAS{mnum}:MATH:FUNC {math}")       
    
    # Analysis
    # TODO Statictics
    def math_statistics(self, state : bool, ):
        """"""
        mnum = int(self.query("SYST:ACT:TRAC?"))

        if state:
            self.write("CALC:MEAS{mnum}:FUNC:STAT:STAT 1")
        else:
            self.write("CALC:MEAS{mnum}:FUNC:STAT:STAT 0")


        # Statistics - Mean, Standard Deviation, Peak to Peak
        # seuts statistic type that xou can query using  CALC:MEAS:FUNCtion:DATA?
        # CALCulate:MEASure:FUNCtion:TYPE
    
        # User Range - Full Span, User 1 to 16
        # CALCulate:MEASure:FUNCtion:DOMain:USER[:RANGe]

        # Start
        # CALCulate:MEASure:FUNCtion:DOMain:USER:STARt

        # Stop
        # CALCulate:MEASure:FUNCtion:DOMain:USER:STOP
    

    #endregion
        
    
    #region Avg BW

    # Smoothing
    @property
    def smoothing_on(self) -> bool:
        """active trace smoothing ON or OFF"""
        mnum = int(self.query("SYST:ACT:TRAC?"))
        state = bool(self.query(f"CALC:MEAS{mnum}:SMO:STAT?"))
        return getattr(self, state, None)

    @smoothing_on.setter
    def smoothing_on(self, state : bool) -> None:
        mnum = int(self.query("SYST:ACT:TRAC?"))
        self.write(f"CALC:MEAS{mnum}:SMO:STAT {state}")

    @property
    def smoothing_percent(self) -> float:
        """active trace amount of smoothing as a percentage of the number of data points"""
        mnum = int(self.query("SYST:ACT:TRAC?"))
        state = float(self.query(f"CALC:MEAS{mnum}:SMO:APER?"))
        return getattr(self, state, None)

    @smoothing_percent.setter
    def smoothing_percent(self, percent : float) -> None:
        mnum = int(self.query("SYST:ACT:TRAC?"))
        val_float = FloatValidator(1, 25)
        percent = val_float.validate_input(percent)
        self.write(f"CALC:MEAS{mnum}:SMO:APER {percent}")

    @property
    def smoothing_points(self) -> int:
        """active trace number of adjacent data points to average"""
        mnum = int(self.query("SYST:ACT:TRAC?"))
        state = int(self.query(f"CALC:MEAS{mnum}:SMO:POIN?"))
        return getattr(self, state, None)

    # TODO  Number of points from 1 point to maximum of 25% of data points in the channel. For example: if number of points in a data trace = 401, the maximum value for points = 100. The points value is always rounded to the closest odd number.
    @smoothing_points.setter
    def smoothing_points(self, points : int) -> None:
        mnum = int(self.query("SYST:ACT:TRAC?"))
        # npoints_trace = get number of points in data trace
        # val_float = IntValidator(1, 0.25*npoints_trace)
        # percent = val_float.validate_input(percent)
        self.write(f"CALC:MEAS{mnum}:SMO:POIN {points}")

    # Delay Aperature
    @property
    def aperature_percent(self) -> float:
        """active trace group delay aperture using a percent of the channel frequency span"""
        mnum = int(self.query("SYST:ACT:TRAC?"))
        state = float(self.query(f"CALC:MEAS{mnum}:GDEL:PERC?"))
        return getattr(self, state, None)

    # TODO Percent of frequency span to use for the aperture setting. Choose between the equivalent of two data points and 100 percent of the channel frequency span.
    @aperature_percent.setter
    def aperature_percent(self, percent : float) -> None:
        mnum = int(self.query("SYST:ACT:TRAC?"))
        # val_float = FloatValidator(2, 25)
        # percent = val_float.validate_input(percent)
        self.write(f"CALC:MEAS{mnum}:GDEL:PERC {percent}")

    # TODO Aperature Points
    @property
    def aperature_points(self) -> int:
        """active trace group delay aperture with fixed number of data points"""
        mnum = int(self.query("SYST:ACT:TRAC?"))
        state = int(self.query(f"CALC:MEAS{mnum}:GDEL:POIN?"))
        return getattr(self, state, None)

    # TODO Number of data points to  use for the aperture setting. Choose between two points and the number of points in the channel.
    @aperature_points.setter
    def aperature_points(self, points : int) -> None:
        mnum = int(self.query("SYST:ACT:TRAC?"))
        # npoints_trace = get number of points in data trace
        # val_float = IntValidator(1, 0.25*npoints_trace)
        # percent = val_float.validate_input(percent)
        self.write(f"CALC:MEAS{mnum}:GDEL:POIN {points}")

    @property
    def aperature_freq(self) -> float:
        """active trace group delay aperture with fixed frequency range"""
        mnum = int(self.query("SYST:ACT:TRAC?"))
        freq = float(self.query(f"CALC:MEAS{mnum}:GDEL:FREQ?"))
        return getattr(self, freq, None)

    # TODO Frequency range (in Hz) to use for the aperture setting. Choose between the equivalent of two data points and the channel frequency span.
    @aperature_freq.setter
    def aperature_freq(self, freq : float) -> None:
        mnum = int(self.query("SYST:ACT:TRAC?"))
        self.write(f"CALC:MEAS{mnum}:GDEL:FREQ {freq}")

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
    pow__on = VNA.command(
        get_cmd="OUTPut:STATe?",
        set_cmd="OUTPut:STATe <arg>",
        doc="""Turns RF power from the source on or off""",
        validator=BooleanValidator(),
    )
    #endregion


    #region Sweep

    #endregion


    #region Trigger 
    trigger_restart = VNA.command(
        get_cmd=None,
        set_cmd="ABOR",
        doc="""stops all sweep, then resume per current trigger settings""",
        validator=IntValidator(),
    )

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

    preset = VNA.command(
        get_cmd=None,
        set_cmd="*RST",
        doc="""Preset device""",
        validator=IntValidator(),
    )

    full_preset = VNA.command(
        get_cmd=None,
        set_cmd="SYST:FPR",
        doc="""standard preset, deletes the default trace, measurement, and window""",
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
    def active_trace(self) -> str:
        '''active trace internal pna name'''
        return self.query("SYST:ACT:MEAS?").replace('"', "")

    @active_trace.setter
    def active_trace(self, name: str) -> None:
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

    # Applicable Models: N522xB, N523xB, N524xB, M937xA, P937xA
    @property
    def active_window(self):
        """Active Window of selected trace"""
        cnum = int(self.query("SYST:ACT:CHAN?"))
        wnum = int(self.query(f"CALC{cnum}PAR:WNUM?"))
        return getattr(self, wnum, None)
    
    # @active_window.setter
    # def active_window(self):
    #     # TODO Implement function
    #     raise NotImplementedError()
    
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



    
