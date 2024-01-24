# TODO

## Links

- <https://github.com/Terrabits/rohdeschwarz/tree/main>

## ToDos

- enums/model.py --> noch nicht implementiert
- Scipy commands abhängig von Gerätetyp und Softwareversion machen --> bei validators??
- validators --> füge SI units hinzu M,p,u,m,...
- active_calset_name: ```SENS<self:cnum>:CORR:CSET:ACT? NAME```
- create_calset: ```SENS<self:cnum>:CORR:CSET:CRE <name>```
- calset_data: ```SENS<self:cnum>:CORR:CSET:DATA?  <eterm>,<port a>,<port b> '<receiver>'```
- Add External Microwave Controller
- Save Screenshot
  - Screenshot erstellen und auf PNA Speichern
  - mit command auf PC übertragen ```MMEMory:TRANsfer <fileName>,<dataBlock>```

```python
PNA.timeout = 10000
PNA.write(':FORMat:DATA %s,%d' % ('REAL', 64))
PNA.write(':DISPlay:ANNotation:MESSage:STATe %d' % (0))
PNA.write(':HCOPy:FILE "%s"' % ('C:\\tmppnascreen.png'))
dataBlock = PNA.query_binary_values(':MMEMory:TRANsfer? "%s"' % ('C:\\tmppnascreen.png'),'B',False)
PNA.write(':MMEMory:DELete "%s"' % ('C:\\tmppnascreen.png'))
PNA.write(':DISPlay:ANNotation:MESSage:STATe %d' % (1))
```

- Read Device Properties (Freq, Ports, Power, Serial Number)
- Load Setup --> File mit Einstellungen in den PNA-X Laden
- Create SI-Validator
- ist fast measurement deaktivierbar bei trace generation im program?
- Segment Sweep muss noch implementiert werden

```python
# start of Upload_Segment_List

# Uploads two sweep segments to an Agilent PNA family network analyzer and displays the sweep table.
# 
# Instructions for Running:
# 1. Enter your instrument address in the Connect step.
# 2. Run the sequence.
# 
# Operation:
# 1. Uploads two segments to the PNA.
# 2. Displays the sweep table.

rm = visa.ResourceManager()
PNA = rm.open_resource('%prompt')
PNA.write(':FORMat:DATA %s' % ('ASCii'))
PNA.write(':SENSe1:SEGMent:LIST %s,%d,%s' % ('SSTOP', 2, '1,101,10000000,1000000000,1,201,1000000000,3000000000'))
PNA.write(':SENSe1:SWEep:TYPE %s' % ('SEGMent'))
PNA.write(':DISPlay:WINDow1:TABLe %s' % ('SEGMent'))
PNA.close()
rm.close()

# end of Upload_Segment_List
```

// Destroy all measurements and add a window
WriteString("SYST:FPR");
WriteString("DISP:WIND:STAT 1");

## Implementation ListListe

### ⚙ Trace

- ⚙ Select Trace / active Trace ➡ active_trace
- ⚙ Measure Trace / create Trace ➡ create_measurement / trace_new
  - Single S-Parameter
  - Diff S-Parameter
- ⚙ Trace Title ➡ trace_title
- ❓ Add Trace:
  - ❓ New Trace + Channel ➡
  - ❓ New Trace + Window ➡
  - ❓ New Trace + Window + Channel ➡
- ⚙ Delete Trace ➡ trace_delete
- ❓ Trace Manager --> Return Trace Window, Channel, Format,... ➡
- ⚙ Trace Hold ➡ trace_hold
- ⚙ Trace Hold ➡ trace_hold_restart

### ⚙ Channel

- ⚙ Select Channel ➡ python channel class
- Add Channel ➡
  - ❓ New Trace + Channel ➡
  - ❓ New Trace + Channel + Window ➡
- Copy Channel
  - ❓ Copy to active Window ➡
  - ❓ Copy to new Window ➡
  - ❓ Copy Channel ➡ ```SYSTem:MACRo:COPY:CHANnel<cnum>[:TO] <num>```
- ⚙ Delete Channel ➡ delete_channel

### ⚙ Window Setup

- ⚙ Select Window ➡ active_measurement
- ⚙ Window Title ➡ win_title
- Add Window
  - ⚙ New Window ➡ win_create
  - ❓ New Trace + Window ➡
  - ❓ New Trace + Channel + Window ➡
- ⚙ Delete Window ➡ win_delete
- 🩺 Move Window ➡ win_move
- ⚙ Window Layout --> win_layout

### ⚙ Sheet Setup

- ⚙ Select Sheet ➡ active_measurement
- ⚙ Sheet Title ➡ sheet_title
- Add Sheet
  - ⚙ New Sheet ➡ sheet_create
  - ❓ New Trace + Sheet ➡
  - ❓ New Trace + Channel + Sheet ➡
- ⚙ Delete Sheet ➡ sheet_delete
- ⚙ Sheet Layout ➡ sheet_layout

### ⚙ Display Setup

- ⚙ Trace Maximize ➡ trace_maximize
- ⚙ Window Max ➡ win_max
- ⚙ Show Table --> None, Marker, Limit, Ripple, Segment ➡ win_table
- ❌ Costomize Disply --> Allgemeine Settings ➡
- ⚙ Touchscreen on/off ➡ touchscreen
- ⚙ Display Update ➡ disp_update

### ⚙ Setup

#### ❌ Main

- ❌ Sweep Setup --> Fenster mit mehreren Freq. Einstellungen --> gleiches fenster wie im unterpunt sweep ➡
- ❌ Meas Class ➡
- ❌ Quick Start
- ❌ Device Expert ➡

#### ❌ System Setup

