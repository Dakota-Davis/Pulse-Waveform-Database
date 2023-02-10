import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.signal import lfilter
import scipy.signal as signal
from database_functions import *

from argparse import ArgumentParser

parser = ArgumentParser(prog = 'Pulse Waveform Database Data Runner', description='This is a data runner for the Pulse Waveform Database')
parser.add_argument('-n', '--number-of-scintillators', type=int, nargs=1, help='The number of scintillators used in the test')
parser.add_argument('-fid', '--first-input-data',type=str, nargs='+', help='The first set of data file(s) (which file you want to use)')
parser.add_argument('-sid', '--second-input-data',type=str, nargs='+', help='The second set of data file(s) (which file you want to use)')
parser.add_argument('-p', '--pmt-used', type=str, nargs='*', help='The PMT that was used for the data set')
parser.add_argument('-s', '--set-used', type=int, nargs=1, help='Which scintillator set is desired/run')
parser.add_argument('-t', '--scintillator-type', type=str, nargs='*', help='The scintillator that was used for the data set')
parser.add_argument('-hc', '--histogram-xlimit', type=int, nargs=2, help='The minimum and maximum x-limit for the energy histogram')
parser.add_argument('-show', '--shown_waveforms', type=str, nargs=1, help='To show or not to show all individual waveforms [ALL] or [NONE]')

args = parser.parse_args()

if args.first_input_data is None and args.second_input_data:
	parser.error('No data specified. . . Please specify the data file to be run')

if args.number_of_scintillators is None:
	parser.error('No scintillators specified. . . Please specify the number of scintillators used')
if args.number_of_scintillators is not None:
		if args.number_of_scintillators[0] not in (1,2):
			parser.error('Too many scintillators specified. . . Please specify a value between 1 and 2')

if args.histogram_xlimit is not None and len(args.histogram_xlimit) != 2:
	parser.error('Incorrect number of histogram x-limits specified. . . Please specify 2 x-limits')

if args.set_used is None and args.number_of_scintillators[0] != 2:
	parser.error('No set specified. . . Please specify the desired set')
if args.set_used is not None:	
	if args.set_used[0] != 1 and args.set_used[0] != 2:
		parser.error('Too many sets specified. . . Please specify a value between 1 and 2')

if args.number_of_scintillators[0] == 1:
		if len(args.pmt_used) == 2:
			parser.error('Too many PMTs specified. . . Only 1 scintillator specified, please match PMTs accordingly')
		if len(args.scintillator_type) == 2:
			parser.error('Too many scintillator types specified. . . Only 1 scintillator specified, please match PMTs accordingly')

if args.pmt_used is None:
	parser.error('No PMT specified. . . Please specify the PMT(s) used')
if args.pmt_used is not None:
		if len(args.pmt_used) not in (1,2):
			parser.error('Too many PMTs specified. . . Please specify a value between 1 and 2')

if args.scintillator_type is None:
	parser.error('No scintillator(s) specified. . . Please specify the type of scintillator(s) used')
if args.scintillator_type is not None:
		if len(args.scintillator_type) not in (1,2):
			parser.error('Too many scintillators specified. . . Please specify a value between 1 and 2')

if args.histogram_xlimit is None:			#Sets energy histogram limits
	hist_minxlim = 0
	hist_maxxlim = 1000
if args.histogram_xlimit is not None and len(args.histogram_xlimit) == 2:
	hist_minxlim = args.histogram_xlimit[0]
	hist_maxxlim = args.histogram_xlimit[1]

showall = True
if args.shown_waveforms[0] is None:
	showall = True
if args.shown_waveforms[0] is not None:
	if args.shown_waveforms[0] == 'NONE':
		showall = False
	if args.shown_waveforms[0] == 'ALL':
		showall = True
	if args.shown_waveforms[0] != 'ALL' and args.shown_waveforms[0] != 'NONE':
		parser.error('Choose to show [ALL] individual waveforms or [NONE] of them')

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

