import numpy as np
import matplotlib.pyplot as plt
from statistics import mode, StatisticsError
from database_functions import *

from argparse import ArgumentParser

parser = ArgumentParser(prog = 'Pulse Waveform Database', description='This is a database for scintillatior pulse waveforms for gamma-ray astronomy.')
parser.add_argument('-i', '--input', help='The input file (which file you want to use as data)')
parser.add_argument('-p', '--pmt', type=str, nargs=1, help='Which Photomultiplier Tube was used')       #change to 'photosensor'
parser.add_argument('-s', '--scintillator', type=str, nargs=1, help='Type of scintillator(s) used')
parser.add_argument('-c', '--psd-cut', type=float, nargs=2, help='The start and first end of the PSD cut range')
parser.add_argument('-e', '--element', type=str, nargs=1, help='The (gamma-ray) source element/isotope used (e.g. Cs137)')
parser.add_argument('-r', '--run-number', type=int, nargs=1, help='The file run number for saving purposes')
parser.add_argument('-etarg', '--energy-target', type=int, nargs=2, help='The Energy Target Range in keV')
parser.add_argument('-w', '--number_of_waveforms', type=int, nargs=1, help='The number of waveforms you would like saved')

args = parser.parse_args()

if args.scintillator is None:
	parser.error('No scintillators specified. . . Please specify the type of scintillator(s) used')
if args.scintillator is not None:
	if len(args.scintillator) != 1:
		parser.error('Incorrect number of scintillators specified. . . Please specify 1 scintillator')

if args.pmt is None:
	parser.error('No PMT specified. . . Please specify the type of PMT used')

if args.element is None:
	parser.error('No source specified. . . Please specify the gamma-ray source used')
if args.element is not None and len(args.element) != 1:
	parser.error('Too many sources specified. . . Please specify a single source')
Scale_Marker = 0
#if args.element is not None and len(args.element) == 1:			#Most common peak values for sources (for scalling)
#	if args.element[0] == 'Ba133':
#		Scale_Marker = 276
#	if args.element[0] == 'Cs137':
#		Scale_Marker = 662
#	if args.element[0] == 'Co60':
#		Scale_Marker = 1333
#	if args.element[0] == 'Am241':
#		Scale_Marker = 60

if args.run_number is None:
	parser.error('No run specified. . . Please specify the collection run used')
if args.element is not None and len(args.element) != 1:
	parser.error('Too many runs specified. . . Please specify a single collection run')

print("Selected File: ",args.input)
print("PMT Used: ",args.pmt)
print("Scintillator Used: ",args.scintillator)
print("PSD Cut Range: ",args.psd_cut)
print("Gamma-ray Source: ",args.element)


path = args.input			#Accepts input file

f = open(path)				#Opens file
header = f.readline()			

lines = f.readlines()			#Reads file
#print(lines)


samps = 0			#Samples gathered
numosamps = 0			#Number of Samples wanted
if args.number_of_waveforms is None:			#Automates samples gathered for saving later on
	numosamps = len(lines)
if args.number_of_waveforms is not None:
	if args.number_of_waveforms[0] > len(lines) or args.number_of_waveforms[0] < 1:
		parser.error('Specified Samples out of Range. . . Enter a number between 1 and the file length [{}]'.format(len(lines)))	
	if args.number_of_waveforms[0] <= len(lines):
		numosamps = args.number_of_waveforms[0]

		
n = len(lines)

# variables used to hold waveform information in memory
energy = np.zeros(n, np.float64)
energy_short = np.zeros(n, np.float64)
psd = np.zeros(n, np.float64)
waveforms = []

nbase = 100
k = 0

#######"Loading Bar"###################
lb = 0
#######"Loading Bar"###################

if len(args.scintillator) == 1:						
	pmtloc = args.pmt[0]
	scintloc = args.scintillator[0]
	filename = args.element[0] + '_data_run_' + str(args.run_number[0]) + "_" + args.scintillator[0]		#File names

# loop through to collect waveforms
for i, line in enumerate(lines):
      energy[i] = float(line.split(';')[1])
      energy_short[i] = float(line.split(';')[2])
      samples = [int(s) for s in line.split(";")[4:]]
      voltage = np.array(samples) * 2.0 / (2**14 -1)  # Conversion from 2V range using 14 bit integer from the digitizer
      waveforms.append(voltage)

waveforms = np.array(waveforms) # need to caste waveforms as an np.array so we can use psd, energy masking later

eMode = mode(energy)				#Finds most common (highest) energy peak to scale against the most common source peaks
for g in range(len(energy)):		#Scales energy and returns histogram
#	energy[g] = float(energy[g] * (Scale_Marker / eMode))
#	energy_short[g] = float(energy_short[g] * (Scale_Marker / eMode))

	if energy[g] != 0:							#Calculates PSD from energy long and short 
		psd[g] = float(energy[g] - energy_short[g]) / float(energy[g])
		#print(psd)
	if energy[g] == 0:							#Prevents divide by zero error (have only seen it once)
		psd[g] = 1.0

	# compute PSD values from the stored energy, energy_short values
	#psd[g] = float(energy[g] - energy_short[g]) / float(energy[g])
