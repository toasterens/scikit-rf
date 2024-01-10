# TODO

## Links

- https://github.com/Terrabits/rohdeschwarz/tree/main

## ToDos

- enums/trace_format.py --> noch nicht implementiert
- enums/model.py --> noch nicht implementiert
- Scipy commands abhängig von Gerätetyp und Softwareversion machen --> bei validators??
- validators --> füge SI units hinzu M,p,u,m,...
- active_calset_name: SENS<self:cnum>:CORR:CSET:ACT? NAME
- create_calset: SENS<self:cnum>:CORR:CSET:CRE <name>
- calset_data: SENS<self:cnum>:CORR:CSET:DATA?  <eterm>,<port a>,<port b> '<receiver>'
- Add Display
- Add External Microwave Controller
- Add Trace
- Save Screenshot
- Read Device Properties (Freq, Ports, Power, Serial Number)
- Load Setup --> File mit Einstellungen in den PNA-X Laden

## Implementation ListListe

### Trace

- [ ] Trace Setup
- [ ] Select Trace
- [ ] Measure Trace
- [ ] Trace Title
- Add Trace:
  - [ ] New Trace --> create_measurement --> Change Name
  - [ ] New Trace + Channel
  - [ ] New Trace + Window
  - [ ] New Trace + Window + Channel
  - [ ] New Traces
- [ ] Delete Trace --> delete_measurement --> Change Name???
- [ ] Trace Manager --> Return Trace Window, Channel, Format,...
- [ ] Trace Hold

### Channel

#### Channel Setup

- [ ] Select Channel
- [ ] Add Channel
  - [ ] New Trace + Channel
  - [ ] New Trace + Channel + Window
- [ ] Copy Channel
  - [ ] Copy to active Window
  - [ ] Copy to new Window
  - [ ] Copy Channel
- [ ] Delete Channel

### Window Setup

- [ ] Select Window
- [ ] Window Title
- [ ] Add Window
  - [ ] New Window
  - [ ] New Trace + Window
  - [ ] New Trace + Channel + Window
- [ ] Delete Window
- [ ] Move Window
- [ ] Window Layout --> win_layout --> nicht vom Channel abhängig --> nach unten verschieben

#### Sheet Setup

- [ ] Select Sheet
- [ ] Sheet Title
- [ ] Add Sheet
  - [ ] New Sheet
  - [ ] New Trace + Sheet
  - [ ] New Trace + Channel + Sheet
- [ ] Sheet Layout
  - [ ] 1 Sheet
  - [ ] 1 Sheet per trace
  - [ ] 1 Channel per sheet
  - [ ] 1 Window per sheet

#### Display Setup

- [ ] Trace Maximize
- [ ] Window Max
- [ ] Show Table --> None, Marker, Limit, Ripple, Segment
- [ ] Costomize Disply --> Allgemeine Settings
- [ ] Touchscreen on/off
- [ ] Display Update

### Setup

#### Main

- [ ] Sweep Setup --> Fenster mit mehreren Freq. Einstellungen --> gleiches fenster wie im unterpunt sweep
- [ ] Meas Class
- [ ] ❌ Quick Start ???
- [ ] Device Expert

#### ❌ System Setup

- [ ] Sound
- [ ] Remote Interface
- [ ] LAN Status
- [ ] Code Emulation

#### Internal Hardware

- [ ] RF Path Config
- [ ] IF Path Config
- [ ] Mechanical Devices
- [ ] Interface Control
- [ ] Reference
- [ ] LF Extension

#### External Hardware

- [ ] External Device
- [ ] Power Meter Setup
- [ ] Multiport
- [ ] Milimeter Config

### Meas

#### S-Parameter

- [ ] Create S-Parameter Meas

#### Balanced

- [ ] Topologie Window

##### Receivers

##### Waves

##### Auxilary

##### Meas Setup

- [ ] Conversions
- [ ] Correction
- [ ] Trace Hold
- [ ] Equition Editor
- [ ] Memory
- [ ] Time Domain
- [ ] Pulse Setup

### Format

#### Format 1

- ⁉ Format
- ⁉ Group Delay Aperature

#### Format 2

- [ ] Temperatur

### Scale

#### Main

- [ ] Autoscale
- [ ] Autoscale All
- [ ] Scale
- [ ] Reference Level
- [ ] Reference Position
- [ ] Y-Axis Spacing
- [ ] Scale Coupling

##### Electrical Delay

- [ ] Delay Time
- [ ] Delay Distance
- [ ] Distance Units
- [ ] Velocity Factor
- [ ] Media
- [ ] Waveguide Cut off

#### Constants

- [ ] System Z0
- [ ] Phase offset
- [ ] Mag offset
- [ ] Mag Slope

### Math

#### Memory

- [ ] Data --> Memory
- [ ] Normalize
- [ ] Data math
- [ ] Display Data Traces
- [ ] 8510 Mode
- [ ] Interpolate

#### Analysis

- [ ] Conversions
- [ ] Equition Editor
- [ ] Statictics
- [ ] AM Distortion
- [ ] Trace Deviations
- [ ] Uncertainity Analysis
- [ ] Limits
- [ ] Limit Table

#### ❌ Time Domain

- [ ] Transform
- [ ] Start Time
- [ ] Stop Time
- [ ] Center Time
- [ ] Span Time
- [ ] TD Mode
- [ ] TD Toolbar
- [ ] Time Domain Setup

##### Time Gating

- [ ] Gating
- [ ] Gate Start
- [ ] Gate Stop
- [ ] Gate Center
- [ ] Gate Span
- [ ] Gate Type
- [ ] Gate Shape
- [ ] Gating Setup

### Avg BW

##### Main