- ❌ Sound
- ❌ Remote Interface
- ❌ LAN Status
- ❌ Code Emulation

#### Internal Hardware

- RF / IF Path Config
  - List available IF settings ➡
  - List available RF settings ➡
  - Config RF IF setting ➡
- Mechanical Devices ➡
- Interface Control ➡
- Reference ➡
- LF Extension ➡

#### External Hardware

- External Device ➡
- Power Meter Setup ➡
- ❌ Multiport ➡
- Milimeter Config ➡

### Meas

#### S-Parameter

- Create S-Parameter Meas ➡

#### Balanced

- Topologie Window ➡

##### Meas Setup

- ⚙ Conversions ➡ meas_conversion
- ❌Correction ➡ in Calibration
- ⚙ Trace Hold ➡ trace_hold
- ❌ Equition Editor ➡ in math
- ❌ Memory ➡ in math
- ❌ Time Domain ➡
- ❌ Pulse Setup ➡

### ⚙ Format

- ⚙ Format ➡ format_trace
- ⚙ Group Delay Aperature ➡ format_group_delay_aper_freq / format_group_delay_aper_percent / format_group_delay_aper_points
- ❌ Temperatur ➡

### ⚙ Scale

#### ⚙ Main Scale

- ⚙ Autoscale ➡ scale_autoscale
- ⚙ Autoscale All ➡ scale_autoscale_all
- ⚙ Scale ➡ scale_div
- ⚙ Reference Level ➡ scale_ref_lv
- ⚙ Reference Position ➡ scale_ref_pos
- 🩺 Y-Axis Spacing ➡ scale_y_axis_spacing --> keine ahnung wie man sinnvol tnum vom aktullen trace bekommen soll
- ⚙ Scale Coupling ➡ scale_coupling

#### ⚙ Electrical Delay

- ⚙ Delay Time ➡ scale_delay_time
- ⚙ Delay Distance ➡ scale_delay_distance
- ⚙ Distance Units ➡ scale_delay_distance_units
- ⚙ Velocity Factor ➡ scale_delay_velocity
- ⚙ Media ➡ scale__delay_media
- ⚙ Waveguide Cut off ➡ scale_delay_cutoff

#### ⚙ Constants

- ⚙ System ➡ Z0 system_impedance
- ⚙ Phase offset ➡ scale_const_offset_phase
- ⚙ Mag offset ➡ scale_const_offset_mag
- ⚙ Mag Slope ➡ scale_const_offset_mag_slope

### Math

#### ⚙ Memory

- ⚙ Data --> Memory ➡ math_data2mem
- ⚙ Data math ➡ math_data_math
- ❌ Display Data Traces ➡
- ⚙ Interpolate ➡ ch.math_interpolate

#### Analysis

- ⚙ Conversions ➡ meas_conversion
- ❌ Equition Editor ➡
- 🩺 Statictics ➡
- ❌ AM Distortion ➡
- ❌ Trace Deviations ➡
- ❌ Uncertainity Analysis ➡
- ❌ Limits ➡
- ❌ Limit Table ➡

#### ❌ Time Domain

- ❌ Transform
- ❌ Start Time
- ❌ Stop Time
- ❌ Center Time
- ❌ Span Time
- ❌ TD Mode
- ❌ TD Toolbar
- ❌ Time Domain Setup

#### ❌ Time Gating

- ❌ Gating ➡
- ❌ Gate Start ➡
- ❌ Gate Stop ➡
- ❌ Gate Center ➡
- ❌ Gate Span ➡
- ❌ Gate Type ➡
- ❌ Gate Shape ➡
- ❌ Gating Setup ➡

### ⚙ Avg BW

#### ⚙ Main Avg BW

- ✔ Averaging ➡ ch.averaging_on, ch.averaging_count
- ✔ Averaging Restart ➡ ch.averaging_clear
- ✔ Average Type ➡ ch.averaging_type
- ⚙ IF BandWith ➡ ch.if_bandwith
- ⚙ IF Stan / Gaus Settings ➡ ch.if_type
- ⚙ LF Auto BW ➡ ch.lf_auto_bw_on

#### ⚙ Smoothing

- ⚙ Smoothing ➡ smoothing_on
- ⚙ Smooth Percent ➡ smoothing_percent
- ⚙ Smooth Points ➡ smoothing_points

#### ⚙ Delay Aperature

- ⚙ Aperature Percent ➡ aperature_percent
- ⚙ Aperature Points ➡ aperature_points
- ⚙ Aperature Freq ➡ aperature_freq

### Cal

- Name und function Anpassen --> calibration ➡
- Parameter in richter reihenfolge für skrf? ➡
- Passt der Name oder die Position im Program? --> get_calibration_meas ➡
- Parameter in richtger reihenfolge für skrf? ➡
- Passt Name oder die Position im Program? --> get_calibration_error_terms ➡
- Switch Terms am richtigen Platz --> get_switch_terms ➡

#### Main Cal

- ❌ Smart Cal
- ❌ Other Cals
- Correction ➡
- SRc Power Correction ➡
- Interpolation ➡
- Correction Methods ➡
- Correction Properties ➡

#### Port Extension

- Select Port ➡
- Port Extension ➡
- Time ➡
- Distance ➡
- Velocity Factor ➡
- DC Loss ➡
- Port Extensions ➡
- Auto Port Extension ➡

#### Cal Sets & Cal Kits

- Cal Set ➡
- Cal Set Viewer ➡
- Cal Kit ➡
- ❌ Ecal ➡
- Cal Pod ➡
- Uncertainity Setup ➡

#### Fixtures

