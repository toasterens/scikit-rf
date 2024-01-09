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
from skrf.vi.validators import (
    BooleanValidator,
    DelimitedStrValidator,
    EnumValidator,
    FloatValidator,
    FreqValidator,
    IntValidator,
)
from skrf.vi.vna import VNA

from .enums    import AveragingMode
from .enums    import SweepMode
from .enums    import SweepType
from .enums    import TriggerSource

class Channel(VNA.Channel):
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
    
    # TODO Select Trace
        
    # TODO Measure Trace
        
    # TODO Trace Title
        
    # TODO Add Trace
        # TODO New Trace
        # TODO New Trace + Channel
        # TODO New Trace + Window
        # TODO New Trace + Window + Channel
        # TODO New Traces
    
    # TODO Delete Trace
        
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
        
    # TODO Window Layout
        # TODO 1 Window
        # TODO 2 Window
        # TODO 3 Window
        # TODO 4 Window
        # TODO 1 Trace per window
        # TODO 1 Channel per window
        # TODO Tile Window

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

    # TODO Averaging Restart

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
        
    # Attenuators
    # TODO Attenuators


    #endregion


    #region Sweep
    # Main
    npoints = VNA.command(
        get_cmd="SENS<self:cnum>:SWE:POIN?",
        set_cmd="SENS<self:cnum>:SWE:POIN <arg>",
        doc="""The number of frequency points. Sets the frequency step as a
            side effect
        """,
        validator=IntValidator(),
    )

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
    # Main
    sweep_mode = VNA.command(
        get_cmd="SENS<self:cnum>:SWE:MODE?",
        set_cmd="SENS<self:cnum>:SWE:MODE <arg>",
        doc="""This channel's trigger mode""",
        validator=EnumValidator(SweepMode),
    )

    # TODO Manual Trigger

    # TODO Trigger Restart

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

    def clear_averaging(self) -> None:
        self.write(f"SENS{self.cnum}:AVER:CLE")

    def create_measurement(self, name: str, parameter: str) -> None:
        self.write(f"CALC{self.cnum}:PAR:EXT '{name}',{parameter}")
        # Not all instruments support DISP:WIND:TRAC:NEXT
        traces = self.query("DISP:WIND:CAT?").replace('"', "")
        traces = [int(tr) for tr in traces.split(",")] if traces != "EMPTY" else [0]
        next_tr = traces[-1] + 1
        self.write(f"DISP:WIND:TRAC{next_tr}:FEED '{name}'")

    def delete_measurement(self, name: str) -> None:
        self.write(f"CALC{self.cnum}:PAR:DEL '{name}'")

    def get_measurement(self, name: str) -> skrf.Network:
        if name not in self.measurement_names:
            raise KeyError(f"{name} does not exist")

        self.parent.active_measurement = name
        ntwk = self.get_active_trace()
        ntwk.name = name
        return ntwk

    def get_active_trace(self) -> skrf.Network:
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




