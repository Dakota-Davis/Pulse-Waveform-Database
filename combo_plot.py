import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.signal import lfilter
import scipy.signal as signal
from database_functions import *


#plt.subplot(1,2,1) 

path = 'data/hamamatsu_r5800/scionix_naitl_csina/88kev_naitl_Average_Waveform.txt'
        
f = open(path)
data = f.readlines()

voltage = []
time = []
for line in data:
    split_line = line.split(';')
    if len(split_line) > 1:
        time.append(float(split_line[0]))
        voltage.append(float(split_line[1]))
        
f.close()

plt.plot(time, voltage, c='darkblue', label='88kev')

path = 'data/hamamatsu_r5800/scionix_naitl_csina/662kev_naitl_Average_Waveform.txt'
        
f = open(path)
data = f.readlines()

voltage = []
time = []
for line in data:
    split_line = line.split(';')
    if len(split_line) > 1:
        time.append(float(split_line[0]))
        voltage.append(float(split_line[1]))
        
f.close()

plt.plot(time, voltage, c='blue',label='662kev')


path = 'data/hamamatsu_r5800/scionix_naitl_csina/1332kev_naitl_Average_Waveform.txt'
        
f = open(path)
data = f.readlines()

voltage= []
time = []
for line in data:
    split_line = line.split(';')
    if len(split_line) > 1:
        time.append(float(split_line[0]))
        voltage.append(float(split_line[1]))
f.close()
       
plt.plot(time, voltage, c='cornflowerblue', label='1332kev')

plt.axhline(y=-0.1, c='black', linestyle='-')
plt.xlabel(r"Time [s]")
plt.ylabel("Amplitude [V]")
plt.title("Amplitude v. Time [NaI(Tl)]")
plt.legend()
plt.ylim(bottom=-0.22)
plt.show()

#plt.subplot(1,2,2) 

path = 'data/hamamatsu_r5800/scionix_naitl_csina/88kev_csina_Average_Waveform.txt'
        
f = open(path)
data = f.readlines()

voltage = []
time = []
for line in data:
    split_line = line.split(';')
    if len(split_line) > 1:
        time.append(float(split_line[0]))
        voltage.append(float(split_line[1]))
        
f.close()

plt.plot(time, voltage, c='firebrick', label='88kev')

path = 'data/hamamatsu_r5800/scionix_naitl_csina/662kev_csina_Average_Waveform.txt'
        
f = open(path)
data = f.readlines()

voltage = []
time = []
for line in data:
    split_line = line.split(';')
    if len(split_line) > 1:
        time.append(float(split_line[0]))
        voltage.append(float(split_line[1]))
        
f.close()

plt.plot(time, voltage, c='red', label='662kev')


path = 'data/hamamatsu_r5800/scionix_naitl_csina/1332kev_csina_Average_Waveform.txt'
        
f = open(path)
data = f.readlines()

voltage= []
time = []
for line in data:
    split_line = line.split(';')
    if len(split_line) > 1:
        time.append(float(split_line[0]))
        voltage.append(float(split_line[1]))
f.close()
       
plt.plot(time, voltage, c='lightsalmon', label='1332kev')

plt.axhline(y=-0.1, c='black', linestyle='-')
plt.xlabel(r"Time [s]")
plt.ylabel("Amplitude [V]")
plt.title("Amplitude v. Time [CsI(Na)]")
plt.legend()
plt.ylim(bottom=-0.22)
plt.show()