- Apply Fixtures ➡
- Power Comp ➡
- Fixture Setup --> Settings Window ➡
- Cal Plane Manager ➡
- Auto Fixture Removal ➡

### Marker

#### Marker Setup

- Marker ➡
- Reference Marker ➡
- Delta ➡
- Discrete ➡
- Type ➡
- Format ➡
- Coupled ➡
- Marker Display ➡
- Marker Table ➡
- All off ➡

### Search

#### Main Search

- Max Search ➡
- Min Search ➡
- Search Range ➡
- User Start / Stop ➡
- Tracking ➡
- Search ➡

#### Peak

- Peak Search ➡
- Threshold ➡
- Excursion ➡
- Peak Polarity ➡
- Tracking ➡

#### Target

- Search Target ➡
- Target Value ➡
- Transition ➡
- Tracking ➡

#### Multi Peak and Target

- Multi Peak Search ➡
- Peak Threshold ➡
- Peak Ecursion ➡
- Peak Polarity ➡
- Multitarget Search ➡
- Target Value ➡
- Transisiton ➡
- Tracking ➡

#### Bandwith & Notch

- Bandwith Search ➡
- BW Ref to ➡
- BW Level ➡
- Notch Search ➡
- Notch Ref to ➡
- Notch Level ➡
- Tracking ➡

#### Comp & Sat

- Compression Search ➡
- Comp Level ➡
- Saturation Search ➡
- Pmax Backoff ➡
- Tracking ➡

#### Normal Op Pt

- Normal Op Searce ➡
- Backoff ➡
- Pin Offset ➡
- Tracking ➡

### ⚙ Freq

#### ⚙ Main Freq

- ✔ freq start ➡ ch.freq_start
- ✔ freq stop ➡ ch.freq_stop
- ✔ freq center ➡ ch.freq_center
- ✔ freq span ➡ ch.freq_span
- ✔ freq step ➡ ch.freq_step
- ⚙ CW freq ➡ ch.freq_cw

#### ✔ Freq Additional Features

- ✔ skrf.Frequency ➡ frequency()

### Power

#### Main Power

- Power Level ➡ ch.pow_lv
- ✔ RF Power On Off ➡ ch.pow_on
- Start Power ➡ ch.pow_start
- Stop Power ➡ ch.pow_stop
- Power and Attenuators ➡

#### Port Power

- Port Power ➡ Was ist Port Power

#### Leveling & Offsets

- Leveling & Offsets ➡

```python
pna_A.write('SOUR1:POW4:ALC:REC:REF "r4"')
pna_A.write('SOUR1:POW4:ALC:REC:TOL 0.1')
pna_A.write('SOUR1:POW4:ALC:REC ON')
```

#### Attenuators

- Attenuators ➡

### Sweep

- Verbessern / Anpassen der sweep function --> sweep() ➡

#### Main Sweep

- npoints --> anpassen des Namens? ➡
- sweep_type --> Anpassen des Names? ➡
- x-axis Type ➡
- Sweep Setup --> Freq. und Sweep Einstellungen in einem Fenster ➡

#### Sweep Timing

- sweep_time --> Auto / Manuel? ➡

```python
pna_A.write(':SENSe1:SWEep:TIME 1') # in sec
```

- sweep_time Anpassen des Names? ➡
- Dwell Time ➡
- Sweep Delay ➡
- Sweep Mode ➡
- Sweep Sequence ➡
- Fast Sweep ➡

#### Source Control

- Frequency Offset ➡
- Pulse Setup ➡
- Balanced Source ➡
- Phase Control ➡
- DC Source ➡
- LF Extension ➡
- Global Source ➡

#### Segment Table

- Add Segment ➡
- Insert Segment ➡
- Delete Segment ➡
- Delete all Segements ➡
- Segment Table --> Multiple Segment Settings in one Window ➡
- Show Table ➡

### Trigger

- trigger_scope --> noch richtig einsortieren ➡

#### Main Trigger

- Sweep type ➡ ch.sweep_mode
- Manual Trigger ➡ ch.trigger_manually
- Trigger Restart ➡ ch.trigger_restart
- Trigger Source ➡ trigger_source
- Trigger Setup
  - Trigger Source ➡ trigger_source
  - Trigger Scope ➡ trigger_scope
  - Channel Trigger State ➡ 
  - Continuous ➡
  - Groups ➡
  - Single ➡
  - Hold ➡
- Meas Trigger
  - Global Trigger Dleay
  - Meas Trig in BNC
  - Handler I/O Pin 18
  - Pulse3
  - Rear SMB
  - Backplane
  - Level/Edge
  - Accept trgger before armed
  - Meas Trig Ready
  - Trigger ready -Rear SMB
  - Trigger ready -Backplane
  - Handler I/O Pin 21
  - Ready High
  - Ready Low
- Aux Trig 1
  - Enable
  - Positive Pulse
  - Negative Pulse
  - Before Acquisition
  - After Acquisition
  - Per Point
  - Rear SMB
  - Backplane
  - Pulse Duration
  - Enable Wair-for-Device Handshake
  - Positive Edge
  - Negative Edge
  - Delay
- Aux Trig 2
  - Enable
  - Positive Pulse
  - Negative Pulse
  - Before Acquisition
  - After Acquisition
  - Per Point
  - Rear SMB
  - Backplane
  - Pulse Duration
  - Enable Wair-for-Device Handshake
  - Positive Edge
  - Negative Edge
  - Delay
- Pule Trigger
  - Trigger Source
  - High Level
  - Positive Edge
  - Negative Edge
  - Syncrhonize ADC using pulse trigger
  - ACD trigger delay

## Matlab Halcyon

