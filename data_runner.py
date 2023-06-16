import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.signal import lfilter
import scipy.signal as signal
from database_functions import *

from argparse import ArgumentParser

parser = ArgumentParser(prog = 'Pulse Waveform Database Data Runner', description='This is a data runner for the Pulse Waveform Database')
#below arg is not really used, remove and update code accordingly
parser.add_argument('-n', '--number-of-scintillators', type=int, nargs=1, help='The number of scintillators used in the test')
parser.add_argument('-f', '--first-input-data',type=str, nargs='+', help='The first set of data file(s) (which file you want to use)')
#parser.add_argument('-sid', '--second-input-data',type=str, nargs='+', help='The second set of data file(s) (which file you want to use)')
parser.add_argument('-p', '--pmt-used', type=str, nargs='*', help='The PMT that was used for the data set')
parser.add_argument('-s', '--scintillator', type=str, nargs='*', help='The scintillator that was used for the data set')
#below arg is not really used, remove and update coda accordingly
parser.add_argument('-l', '--histogram-xlimit', type=int, nargs=2, help='The minimum and maximum x-limit for the energy histogram')
parser.add_argument('-z', '--show', action='store_true', help='To show or not show all individual waveforms as an overlay')
parser.add_argument('-o', '--output-file-name', help='The name of Average Waveform output file name for saving purposes')


args = parser.parse_args()

if args.first_input_data is None:
	parser.error('No data specified. . . Please specify the data file to be run')

if args.number_of_scintillators is None:
	parser.error('No scintillators specified. . . Please specify the number of scintillators used')
if args.number_of_scintillators is not None:
		if args.number_of_scintillators[0] not in (1,2):
			parser.error('Too many scintillators specified. . . Please specify a value between 1 and 2')

if args.histogram_xlimit is not None and len(args.histogram_xlimit) != 2:
	parser.error('Incorrect number of histogram x-limits specified. . . Please specify 2 x-limits')
    
if args.number_of_scintillators[0] == 1:
		if len(args.pmt_used) == 2:
			parser.error('Too many PMTs specified. . . Only 1 scintillator specified, please match PMTs accordingly')
		if len(args.scintillator) == 2:
			parser.error('Too many scintillators specified. . . Only 1 scintillator specified, please match PMTs accordingly')

if args.pmt_used is None:
	parser.error('No PMT specified. . . Please specify the PMT(s) used')
if args.pmt_used is not None:
		if len(args.pmt_used) not in (1,2):
			parser.error('Too many PMTs specified. . . Please specify a value between 1 and 2')

if args.scintillator is None:
	parser.error('No scintillator(s) specified. . . Please specify the scintillator(s) used')
if args.scintillator is not None:
		if len(args.scintillator) not in (1,2):
			parser.error('Too many scintillators specified. . . Please specify a value between 1 and 2')

if args.histogram_xlimit is None:			#Sets energy histogram limits
	hist_minxlim = 0
	hist_maxxlim = 1000
if args.histogram_xlimit is not None and len(args.histogram_xlimit) == 2:
	hist_minxlim = args.histogram_xlimit[0]
	hist_maxxlim = args.histogram_xlimit[1]

showall = True
if args.show:
	showall = True
if not args.show:
	#if args.show[0] == 'NONE':
    showall = False
	#if args.show[0] == 'ALL':
	#	showall = True
	#if args.show[0] != 'ALL' and args.show[0] != 'NONE':
    #parser.error('Choose to show [ALL] individual waveforms or [NONE] of them')

varray = []	
psdarray = []
varray2 = []	
psdarray2 = []
va = -1
va2 = -1

energy_array = []
energy2_array = []

c1 = 'lightblue'
c2 = 'red'
ac1 = 'orangered'
ac2 = 'purple'

if args.number_of_scintillators[0] == 1:
	for input_file in range(len(args.first_input_data)):

		path = '{}'.format(args.first_input_data[input_file])
        
		f = open(path)
		data = f.readlines()

		voltage = []
		time = []
		for line in data:
			split_line = line.split(' ')
			if len(split_line) > 1:
				time.append(float(split_line[0]))
				voltage.append(float(split_line[1]))

		#psd = []
		#energy = []
		psd = (float(time[0]))
		energy = (float(voltage[0]))
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
			
			#plt.subplot(1,4,1)

			plt.plot(time, voltage, alpha=0.1, color=c1)
            
			#plt.subplot(1,4,2)
			#Expo_Fit(voltage, time, 1, c1)  #not sure if this function actually works or not
		
		#plt.subplot(1,4,4)
		#plt.scatter(energy,psd, color=c1, label='Scint 1')

		va +=1

	Avarray = []
	Current = []
	for val in varray:
		Avarray.append(val/len(args.first_input_data))
		Current.append(val/50)		

	d = np.array([time,Avarray])
	d = d.T
	np.savetxt('data/{}/{}/{}_Average_Waveform.txt'.format(args.pmt_used[0], args.scintillator[0], args.output_file_name), d, delimiter=';')  
    #may need to change (above) due to file naming system changing

	##########Returns/Printing for Set 1

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

	#plt.subplot(1,4,2)						#Plots the Exponential Decay of the curve
	#Expo_Fit(Avarray, time, 1, ac1)
	#plt.xlabel("Time [s]")
	#plt.ylabel("Amplitude [V]")
	#plt.title("Set Decay Rates")

	plt.show()
