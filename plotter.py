import numpy as np
import matplotlib.pyplot as plt
from database_functions import *

from argparse import ArgumentParser

parser = ArgumentParser(prog = 'Pulse Waveform Database Plotter', description='This is a plotter for the Pulse Waveform Database')
parser.add_argument('-i', '--input-data',type=str, nargs='+', help='The set of data file(s) (which file you want to use)')
parser.add_argument('-p', '--pmt-used', type=str, nargs=1, help='The PMT that was used for the data set')
parser.add_argument('-s', '--scintillator', type=str, nargs=1, help='The scintillator that was used for the data set')
parser.add_argument('-z', '--show', action='store_true', help='To show or not show all individual waveforms as an overlay')
parser.add_argument('-o', '--output-file-name', help='The name of Average Waveform output file name for saving purposes')


args = parser.parse_args()

if args.input_data is None:
	parser.error('No data specified. . . Please specify the data file to be run')

showall = True
if args.show:
	showall = True
if not args.show:
    showall = False

varray = []	
psdarray = []
#varray2 = []	
#psdarray2 = []
va = -1
va2 = -1

energy_array = []
#energy2_array = []

c1 = 'lightblue'
c2 = 'red'
ac1 = 'orangered'
ac2 = 'purple'

for input_file in range(len(args.input_data)):

    path = '{}'.format(args.input_data[input_file])
        
    f = open(path)
    data = f.readlines()

    voltage = []
    time = []
    for line in data:
	    split_line = line.split(' ')
	    if len(split_line) > 1:
       		time.append(float(split_line[0]))
	        voltage.append(float(split_line[1]))

    energy = (float(time[0]))
    psd = (float(voltage[0]))
    time = np.delete(time, 0, 0)
    voltage = np.delete(voltage, 0, 0)

    #print("PSD: ",psd," ENERGY: ",energy)

    for b in range(len(voltage)):				#Automates size of varray for Average voltage values (Avarray)
        if va < 0:
            varray.append(voltage[b])
        if va >= 0:
            varray[b] += voltage[b]
    energy_array.append(energy)			#Appends energy to array of all energies

    psdarray.append(psd)

		##########Graphing/Plots
    if showall is True:
        
        plt.plot(time, voltage, alpha=0.1, color=c1)

    va +=1

Avarray = []
Current = []
for val in varray:
	Avarray.append(val/len(args.input_data))
	Current.append(val/50)		

d = np.array([time,Avarray])
d = d.T
np.savetxt('data/{}/{}/{}_Average_Waveform.txt'.format(args.pmt_used[0], args.scintillator[0], args.output_file_name), d, delimiter=';')  

##########Returns/Printing for Set 1
#print(psdarray)
print("Super-Set PSD Average: " ,Average(psdarray)) #returns PSD average for cut 1

print("Area under the curve of Super-Set 1: " ,Area_under_Curve(Current, time), "Coulombs")

print("Rise Time for Super-Set 1: ",Rise_Time(Avarray, time), " seconds")	#returns rise time (between 5% and peak voltage)
print("Fall Time for Super-Set 1: ",Fall_Time(Avarray, time), " seconds")

print("The T90 for Super-Set 1: ",T90(Avarray, time)[0], "seconds")
#print("T90 Check: ",t90(Avarray,time))
#print("Original T90 Method: ",t_90(Avarray, time)[0])

##########Graphing for Set 1

#plt.subplot(1,4,1)						#Plots average voltage v. time
plt.plot(time, Avarray, label='Super-Set 1 Average Curve')#,label='PSD Average: %.6e\nAuC: %.6e\nRise Time: %.6e\nFall Time: %.6e\nAverage T90: %.4e'%(Average(psdarray),Area_under_Curve(Current, time),Rise_Time(Avarray, time),Fall_Time(Avarray, time),T90(Avarray, time)[0]))
plt.xlabel(r"Time [s]")
plt.ylabel("Amplitude [V]")
plt.title("Amplitude v. Time")

##These Plot Markers for the T90 of the averaged curve##
plt.plot(time[T90(Avarray, time)[1]], Avarray[T90(Avarray, time)[1]], marker=">", markersize=7, markeredgecolor="black", markerfacecolor="yellow", label="Super-Set T90 Start")
plt.plot(time[T90(Avarray, time)[2]], Avarray[T90(Avarray, time)[2]], marker="<", markersize=7, markeredgecolor="black", markerfacecolor="yellow", label="Super-Set T90 End")

plt.legend()
plt.show()