```python
# ####################################################################################################
# Delete all traces
'CALCulate1:PARameter:DELete:ALL'

# ####################################################################################################
function [freq, data_complex, N_traces, traceNames] = func_M9371A_getComplexData(ZVA_obj)

% changes the state of each channel to the initiation state in the trigger system
% fprintf(ZVA_obj,'INIT');   
% pause(0.001)

% Returns an ASCII "+1" when all pending overlapped operations have been completed
% fprintf(ZVA_obj,'*OPC?');   
% pause(0.001)

% Sets the data format for transferring measurement data and frequency data.
%fprintf(ZVA_obj,['FORM REAL,32']); 


fprintf(ZVA_obj,['format:data ascii']); 
fprintf(ZVA_obj, ['CALC:PAR:CAT:EXT? DEF']);
%read_traceNames = binblockread(ZVA_obj, 'float');
read_traceNames = fscanf(ZVA_obj);
%fread(ZVA_obj,1);   % Read terminating character LF

pause(0.1)

fprintf(ZVA_obj,['FORM REAL,32']); 


% get Trace Names
read_traceNames = convertCharsToStrings(read_traceNames);
read_traceNames = erase(read_traceNames,'"');
read_traceNames = regexp(read_traceNames, ',', 'split');

i = 1;
for n = 1:2:length(read_traceNames)
    traceNames(i) = read_traceNames(n);
    i = i+1;
end


% Get Trace Numbers
for n = 1:1:length(traceNames)
    % Get trace number
    traceNum(n) = str2double(regexp(string(traceNames(n)),'\d*','Match'));
end


% Read selected Traces
for i=1:1:length(traceNum)
    fprintf(ZVA_obj, strcat('CALCulate:MEASure', num2str(traceNum(i)), ':DATA:SDATA?'));
    data_complex_meas(:,i) = binblockread(ZVA_obj, 'float');
    fread(ZVA_obj,1);   % Read terminating character LF
    pause(0.01)
end


s = size(data_complex_meas);
for m = 1:1:s(2)  
    i = 1;
    for n = 1:2:s(1)
       data_complex(i,m) = complex(data_complex_meas(n,m),data_complex_meas(n+1,m));
       i = i+1;
    end
end



% Get frequency
fprintf(ZVA_obj, 'CALC:MEAS:DATA:X?');
freq = binblockread(ZVA_obj, 'float');
fread(ZVA_obj,1);   % Read terminating character LF

N_traces = length(freq);

 end


# ####################################################################################################

 function [freq, traceData] = func_M9371A_getTrace(ZVA_obj, traceName)

% fprintf(ZVA_obj,'INIT');   
% %     pause(0.001)
% fprintf(ZVA_obj,'*OPC?');   
% %     pause(0.001)

%ZVA_obj.ByteOrder = 'littleEndian';
% Sets the data format for transferring measurement data and frequency data.
% fprintf(ZVA_obj,['FORM REAL,32']); 


% Get frequency
fprintf(ZVA_obj, 'CALC:MEAS:DATA:X?');
freq = binblockread(ZVA_obj, 'float');
fread(ZVA_obj,1);   % Read terminating character LF


% Get trace number
traceNum = str2double(regexp(traceName,'\d*','Match'));

fprintf(ZVA_obj, strcat('CALCulate:MEASure', num2str(traceNum), ':DATA:SDATA?'));
traceDataMeas = binblockread(ZVA_obj, 'float');
fread(ZVA_obj,1);   % Read terminating character LF

traceDataMeas = single(traceDataMeas);

traceData(length(freq)) = 0;
i = 1;
for n = 1:2:length(traceDataMeas)
   traceData(i) = complex(traceDataMeas(n),traceDataMeas(n+1));
   i = i+1;
end


if  length(traceData) ~= length(freq)
    error('Freq and Data vector do not match');
end


end

####################################################################################################
# Recal PNA Settings
'MMEM:LOAD:CSAR '''filename'.sta''

# ####################################################################################################
# Set Port Impedance
% fprintf(ZVA_obj,['LPOR' num2str(port_N) ':ZDIF ' num2str(real(port_Z_diff)) ', ' num2str(imag(port_Z_diff))]);
% fprintf(ZVA_obj,['LPOR' num2str(port_N) ':ZCOM ' num2str(real(port_Z_com)) ', ' num2str(imag(port_Z_com))]);

% Sets the Imag/Real part of the impedance value for the common port
% impedance converstion function
fprintf(ZVA_obj, ['CALC:FSIM:BAL:CZC:LPOR', num2str(port_N) , ':REAL ', num2str(real(port_Z_com))]);
fprintf(ZVA_obj, ['CALC:FSIM:BAL:CZC:LPOR', num2str(port_N) , ':IMAG ', num2str(imag(port_Z_com))]);

% Sets the Imag/Real part of the impedance value for the differntial part
% impedance conversion function
fprintf(ZVA_obj, ['CALC:FSIM:BAL:DZC:LPOR', num2str(port_N) , ':REAL ', num2str(real(port_Z_diff))]);
fprintf(ZVA_obj, ['CALC:FSIM:BAL:DZC:LPOR', num2str(port_N) , ':IMAG ', num2str(imag(port_Z_diff))]);

# ####################################################################################################
# SETPORTZ
% fprintf(ZVA_obj,['PORT' num2str(port_N) ':ZREF ' num2str(real(port_Z)) ',% ' num2str(imag(port_Z))]);  % R&S SCPI Command

% Turns all three fixturing functions (de-embedding, port matching, impedance conversion) ON 
%fprintf(ZVA_obj, 'CALC:FSIM:STAT 1');    

% Sets the complex impedance value for the single-ended port impedance conversion function.
fprintf(ZVA_obj, ['CALC:FSIM:SEND:ZCON:PORT' num2str(port_N) ':REAL ' num2str(real(port_Z))]);
fprintf(ZVA_obj, ['CALC:FSIM:SEND:ZCON:PORT' num2str(port_N) ':IMAG ' num2str(imag(port_Z))]);

%fprintf(ZVA_obj, strcat('CALC:FSIM:DRAF:ZCON:SEND:POR', num2str(port_N), ':COMPL ', num2str(real(port_Z)), ',', num2str(imag(port_Z))));

# ####################################################################################################

function [] = func_M9371A_setSweep(VNA_obj,freq_array,N_segments, freqPointsPerSegment, powerIndBm, measurementBandwidth, TRIGGER_MODE)
%FUNC_M9371A_SETSWEEP Summary of this function goes here
%   Detailed explanation goes here
        fprintf(VNA_obj,'*IDN?');                            % CLear Status, no query
        fread(VNA_obj);
        pause(0.1)
        fprintf(VNA_obj,'*CLS');                            % CLear Status, no query
        pause(0.1)
        
        %convert to char arrays
        powerIndBm = num2str(powerIndBm);
        freqPointsPerSegment = num2str(freqPointsPerSegment);
        measurementBandwidth = num2str(measurementBandwidth);
        if N_segments == 1
            freq11 = num2str(freq_array(1,1));
            freq12 = num2str(freq_array(1,2));
            %fprintf(VNA_obj,['FREQ:STAR ' freq11 'E+6; STOP ' freq12 'E+6']);
            fprintf(VNA_obj,['SENSe:FREQ:STAR ' freq11 'E+6']);
            fprintf(VNA_obj,['SENSe:FREQ:STOP ' freq12 'E+6']);
            fprintf(VNA_obj,'SENSe:SWE:TYPE LIN');
            fprintf(VNA_obj,['SENSe:SWEep:POINts ' freqPointsPerSegment ]);
            fprintf(VNA_obj,['SOUR:POW ' powerIndBm]);
        else %N_segments == 2
            freq11 = num2str(freq_array(1,1));
            freq12 = num2str(freq_array(1,2));
            freq21 = num2str(freq_array(2,1));
            freq22 = num2str(freq_array(2,2));
            % Deletes the specified sweep segment
            fprintf(VNA_obj,'SENS:SEGM:DEL');
            
            % R&S Command
            % fprintf(VNA_obj,['SEGM1:INS ' freq11 'MHZ, ' freq12 'MHZ, ' freqPointsPerSegment ', ' powerIndBm 'DBM, AUTO, 0, ' measurementBandwidth 'KHZ']);
            % fprintf(VNA_obj,['SEGM2:INS ' freq21 'MHZ, ' freq22 'MHZ, ' freqPointsPerSegment ', ' powerIndBm 'DBM, AUTO, 0, ' measurementBandwidth 'KHZ']);
        
            
            % Activate IFbandwidth, Dwell Time, Port Power for SEGM Controll
            fprintf(VNA_obj, 'SENSe:SEGMent:BWIDth:CONTrol ON');
            fprintf(VNA_obj, 'SENSe:SEGMent:SWEep:TIME:CONTrol ON');
            fprintf(VNA_obj, 'SENSe:SEGMent:POWer:CONTrol ON');
            % Turning off coupling allows power to vary per each port
            fprintf(VNA_obj, 'SOURce:POWer:COUPle OFF');
      
                  
            % writes the entire list of values in the segment sweep table
            Seg1 = strcat('1', ',', num2str(freqPointsPerSegment), ',', num2str(freq11), ' E+6,', num2str(freq12), ' E+6,', num2str(measurementBandwidth), ' E+3, 0,', num2str(powerIndBm), ',');
            Seg2 = strcat('1', ',', num2str(freqPointsPerSegment), ',', num2str(freq21), ' E+6,', num2str(freq22), ' E+6,', num2str(measurementBandwidth), ' E+3, 0,', num2str(powerIndBm));
            
            %Seg1 = strcat('1', ',', num2str(freqPointsPerSegment), ',', num2str(freq11), ' E+6,', num2str(freq12), ' E+6,');
            %Seg2 = strcat('1', ',', num2str(freqPointsPerSegment), ',', num2str(freq21), ' E+6,', num2str(freq22), ' E+6');
            fprintf(VNA_obj, strcat('SENSe:SEGMent:LIST SSTOP,2,', Seg1, Seg2));
           
           
            % Set segment sweep type on Channel 1
            fprintf(VNA_obj,'SENSe:SWE:TYPE SEGM');
            
            % Having the VNA display the segment sweep table for the channel
            fprintf(VNA_obj, 'DISPlay:WINDow1:TABLe SEGMent');
            
        end
        % Frequenzbereich einstellen
        pause(0.12)
                     
        % fprintf(VNA_obj,'SYSTEM:DISPLAY:UPDATE ON');  % Switches the display on or off while the analyzer is in the remote state.
        fprintf(VNA_obj,'DISP:ENAB ON');  % Switches the display on or off while the analyzer is in the remote state.
        
        
        
        
        % fprintf(VNA_obj,['CALC:TRAN:IMP:RNOR PWAV']); %Renormalization of port impedances: power waves theory
        
        
        
        fprintf(VNA_obj,'TRIG:SOUR IMM'); %Free running Trigger
        pause(1)
        
        if TRIGGER_MODE == 1
            fprintf(VNA_obj,'TRIG:SOUR EXT'); %External Trigger
            fprintf(VNA_obj,'TRIG:SLOP POS'); %positive slope
            %Output of Trigger after Sweep
            fprintf(VNA_obj,['TRIG:CHAN:AUX:ENAB ON']); %enable output trigger
            fprintf(VNA_obj,['TRIG:CHAN:AUX:DUR 10 us']); %duration
            fprintf(VNA_obj,['TRIG:CHAN:AUX:POS AFT']); %Trigger after Sweep
            fprintf(VNA_obj,['TRIG:CHAN:AUX:INT SWE']); %trigger each sweep
            fprintf(VNA_obj,['TRIG:CHAN:AUX:OPOL POS']); %positive trigger
        else
            fprintf(VNA_obj,['TRIG:SOUR IMM']); %Free running Trigger

        end
        


# ####################################################################################################
function [] = func_M9371A_setTraces(ZVA_obj,traces_array)
%FUNC_M9371A_SETTRACES Summary of this function goes here
%   Detailed explanation goes here

%func_M9371A_deleteTraces(ZVA_obj)

for n=1:length(traces_array)
    % Creates a trace and assigns a channel number, a name and a measurement parameter to it.
    fprintf(ZVA_obj, strcat("CALCulate1:PARameter:DEFine:EXTended 'TRC" , num2str(n) , "', S" , num2str(traces_array(n)) , ""));
    
    % Log Mag Select View
    fprintf(ZVA_obj,["CALCulate1:FORMat MLOG"]);    
    
    % create window
    fprintf(ZVA_obj,["DISPlay:WINDow1:STATe ON"]);  

    % display Measurement
    fprintf(ZVA_obj,strcat("DISPlay:WINDow1:TRACe", num2str(n) ,":FEED 'TRC" , num2str(n) ,"'"));  

    pause(0.1)
end
pause(0.1)
end

####################################################################################################
%% M9371A
clc, clear, instrreset, close all

% M9371A Setup
M9371A_power = -5;%0; %dBm  prev: 10dBm

Visa_Adress = 'TCPIP0::Localhost::hislip2::INSTR';
VNA_obj = func_M9371A_init(Visa_Adress);
ZVA_obj = VNA_obj;

% Delete Old Traces
func_M9371A_deleteTraces(VNA_obj);

freq_vec_full = (500:1000)*1e6; %for final plot
freq_array_final = [freq_vec_full(1) freq_vec_full(end)]/1e6; % frequencies in MHz

N_segments_final = 1;

freqPointsPerSegment_final = length(freq_vec_full);
measurementBandwidth = 10;% in kHz
TRIGGER_MODE = 0;


% Set Sweep
func_M9371A_setSweep(VNA_obj,freq_array_final,N_segments_final, freqPointsPerSegment_final, M9371A_power,measurementBandwidth, TRIGGER_MODE)


%all ports to 50 Ohm
func_M9371A_setPortZ(VNA_obj ,1 , 50)
func_M9371A_setPortZ(VNA_obj ,2 , 50)

traces_array_allSparams = [11 12 21 22];
func_M9371A_setTraces(VNA_obj,traces_array_allSparams)


%func_M9371A_setLogicalPortZ(VNA_obj, 1, 10+i*10, 20+i*20)


% Read Data
%[freq,data3, N_traces] = func_M9371A_getComplexData(VNA_obj);


% Sets the data format for transferring measurement data and frequency data.
fprintf(ZVA_obj,['FORM REAL,32']); 

[freq_1, traceData_1] = func_M9371A_getTrace(ZVA_obj, 'TRC1');
[freq_2, traceData_2] = func_M9371A_getTrace(ZVA_obj, 'TRC4');
figure
plot(freq_1,20*log10(abs(traceData_1)))
hold on
plot(freq_2,20*log10(abs(traceData_2)))




[freq, data_complex, N_traces] = func_M9371A_getComplexData(ZVA_obj);

figure
plot(freq,20*log10(abs(data_complex(:,1)))) % S11
hold on
plot(freq,20*log10(abs(data_complex(:,2)))) % S21
hold on
plot(freq,20*log10(abs(data_complex(:,3)))) % S12
hold on 
plot(freq,20*log10(abs(data_complex(:,4)))) % S22
legend('S11', 'S21', 'S12', 'S22')


# ####################################################################################################

 function [freq, data_complex, N_traces, traceNames] = func_M9801A_getComplexData(ZVA_obj)

% changes the state of each channel to the initiation state in the trigger system
% fprintf(ZVA_obj,'INIT');   
% pause(0.001)

% Returns an ASCII "+1" when all pending overlapped operations have been completed
% fprintf(ZVA_obj,'*OPC?');   
% pause(0.001)

% Sets the data format for transferring measurement data and frequency data.
%fprintf(ZVA_obj,['FORM REAL,32']); 


fprintf(ZVA_obj,['format:data ascii']); 
fprintf(ZVA_obj, ['CALC:PAR:CAT:EXT? DEF']);
%read_traceNames = binblockread(ZVA_obj, 'float');
read_traceNames = fscanf(ZVA_obj);
%fread(ZVA_obj,1);   % Read terminating character LF

pause(0.1)

fprintf(ZVA_obj,['FORM REAL,32']); 




% get Trace Names
read_traceNames = convertCharsToStrings(read_traceNames);
read_traceNames = erase(read_traceNames,'"');
read_traceNames = regexp(read_traceNames, ',', 'split');

i = 1;
for n = 1:2:length(read_traceNames)
    traceNames(i) = read_traceNames(n);
    i = i+1;
end


% Get Trace Numbers
for n = 1:1:length(traceNames)
    % Get trace number
    numbers =  str2double(regexp(string(traceNames(n)),'\d*','Match'));
    traceNum(n) = numbers(end);
end


% Read selected Traces
for i=1:1:length(traceNum)
    fprintf(ZVA_obj, strcat('CALCulate:MEASure', num2str(traceNum(i)), ':DATA:SDATA?'));
    data_complex_meas(:,i) = binblockread(ZVA_obj, 'float');
    fread(ZVA_obj,1);   % Read terminating character LF
    pause(0.01)
end


s = size(data_complex_meas);
for m = 1:1:s(2)  
    i = 1;
    for n = 1:2:s(1)
       data_complex(i,m) = complex(data_complex_meas(n,m),data_complex_meas(n+1,m));
       i = i+1;
    end
end



% Get frequency
fprintf(ZVA_obj, 'CALC:MEAS:DATA:X?');
freq = binblockread(ZVA_obj, 'float');
fread(ZVA_obj,1);   % Read terminating character LF

N_traces = s(2);

end

# ####################################################################################################

 function [freq, traceData] = func_M9801A_getTrace(ZVA_obj, traceName)

% fprintf(ZVA_obj,'INIT');   
% %     pause(0.001)
% fprintf(ZVA_obj,'*OPC?');   
% %     pause(0.001)

%ZVA_obj.ByteOrder = 'littleEndian';
% Sets the data format for transferring measurement data and frequency data.
% fprintf(ZVA_obj,['FORM REAL,32']); 

% Get frequency
fprintf(ZVA_obj, 'CALC:MEAS:DATA:X?');
freq = binblockread(ZVA_obj, 'float');
fread(ZVA_obj,1);   % Read terminating character LF


% Get trace number
traceNum = str2double(regexp(traceName,'\d*','Match'));

fprintf(ZVA_obj, strcat('CALCulate:MEASure', num2str(traceNum), ':DATA:SDATA?'));
traceDataMeas = binblockread(ZVA_obj, 'float');
fread(ZVA_obj,1);   % Read terminating character LF

traceDataMeas = single(traceDataMeas);

traceData(length(freq)) = 0;
i = 1;
for n = 1:2:length(traceDataMeas)
   traceData(i) = complex(traceDataMeas(n),traceDataMeas(n+1));
   i = i+1;
end


if  length(traceData) ~= length(freq)
    error('Freq and Data vector do not match');
end


end

# ####################################################################################################

function [] = func_M9801A_setLogicalPortZ(ZVA_obj ,port_N , port_Z_diff, port_Z_com)
%FUNC_M9801A_SETPORTZ Summary of this function goes here
%   Detailed explanation goes here

% 
% fprintf(ZVA_obj,['LPOR' num2str(port_N) ':ZDIF ' num2str(real(port_Z_diff)) ', ' num2str(imag(port_Z_diff))]);
% fprintf(ZVA_obj,['LPOR' num2str(port_N) ':ZCOM ' num2str(real(port_Z_com)) ', ' num2str(imag(port_Z_com))]);


% Sets the Imag/Real part of the impedance value for the common port
% impedance converstion function
fprintf(ZVA_obj, ['CALC:FSIM:BAL:CZC:LPOR', num2str(port_N) , ':REAL ', num2str(real(port_Z_com))]);
fprintf(ZVA_obj, ['CALC:FSIM:BAL:CZC:LPOR', num2str(port_N) , ':IMAG ', num2str(imag(port_Z_com))]);


% Sets the Imag/Real part of the impedance value for the differntial part
% impedance conversion function
fprintf(ZVA_obj, ['CALC:FSIM:BAL:DZC:LPOR', num2str(port_N) , ':REAL ', num2str(real(port_Z_diff))]);
fprintf(ZVA_obj, ['CALC:FSIM:BAL:DZC:LPOR', num2str(port_N) , ':IMAG ', num2str(imag(port_Z_diff))]);

end

# ####################################################################################################
function [] = func_M9801A_setPortZ(ZVA_obj ,port_N , port_Z)
%FUNC_M9801A_SETPORTZ Summary of this function goes here
%   Detailed explanation goes here

% fprintf(ZVA_obj,['PORT' num2str(port_N) ':ZREF ' num2str(real(port_Z)) ',% ' num2str(imag(port_Z))]);  % R&S SCPI Command

% Turns all three fixturing functions (de-embedding, port matching, impedance conversion) ON 
%fprintf(ZVA_obj, 'CALC:FSIM:STAT 1');    

% Sets the complex impedance value for the single-ended port impedance conversion function.
fprintf(ZVA_obj, ['CALC:FSIM:SEND:ZCON:PORT' num2str(port_N) ':REAL ' num2str(real(port_Z))]);
fprintf(ZVA_obj, ['CALC:FSIM:SEND:ZCON:PORT' num2str(port_N) ':IMAG ' num2str(imag(port_Z))]);

end


# ####################################################################################################
function [] = func_M9801A_setSweep(VNA_obj,freq_array,N_segments, freqPointsPerSegment, powerIndBm, measurementBandwidth, TRIGGER_MODE)
%FUNC_M9371A_SETSWEEP Summary of this function goes here
%   Detailed explanation goes here
        fprintf(VNA_obj,'*IDN?');                            % CLear Status, no query
        fread(VNA_obj);
        pause(0.1)
        fprintf(VNA_obj,'*CLS');                            % CLear Status, no query
        pause(0.1)
        
        %convert to char arrays
        powerIndBm = num2str(powerIndBm);
        freqPointsPerSegment = num2str(freqPointsPerSegment);
        measurementBandwidth = num2str(measurementBandwidth);
        if N_segments == 1
            freq11 = num2str(freq_array(1,1));
            freq12 = num2str(freq_array(1,2));
            %fprintf(VNA_obj,['FREQ:STAR ' freq11 'E+6; STOP ' freq12 'E+6']);
            fprintf(VNA_obj,['SENSe:FREQ:STAR ' freq11 'E+6']);
            fprintf(VNA_obj,['SENSe:FREQ:STOP ' freq12 'E+6']);
            fprintf(VNA_obj,'SENSe:SWE:TYPE LIN');
            fprintf(VNA_obj,['SENSe:SWEep:POINts ' freqPointsPerSegment ]);
            fprintf(VNA_obj,['SOUR:POW ' powerIndBm]);
        else %N_segments == 2
            freq11 = num2str(freq_array(1,1));
            freq12 = num2str(freq_array(1,2));
            freq21 = num2str(freq_array(2,1));
            freq22 = num2str(freq_array(2,2));
            % Deletes the specified sweep segment
            fprintf(VNA_obj,'SENS:SEGM:DEL');
            
            % R&S Command
            % fprintf(VNA_obj,['SEGM1:INS ' freq11 'MHZ, ' freq12 'MHZ, ' freqPointsPerSegment ', ' powerIndBm 'DBM, AUTO, 0, ' measurementBandwidth 'KHZ']);
            % fprintf(VNA_obj,['SEGM2:INS ' freq21 'MHZ, ' freq22 'MHZ, ' freqPointsPerSegment ', ' powerIndBm 'DBM, AUTO, 0, ' measurementBandwidth 'KHZ']);
        
            
            % Activate IFbandwidth, Dwell Time, Port Power for SEGM Controll
            fprintf(VNA_obj, 'SENSe:SEGMent:BWIDth:CONTrol ON');
            fprintf(VNA_obj, 'SENSe:SEGMent:SWEep:TIME:CONTrol ON');
            fprintf(VNA_obj, 'SENSe:SEGMent:POWer:CONTrol ON');
            % Turning off coupling allows power to vary per each port
            fprintf(VNA_obj, 'SOURce:POWer:COUPle OFF');
      
                  
            % writes the entire list of values in the segment sweep table
            Seg1 = strcat('1', ',', num2str(freqPointsPerSegment), ',', num2str(freq11), ' E+6,', num2str(freq12), ' E+6,', num2str(measurementBandwidth), ' E+3, 0,', num2str(powerIndBm), ',');
            Seg2 = strcat('1', ',', num2str(freqPointsPerSegment), ',', num2str(freq21), ' E+6,', num2str(freq22), ' E+6,', num2str(measurementBandwidth), ' E+3, 0,', num2str(powerIndBm));
            
            %Seg1 = strcat('1', ',', num2str(freqPointsPerSegment), ',', num2str(freq11), ' E+6,', num2str(freq12), ' E+6,');
            %Seg2 = strcat('1', ',', num2str(freqPointsPerSegment), ',', num2str(freq21), ' E+6,', num2str(freq22), ' E+6');
            fprintf(VNA_obj, strcat('SENSe:SEGMent:LIST SSTOP,2,', Seg1, Seg2));
           
           
            % Set segment sweep type on Channel 1
            fprintf(VNA_obj,'SENSe:SWE:TYPE SEGM');
            
            % Having the VNA display the segment sweep table for the channel
            fprintf(VNA_obj, 'DISPlay:WINDow1:TABLe SEGMent');
            
        end
        % Frequenzbereich einstellen
        pause(0.12)
                     
        % fprintf(VNA_obj,'SYSTEM:DISPLAY:UPDATE ON');  % Switches the display on or off while the analyzer is in the remote state.
        fprintf(VNA_obj,'DISP:ENAB ON');  % Switches the display on or off while the analyzer is in the remote state.
        
        
        
        
        % fprintf(VNA_obj,['CALC:TRAN:IMP:RNOR PWAV']); %Renormalization of port impedances: power waves theory
        
        
        
        fprintf(VNA_obj,'TRIG:SOUR IMM'); %Free running Trigger
        pause(1)
        
        if TRIGGER_MODE == 1
            fprintf(VNA_obj,'TRIG:SOUR EXT'); %External Trigger
            fprintf(VNA_obj,'TRIG:SLOP POS'); %positive slope
            %Output of Trigger after Sweep
            fprintf(VNA_obj,['TRIG:CHAN:AUX:ENAB ON']); %enable output trigger
            fprintf(VNA_obj,['TRIG:CHAN:AUX:DUR 10 us']); %duration
            fprintf(VNA_obj,['TRIG:CHAN:AUX:POS AFT']); %Trigger after Sweep
            fprintf(VNA_obj,['TRIG:CHAN:AUX:INT SWE']); %trigger each sweep
            fprintf(VNA_obj,['TRIG:CHAN:AUX:OPOL POS']); %positive trigger
        else
            fprintf(VNA_obj,['TRIG:SOUR IMM']); %Free running Trigger

        end
        
        
end

####################################################################################################
function [] = func_M9801A_setTraces(ZVA_obj,traces_array)
%FUNC_M9801A_SETTRACES Summary of this function goes here
%   Detailed explanation goes here


for n=1:length(traces_array)
    % Creates a trace and assigns a channel number, a name and a measurement parameter to it.
    fprintf(ZVA_obj, strcat("CALCulate1:PARameter:DEFine:EXTended 'TRC" , num2str(n) , "', S" , num2str(traces_array(n)) , ""));
    
    % Log Mag Select View
    fprintf(ZVA_obj,["CALCulate1:FORMat MLOG"]);    
    
    % create window
    fprintf(ZVA_obj,["DISPlay:WINDow1:STATe ON"]);  

    % display Measurement
    fprintf(ZVA_obj,strcat("DISPlay:WINDow1:TRACe", num2str(n) ,":FEED 'TRC" , num2str(n) ,"'"));  

    pause(0.1)
end
pause(0.1)
end