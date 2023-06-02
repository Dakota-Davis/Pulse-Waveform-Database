import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.signal import lfilter
import scipy.signal as signal
from database_functions import *

path = 'data/hamamatsu_r5800/scionix_2_naitl_co60_1173kev/Average_Waveform.txt'
        
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

plt.plot(time, voltage, c='blue')


path2 = 'data/hamamatsu_r5800/scionix_2_naitl_co60_1332kev/Average_Waveform.txt'
        
f = open(path2)
data = f.readlines()

voltage2 = []
time2 = []
for line in data:
    split_line = line.split(';')
    if len(split_line) > 1:
        time2.append(float(split_line[0]))
        voltage2.append(float(split_line[1]))
f.close()
       
plt.plot(time2, voltage2,c='red')

path3 = 'data/hamamatsu_r5800/scionix_2_csina_co60_1332kev/Average_Waveform.txt'
        
f = open(path3)
data = f.readlines()

voltage3 = []
time3 = []
for line in data:
    split_line = line.split(';')
    if len(split_line) > 1:
        time3.append(float(split_line[0]))
        voltage3.append(float(split_line[1]))
f.close()
       
plt.plot(time3, voltage3,c='green')
plt.axhline(y=-0.1, c='black', linestyle='-')


plt.xlabel(r"Time [s]")
plt.ylabel("Amplitude [V]")
plt.title("Amplitude v. Time")
plt.show()