- [ ] Averaging
- [ ] Averaging Restart --> clear_averaging --> Entspricht clear_averaging --> Macht funktioner was sie machen soll?
- [ ] Average Type
- [ ] Stan / Gaus Settings --> if_bandwidth --> nahmen ändern?
- [ ] LF Auto BW

#### Smoothing

- [ ] Smoothing
- [ ] Smooth Percent
- [ ] Smooth Points

#### Delay Aperature

- [ ] Aperature Percent
- [ ] Aperature Points
- [ ] Aperature Freq

### Cal

- [ ] Name und function Anpassen --> calibration
- [ ] Parameter in richter reihenfolge für skrf?
- [ ] Passt der Name oder die Position im Program? --> get_calibration_meas
- [ ] Parameter in richtger reihenfolge für skrf?
- [ ] Passt Name oder die Position im Program? --> get_calibration_error_terms
- [ ] Switch Terms am richtigen Platz --> get_switch_terms

#### Main

- [ ] ❌ Smart Cal
- [ ] ❌ Other Cals
- [ ] Correction
- [ ] SRc Power Correction
- [ ] Interpolation
- [ ] Correction Methods
- [ ] Correction Properties

#### Port Extension

- [ ] Select Port
- [ ] Port Extension
- [ ] Time
- [ ] Distance
- [ ] Velocity Factor
- [ ] DC Loss
- [ ] Port Extensions
- [ ] Auto Port Extension

#### Cal Sets & Cal Kits

- [ ] Cal Set
- [ ] Cal Set Viewer
- [ ] Cal Kit
- [ ] Ecal
- [ ] Cal Pod
- [ ] Uncertainity Setup

#### Fixtures

- [ ] Apply Fixtures
- [ ] Power Comp
- [ ] Fixture Setup --> Settings Window
- [ ] Cal Plane Manager
- [ ] Auto Fixture Removal

### Marker

#### Marker Setup

- [ ] Marker
- [ ] Reference Marker
- [ ] Delta
- [ ] Discrete
- [ ] Type
- [ ] Format
- [ ] Coupled
- [ ] Marker Display
- [ ] Marker Table
- [ ] All off

### Search

#### Main

- [ ] Max Search
- [ ] Min Search
- [ ] Search Range
- [ ] User Start / Stop
- [ ] Tracking
- [ ] Search

#### Peak

- [ ] Peak Search
- [ ] Threshold
- [ ] Excursion
- [ ] Peak Polarity
- [ ] Tracking

#### Target

- [ ] Search Target
- [ ] Target Value
- [ ] Transition
- [ ] Tracking

#### Multi Peak and Target

- [ ] Multi Peak Search
- [ ] Peak Threshold
- [ ] Peak Ecursion
- [ ] Peak Polarity
- [ ] Multitarget Search
- [ ] Target Value
- [ ] Transisiton
- [ ] TODO Tracking

#### Bandwith & Notch

- [ ] Bandwith Search
- [ ] BW Ref to
- [ ] BW Level
- [ ] Notch Search
- [ ] Notch Ref to
- [ ] Notch Level
- [ ] Tracking

#### Comp & Sat

- [ ] Compression Search
- [ ] Comp Level
- [ ] Saturation Search
- [ ] Pmax Backoff
- [ ] Tracking

#### Normal Op Pt

- [ ] Normal Op Searce
- [ ] Backoff
- [ ] Pin Offset
- [ ] Tracking

### Freq

##### Main

- [ ] freq_start
- [ ] freq_stop
- [ ] freq_center
- [ ] freq_span
- [ ] freq_step
- [ ] CW
- [ ] frequency(self) -> Frequenz als skrf.Frequency übergeben

### Power

#### Main

- [ ] Power Level
- [ ] RF Power On Off
- [ ] Start Power
- [ ] Stop Power
- [ ] Power and Attenuators

#### Port Power

- [ ] Port Power

#### Leveling & Offsets

- [ ] Leveling & Offsets

```python
pna_A.write('SOUR1:POW4:ALC:REC:REF "r4"')
pna_A.write('SOUR1:POW4:ALC:REC:TOL 0.1')
pna_A.write('SOUR1:POW4:ALC:REC ON')
```
#### Attenuators

- [ ] Attenuators

### Sweep

- [ ] Verbessern / Anpassen der sweep function --> sweep()

#### Main

- [ ] npoints --> anpassen des Namens?
- [ ] sweep_type --> Anpassen des Names?
- [ ] x-axis Type
- [ ] Sweep Setup --> Freq. und Sweep Einstellungen in einem Fenster

#### Sweep Timing

- [ ] sweep_time --> Auto / Manuel?

```python
pna_A.write(':SENSe1:SWEep:TIME 1') # in sec
```

- [ ] sweep_time Anpassen des Names?
- [ ] Dwell Time
- [ ] Sweep Delay
- [ ] Sweep Mode
- [ ] Sweep Sequence
- [ ] Fast Sweep

#### Source Control

- [ ] Frequency Offset
- [ ] Pulse Setup
- [ ] Balanced Source
- [ ] Phase Control
- [ ] DC Source
- [ ] LF Extension
- [ ] Global Source

#### Segment Table

- [ ] Add Segment
- [ ] Insert Segment
- [ ] Delete Segment
- [ ] Delete all Segements
- [ ] Segment Table --> Multiple Segment Settings in one Window
- [ ] Show Table

### Trigger

- [ ] trigger:mode --> richtig einsortieren?
- [ ] trigger_scope --> noch richtig einsortieren

#### Main

- [ ] alter command sweep_mode --> namensgebung, funktion?
- [ ] Manual Trigger --> trigger_manually --> namensgebung?
- [ ] Trigger Restart  

```python
pna_A.ch1.write('ABOR')
```

- [ ] Trigger Source
- [ ] Trigger --> Window with multiple Trigger Settings