if args.number_of_scintillators[0] == 1 and args.set_used[0] == 1:
	for input_file in range(len(args.first_input_data)):	

		path = '{}'.format(args.first_input_data[input_file])
		f = open(path)
		data = f.readlines()

		voltage = []
		time = []
		for line in data:
			split_line = line.split(';')
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
			#Expo_Fit(voltage, time, 1, c1)
		
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
	np.savetxt('data/hamamatsu_R12699/nai_tl/356kev_Average.txt', d, delimiter=';')

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
	plt.plot(time, Avarray, label='CsI(Na) Average Curve [356keV]')#,label='PSD Average: %.6e\nAuC: %.6e\nRise Time: %.6e\nFall Time: %.6e\nAverage T90: %.4e'%(Average(psdarray),Area_under_Curve(Current, time),Rise_Time(Avarray, time),Fall_Time(Avarray, time),T90(Avarray, time)[0]))
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
		
	#plt.subplot(1,4,3)						#Adds labels to the energy histogram
	#plt.hist(energy_array, bins=100, range=[hist_minxlim,hist_maxxlim], label='Scint 1', color=c1)
	#plt.xlabel("Energy")
	#plt.ylabel("Energy Frequency")
	#plt.title("Histogram of Energy")

	#plt.subplot(1,4,4)						#Adds labels to psd v. energy
	#plt.scatter(energy_array, psdarray, s=2, color=c1)
	#plt.xlabel("Energy")
	#plt.ylabel("PSD")
	#plt.title("PSD v. Energy")

	plt.show()

#####################################################################
	#Below does same as above but for the second set in the event that 2 sets are inputed but 1 is wanted for viewing
#####################################################################
elif args.number_of_scintillators[0] == 1 and args.set_used[0] == 2:     
##########Set 2 manipulation
	
	for input_file in range(len(args.second_input_data)):	

		path = '{}'.format(args.second_input_data[input_file])
		f = open(path)
		data2 = f.readlines()

		voltage2 = []
		time2 = []
		for line in data2:
			split_line = line.split(';')
			if len(split_line) > 1:
				time2.append(float(split_line[0]))
				voltage2.append(float(split_line[1]))

		#psd2 = []
		#energy2 = []
		psd2 = (float(time2[0]))
		energy2 = (float(voltage2[0]))
		time2 = np.delete(time2, 0, 0)
		voltage2 = np.delete(voltage2, 0, 0)

		#print("PSD: ",psd2," ENERGY: ",energy2)

		for b2 in range(len(voltage2)):				
			if va2 < 0:
				varray2.append(voltage2[b2])
			if va2 >= 0:
				varray2[b2] += voltage2[b2]
		energy2_array.append(energy2)

		psdarray2.append(psd2)

		##########Graphing/Plots
		if showall is True:
			
			plt.subplot(1,4,1)

			plt.plot(time2, voltage2, alpha=0.1, color=c2)
			
			plt.subplot(1,4,2)
			Expo_Fit(voltage2, time2, 1, c2)
	
		#plt.subplot(1,4,4)
		#plt.scatter(energy2,psd2, color=c2, label='Scint 2')

		va2 +=1

	Avarray2 = []
	Current2 = []
	for val in varray2:
		Avarray2.append(val/len(args.second_input_data))
		Current2.append(val/50)		
	
	#print(va2)
	
	##########Returns/Printing for Set 2

	print("Super-Set 2 PSD Average: " ,Average(psdarray2)) #returns PSD average for cut 2

	print("Area under the curve of Super-Set 2: " ,Area_under_Curve(Current2, time2), "Coulombs")

	print("Rise Time for Super-Set 2: ",Rise_Time(Avarray2, time2), " seconds")	#returns rise time (between 5% and peak voltage)
	print("Fall Time for Super-Set 2: ",Fall_Time(Avarray2, time2), " seconds")

	print("The T90 for Super-Set 2: ",T90(Avarray2, time2)[0], "seconds")
	#print("T90 Check: ",t90(Avarray2,time2))
	#print("Original T90 Method: ",t_90(Avarray2, time2)[0])
	
	##########Graphing for Set 2

	plt.subplot(1,4,1)
	plt.plot(time2, Avarray2, label='Super-Set 2 Average', color=ac1)
	plt.xlabel(r"Time [s]")
	plt.ylabel("Amplitude [V]")
	plt.title("Amplitude v. Time")

	plt.plot(time2[T90(Avarray2, time2)[1]], Avarray2[T90(Avarray2, time2)[1]], marker=">", markersize=7, markeredgecolor="black", markerfacecolor="orange", label="Super-Set 2 T90 Start")
	plt.plot(time2[T90(Avarray2, time2)[2]], Avarray2[T90(Avarray2, time2)[2]], marker="<", markersize=7, markeredgecolor="black", markerfacecolor="orange", label="Super-Set 2 T90 End")

	plt.legend()

	plt.subplot(1,4,2)
	Expo_Fit(Avarray2, time2, 2, ac1)
	plt.xlabel("Time [s]")
	plt.ylabel("Amplitude")
	plt.title("Set Decay Rates")

	plt.subplot(1,4,3)
	plt.xlabel("Energy [keV]")
	plt.hist(energy2_array, bins=100, range=[hist_minxlim,hist_maxxlim], label='Scint 2', color=c2)
	plt.ylabel("Energy Frequency")
	plt.title("Histogram of Energy")

	plt.subplot(1,4,4)
	plt.scatter(energy2_array, psdarray2, s=2, color=c2)
	plt.xlabel("Energy")
	plt.ylabel("PSD")
	plt.title("PSD v. Energy")

	plt.show()

