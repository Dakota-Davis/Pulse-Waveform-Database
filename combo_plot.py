import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.signal import lfilter
import scipy.signal as signal
from database_functions import *


plt.subplot(1,2,1) 

path = 'data/hamamatsu_r5800/scionix_naitl_csina/co60_1173kev_Average_Waveform.txt'
        
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

plt.plot(time, voltage, c='blue', label='1173kev')


path2 = 'data/hamamatsu_r5800/scionix_naitl_csina/co60_1332kev_Average_Waveform.txt'
        
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
       
plt.plot(time2, voltage2,c='red', label='1332kev')
plt.axhline(y=-0.1, c='black', linestyle='-')

plt.xlabel(r"Time [s]")
plt.ylabel("Amplitude [V]")
plt.title("Amplitude v. Time [NaI(Tl)]")
plt.legend()
#plt.show()

plt.subplot(1,2,2) 

path3 = 'data/hamamatsu_r5800/scionix_naitl_csina/co60_1173kev_csina_Average_Waveform.txt'
        
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
       
plt.plot(time3, voltage3, label='1173kev')
#plt.axhline(y=-0.1, c='black', linestyle='-')
#plt.show()

path4 = 'data/hamamatsu_r5800/scionix_naitl_csina/co60_1332kev_csina_Average_Waveform.txt'
        
f = open(path4)
data = f.readlines()

voltage4 = []
time4 = []
for line in data:
    split_line = line.split(';')
    if len(split_line) > 1:
        time4.append(float(split_line[0]))
        voltage4.append(float(split_line[1]))
f.close()
       
plt.plot(time4, voltage4, c='green', label='1332kev')
plt.axhline(y=-0.1, c='black', linestyle='-')


plt.xlabel(r"Time [s]")
plt.ylabel("Amplitude [V]")
plt.title("Amplitude v. Time [CsI(Na)]")
plt.legend()
plt.show()
