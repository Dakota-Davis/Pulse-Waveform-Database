import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.signal import lfilter
import scipy.signal as signal
from database_functions import *


plt.rcParams['font.size'] = 32 #change font size
plt.rcParams["legend.loc"] = 'lower right' #change legend location
plt.rcParams['figure.constrained_layout.use'] = True
ax = plt.gca()
start, end = ax.get_ylim()
ax.yaxis.set_ticks(np.arange(0, -0.7, -0.1)) #set y-axis start & end & step interval

#plt.subplot(1,2,1) 

path = 'data/hamamatsu_r12699/scionix_naitl_csina/88kev_naitl_Average_Waveform.txt'
        
f = open(path)
data = f.readlines()

voltage = []
time = []
for line in data:
    split_line = line.split(';')
    if len(split_line) > 1:
        time.append(float(split_line[0])/1e-6)
        voltage.append(float(split_line[1]))
        
f.close()

plt.plot(time, voltage, c='darkblue', label='88kev')

path = 'data/hamamatsu_r12699/scionix_naitl_csina/662kev_naitl_Average_Waveform.txt'
        
f = open(path)
data = f.readlines()

voltage = []
time = []
for line in data:
    split_line = line.split(';')
    if len(split_line) > 1:
        time.append(float(split_line[0])/1e-6)
        voltage.append(float(split_line[1]))
        
f.close()

plt.plot(time, voltage, c='blue',label='662kev')


path = 'data/hamamatsu_r12699/scionix_naitl_csina/1332kev_naitl_Average_Waveform.txt'
        
f = open(path)
data = f.readlines()

voltage= []
time = []
for line in data:
    split_line = line.split(';')
    if len(split_line) > 1:
        time.append(float(split_line[0])/1e-6)
        voltage.append(float(split_line[1]))
f.close()
       
plt.plot(time, voltage, c='cornflowerblue', label='1332kev')

#plt.axhline(y=-0.1, c='black', linestyle='-')
plt.xlabel(r"Time [$\mu$s]")
plt.ylabel("Amplitude [V]")
#plt.title("Amplitude v. Time [NaI(Tl)]")
plt.legend()
plt.ylim(top=0.01,bottom=-0.7)
plt.xlim(0,10)
#plt.tight_layout(pad=0)

plt.show()

#plt.subplot(1,2,2) 

ax = plt.gca()
start, end = ax.get_ylim()
ax.yaxis.set_ticks(np.arange(0, -0.7, -0.1))

path = 'data/hamamatsu_r12699/scionix_naitl_csina/88kev_csina_Average_Waveform.txt'
        
f = open(path)
data = f.readlines()

voltage = []
time = []
for line in data:
    split_line = line.split(';')
    if len(split_line) > 1:
        time.append(float(split_line[0])/1e-6)
        voltage.append(float(split_line[1]))
        
f.close()

plt.plot(time, voltage, c='firebrick', label='88kev')

path = 'data/hamamatsu_r12699/scionix_naitl_csina/662kev_csina_Average_Waveform.txt'
        
f = open(path)
data = f.readlines()

voltage = []
time = []
for line in data:
    split_line = line.split(';')
    if len(split_line) > 1:
        time.append(float(split_line[0])/1e-6)
        voltage.append(float(split_line[1]))
        
f.close()

plt.plot(time, voltage, c='red', label='662kev')


path = 'data/hamamatsu_r12699/scionix_naitl_csina/1332kev_csina_Average_Waveform.txt'
        
f = open(path)
data = f.readlines()

voltage= []
time = []
for line in data:
    split_line = line.split(';')
    if len(split_line) > 1:
        time.append(float(split_line[0])/1e-6)
        voltage.append(float(split_line[1]))
f.close()
       
plt.plot(time, voltage, c='lightsalmon', label='1332kev')

#plt.axhline(y=-0.1, c='black', linestyle='-')
plt.xlabel(r"Time [$\mu$s]")
plt.ylabel("Amplitude [V]")
#plt.title("Amplitude v. Time [CsI(Na)]")
plt.legend()
plt.ylim(top=0.01,bottom=-0.7)
plt.xlim(0,10)
#plt.tight_layout(pad=0)

plt.show()

"""
#START ENERGY GATES PLOT
ax = plt.gca()
start, end = ax.get_ylim()
ax.yaxis.set_ticks(np.arange(0.25, -0.25, -0.05)) #set y-axis start & end & step interval

path = 'data/hamamatsu_r12699/scionix_naitl_csina/1332kev_naitl_Average_Waveform.txt'
        
f = open(path)
data = f.readlines()

voltage= []
time = []
for line in data:
    split_line = line.split(';')
    if len(split_line) > 1:
        time.append(float(split_line[0])/1e-6)
        voltage.append(float(split_line[1]))
f.close()
       
plt.plot(time, voltage, c='cornflowerblue', label='Input')


plt.axhline(y=0.0, c='black', linestyle='-')
plt.axvline(x=0.73, c='black', linestyle='dashed')

x = [0,0.73,0.73,1.73,1.73,5]           #long gate
y = [0.1,0.1,0.125,0.125,0.1,0.1]
plt.plot(x,y, c='red', label='Long Gate')
x = [0,0.73,0.73,1.03,1.03,5]           #short gate
y = [0.05,0.05,0.075,0.075,0.05,0.05]
plt.plot(x,y, c='limegreen', label='Short Gate')

plt.xlabel(r"Time [$\mu$s]")
plt.ylabel("Amplitude [V]")
#plt.title("Amplitude v. Time [NaI(Tl)]")
plt.legend()
plt.ylim(top=0.15,bottom=-0.22)
plt.xlim(0,5)

plt.show()
"""