##################################################################### 
	#Below allows for both waveform super-sets to be run and plotted agaisnt each other, runs same as above
##################################################################### 
elif args.number_of_scintillators[0] == 2:
	##########Set 1 manipulation
	for input_file in range(len(args.first_input_data)):	

		path = '{}'.format(args.first_input_data[input_file])
		f = open(path)
		data = f.readlines()

		voltage = []
		time = []
		for line in data:
			split_line = line.split(';')
			if len(split_line) > 1:
				time.append(float(split_line[0]) / 1e-6)
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
			
			plt.subplot(1,4,1)

			plt.plot(time, voltage, alpha=0.1, color=c1)
			
			#plt.subplot(1,4,2)
			#Expo_Fit(voltage, time, 1, c1)
		
		#plt.subplot(1,4,4)
		#plt.scatter(energy,psd, color=c1, label='Scint 1')

		va +=1

	Avarray = []
	Current = []
	for val in varray:
		Avarray.append(val/len(args.first_input_data))
		Current.append(val/50)		

	#print(va)	

	##########Set 2 manipulation
	
	for input_file in range(len(args.second_input_data)):	

		path = '{}'.format(args.second_input_data[input_file])
		f = open(path)
		data2 = f.readlines()

		voltage2 = []
		time2 = []
		for line in data2:
			split_line = line.split(';')
			if len(split_line) > 1:
				time2.append(float(split_line[0]) / 1e-6)
				voltage2.append(float(split_line[1]))

		#psd2 = []
		#energy2 = []
		psd2 = (float(time2[0]))
		energy2 = (float(voltage2[0]))
		time2 = np.delete(time2, 0, 0)
		voltage2 = np.delete(voltage2, 0, 0)

		#print("PSD: ",psd2," ENERGY: ",energy2)

		for b2 in range(len(voltage2)):				
			if va2 < 0:
				varray2.append(voltage2[b2])
			if va2 >= 0:
				varray2[b2] += voltage2[b2]
		energy2_array.append(energy2)

		psdarray2.append(psd2)

		##########Graphing/Plots
		if showall is True:
			
			plt.subplot(1,4,1)

			plt.plot(time2, voltage2, alpha=0.1, color=c2)
			
			#plt.subplot(1,4,2)
			#Expo_Fit(voltage2, time2, 1, c2)
	
		#plt.subplot(1,4,4)
		#plt.scatter(energy2,psd2, color=c2, label='Scint 2')

		va2 +=1

	Avarray2 = []
	Current2 = []
	for val in varray2:
		Avarray2.append(val/len(args.second_input_data))
		Current2.append(val/50)		
	
	#print(va2)

	##########Returns/Printing for Set 1

	print("Super-Set PSD Average: " ,Average(psdarray)) #returns PSD average for cut 1

	print("Area under the curve of Super-Set 1: " ,Area_under_Curve(Current, time), "Coulombs")

	print("Rise Time for Super-Set 1: ",Rise_Time(Avarray, time), " seconds")	#returns rise time (between 5% and peak voltage)
	print("Fall Time for Super-Set 1: ",Fall_Time(Avarray, time), " seconds")

	print("The T90 for Super-Set 1: ",T90(Avarray, time)[0], "seconds")
	#print("T90 Check: ",t90(Avarray,time))
	#print("Original T90 Method: ",t_90(Avarray, time)[0])

	##########Returns/Printing for Set 2

	print("\nSuper-Set 2 PSD Average: " ,Average(psdarray2)) #returns PSD average for cut 2

	print("Area under the curve of Super-Set 2: " ,Area_under_Curve(Current2, time2), "Coulombs")

	print("Rise Time for Super-Set 2: ",Rise_Time(Avarray2, time2), " seconds")	#returns rise time (between 5% and peak voltage)
	print("Fall Time for Super-Set 2: ",Fall_Time(Avarray2, time2), " seconds")

	print("The T90 for Super-Set 2: ",T90(Avarray2, time2)[0], "seconds")
	#print("T90 Check: ",t90(Avarray2,time2))
	#print("Original T90 Method: ",t_90(Avarray2, time2)[0])
						
	##########Graphing for Set 1

	#plt.subplot(1,4,1)
	plt.plot(time, Avarray, label='NaI(Tl) Average Curve [356keV]', linewidth=4)
	plt.plot(time2, Avarray2, label='CsI(Na) Average Curve [356keV]', color=ac1, linewidth=4)
	plt.xlabel(r"Time [$\mu$s]", fontsize=40)
	plt.ylabel("Amplitude [V]", fontsize=40)
	plt.tick_params(axis='both', which='major', labelsize=30)
	plt.xlim(0, 3)
	plt.title("Amplitude v. Time", fontsize=40)

	plt.plot(time[T90(Avarray, time)[1]], Avarray[T90(Avarray, time)[1]], marker=">", markersize=15, markeredgecolor="black", markerfacecolor="yellow", label="NaI(Tl) T90 Start")
	plt.plot(time[T90(Avarray, time)[2]], Avarray[T90(Avarray, time)[2]], marker="<", markersize=15, markeredgecolor="black", markerfacecolor="yellow", label="NaI(Tl) T90 End")
	plt.plot(time2[T90(Avarray2, time2)[1]], Avarray2[T90(Avarray2, time2)[1]], marker=">", markersize=15, markeredgecolor="black", markerfacecolor="black", label="CsI(Na) T90 Start")
	plt.plot(time2[T90(Avarray2, time2)[2]], Avarray2[T90(Avarray2, time2)[2]], marker="<", markersize=15, markeredgecolor="black", markerfacecolor="black", label="CsI(Na) T90 End")

	plt.legend(prop={'size': 20})

	#plt.subplot(1,4,2)
	#Expo_Fit(Avarray, time, 1, ac1)
	#Expo_Fit(Avarray2, time2, 2, ac2)
	#plt.xlabel("Time [s]")
	#plt.ylabel("Amplitude [V]")
	#plt.title("Set Decay Rates")

	#print("ENERGY: ",energy_array," LENGHT: ",len(energy_array))
	#print("ENERGY: ",energy2_array," LENGHT: ",len(energy2_array))
	#print("PSD: ",psdarray)
	#print("PSD: ",psdarray2)

	#plt.subplot(1,4,3)
	#plt.hist(energy_array, bins=100, range=[hist_minxlim,hist_maxxlim], label='Scint 1', color=c1)
	#plt.hist(energy2_array, bins=100, range=[hist_minxlim,hist_maxxlim], label='Scint 2', color=c2)
	#plt.xlabel("Energy")
	#plt.ylabel("Energy Frequency")
	#plt.title("Histogram of Energy")

	#plt.subplot(1,4,4)	
	#plt.scatter(energy_array, psdarray, s=2, color=c1)
	#plt.scatter(energy2_array, psdarray2, s=2, color=c2)
	#plt.xlabel("Energy")
	#plt.ylabel("PSD")
	#plt.title("PSD v. Energy")

	plt.show()