plt.subplot(1,2,1)
plt.hist(energy, bins=100, range=[0,1000])
plt.subplot(1,2,2)
plt.scatter(energy, psd)
plt.ylim(0,1.5)
plt.show()

# NOTE: You could use the input() function here to pause and let the user enter energy and PSD information from the command line after looking at the energy and PSD histograms compute the time series once because it's the same for every waveform in a given file

time = np.arange(np.size(waveforms)) * 4e-9 # Times of each voltage sample are separated by 4 nanoseconds

                                                #could probably change these to input as the type they are meant to be used in (less steps)
scints = input("input your scintillators: ")  
ecuts = input("energy cuts: ")
pcuts = input("psd cuts: ")

scintillators = scints.split(" ")
energy_cuts = ecuts.split(" ")
psd_cuts = pcuts.split(" ")

print(scintillators, energy_cuts, psd_cuts)

# now loop over the scintillators you want to output
for w in range(len(scintillators)):

	psd_min = float(psd_cuts[0])
	psd_max = float(psd_cuts[1])
	#print(psd_min)
	energy_min = int(energy_cuts[0])
	energy_max = int(energy_cuts[1])

	mask = (psd_min < psd) & (psd < psd_max) & (energy_min < energy) & (energy < energy_max)
	masked_psd = psd[mask]
	masked_energy = energy[mask]
	masked_waveforms = waveforms[mask]

 

	nbase = 100 # use 100 samples to measure the baseline of the voltage waveform at the beginning. This is the “zero” point
	nmax = np.min([mask.sum(), 100]) # output 100 waveforms if available, otherwise output all waveforms selected by mask

	for j in range(nmax):

		waveform = masked_waveforms[j]
		baseline = waveform[:nbase].sum() / nbase
		waveform -= baseline
		print("yes")
		#  "write masked_psd[j], masked_energy[j], waveform to a file"
		if samps >= numosamps:
			break
		time = np.insert(time, 0, psd[j], axis=0)		#Inserts psd into array for saving to 1 file
		voltage = np.insert(waveforms, 0, energy[j], axis=0)	#Inserts energy into array for saving to 1 file	

		data = np.array([time,waveforms])
		data = data.T
		np.savetxt('data/{}/{}/{}__{}.txt'.format(pmtloc,scintillators[0],filename,samps), data, delimiter=';')

		
		samps +=1
		k += 1
		#######"Loading Bar"###################
		print("Set [",samps,"/",numosamps,"] of [",len(lines),"] . . . Compiled")
















for line in lines:
#	timestamp = int(line.split(";")[0])					#Timestamp of set
	#print(timestamp)
#	energy = (int(line.split(';')[1]) * (Scale_Marker / Mode))		#Energy long gate of set
	#print("e = ",energy)

#	energyshort = float(int(line.split(';')[2]) * (Scale_Marker / Mode))	#Energy short gate of set
	#print("es = ",energyshort)
#	samples = [int(s) for s in line.split(";")[4:]]				#Data samples for the set
	
	if len(args.scintillator) == 1:
		#print(line)
	
#		voltage = np.array(samples) * 2.0 / (2**14 -1)  #Conversion from 2V range using 14 bit digitizer
#		time = 4e-9 * np.arange(voltage.size)           #Times of each voltage sample are seperated by 4 nanoseconds

		baseline = voltage[:nbase].sum() / nbase
		voltage -= baseline

#		if energy != 0:							#Calculates PSD from energy long and short 
#			psd = float(energy - energyshort) / float(energy)
#			#print(psd)
#		if energy == 0:							#Prevents divide by zero error (have only seen it once)
#			psd = 0.0

		Bcut = (psd < args.psd_cut[1]) and (psd > args.psd_cut[0]) and (energy < args.energy_target[1]) and (energy > args.energy_target[0])							#Both psd and energy cuts for sorting data


		#######"Loading Bar"###################
		if lb == 0:
			print("Compiling Sets within parameters. . . [0/",numosamps,"] of [",len(lines),"]")
		#######"Loading Bar"###################
		
		if k <= len(lines):			#was -- if k < len(lines)
			if samps >= numosamps:
				break
			if Bcut:
				time = np.insert(time, 0, psd, axis=0)			#Inserts psd into array for saving to 1 file
				voltage = np.insert(voltage, 0, energy, axis=0)		#Inserts energy into array for saving to 1 file	

				data = np.array([time,voltage])
				data = data.T
				np.savetxt('data/{}/{}/{}__{}.txt'.format(pmtloc,scintloc,filename,samps), data, delimiter=';')

				
				samps +=1
				k += 1
				#######"Loading Bar"###################
				print("Set [",samps,"/",numosamps,"] of [",len(lines),"] . . . Compiled")
	lb+=1
print("Sending Data. . .\n. . . All Related Sets Compiled and Sent")
#######"Loading Bar"###################	
