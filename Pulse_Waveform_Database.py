import numpy as np
import matplotlib.pyplot as plt
from statistics import mode, StatisticsError
from database_functions import *

from argparse import ArgumentParser

parser = ArgumentParser(prog = 'Pulse Waveform Database', description='This is a database for scintillatior pulse waveforms for gamma-ray astronomy.')
parser.add_argument('-i', '--input', help='The input file (which file you want to use as data)')
parser.add_argument('-p', '--pmt', type=str, nargs=1, help='Which Photomultiplier Tube was used')
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


if args.run_number is None:
	parser.error('No run specified. . . Please specify the collection run used')
if args.element is not None and len(args.element) != 1:
	parser.error('Too many runs specified. . . Please specify a single collection run')

print("Selected File: ",args.input)
print("PMT Used: ",args.pmt)
print("Scintillator(s) Used: ",args.scintillator)
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

		
energy = []			#ENERGY ARRAY
energy_short = []
waveforms = []

#nbase = 100
k = 0
#######"Loading Bar"###################
lb = 0
#######"Loading Bar"###################

if len(args.scintillator) == 1:						
	pmtloc = args.pmt[0]
	scintloc = args.scintillator[0]
	vfilename = args.element[0] + '_data_run_' + str(args.run_number[0]) + "_" + args.scintillator[0]		#File names



for line in lines:
	ener = int(line.split(";")[1])		
	energy.append(ener)
	samples = [int(s) for s in line.split(";")[4:]]				#Data samples for the set
	ener_short = int(line.split(';')[2])
	energy_short.append(ener_short)

	voltage = np.array(samples) * 2.0 / (2**14 -1)  #Conversion from 2V range using 14 bit digitizer
	time = 4e-9 * np.arange(voltage.size)           #Times of each voltage sample are seperated by 4 nanoseconds		#MOVE?#

	#baseline = voltage[:nbase].sum() / nbase
	#voltage -= baseline
	waveforms.append(voltage)

eMode = mode(energy)				#Finds most common (highest) energy peak to scale against the most common source peaks

psd = np.zeros(len(lines), np.float64)
#print(len(energy))
#print(len(psd))
#print(len(time))
#print(len(voltage))
#print(waveforms)

for e in range(len(energy)):				#Scales energy and energy short to preset mode peak of source
#	energy[e] = float(energy[e] * (Scale_Marker / eMode))			#Energy long gate of set
#	energy_short[e] = float(energy_short[e] * (Scale_Marker / eMode))		#Energy short gate of set

	if energy[e] != 0:							#Calculates PSD from energy long and short 
		psd[e] = float(energy[e] - energy_short[e]) / float(energy[e])
		#print(psd)
	if energy[e] == 0:							#Prevents divide by zero error (have only seen it once)
		psd[e] = 0.0

energy = np.array(energy)
waveforms = np.array(waveforms)

data = np.array([energy,psd])
data = data.T
np.savetxt('data/{}/{}/ALLkev_psd_energy.txt'.format(pmtloc,scintloc), data, delimiter=';')

##########################
#####ENERGY HIST HERE#####
plt.subplot(1,2,1)
plt.hist(energy, bins=400, range=[0,400], color='black')		#4096
plt.xlim(0,400)
plt.subplot(1,2,2)
plt.scatter(energy, psd, color='black')
plt.ylim(0,1)
#plt.show()
##########################
#####TAKE INPUTS HERE#####
##########################


#for l in range(len(psd)):
if True:
	if len(args.scintillator) == 1:

		mask = (psd < args.psd_cut[1]) & (psd > args.psd_cut[0]) & (energy < args.energy_target[1]) & (energy > args.energy_target[0])							#Both psd and energy cuts for sorting data
		masked_psd = psd[mask]
		masked_energy = energy[mask]

		#print(waveforms.shape)
		#print("Mask shape: ",mask.shape)
		masked_waveforms = waveforms[mask]
		#print(masked_waveforms,masked_waveforms.shape)
		#print("Mask sum: ",mask.sum())

		nbase = 100 # use 100 samples to measure the baseline of the voltage waveform at the beginning. This is the “zero” point
		#nmax = np.min([mask.sum(), 100]) # output 100 waveforms if available, otherwise output all waveforms selected by mask
		#for j in range(nmax):
		for j in range(len(masked_waveforms)): 
			if samps >= numosamps:
				break
			
			waveform = masked_waveforms[j]
			baseline = waveform[:nbase].sum() / nbase
			waveform -= baseline
			#print("sent")
			
			#plt.plot(time, waveforms[l])
			#plt.show()

			#print(waveform,waveform.shape)
			
			time = np.insert(time, 0, masked_psd[j], axis=0)			#Inserts psd into array for saving to 1 file
			waveform = np.insert(waveform, 0, masked_energy[j], axis=0)		#Inserts energy into array for saving to 1 file	
			#print("energy is: ",energy[j])
			#print(waveform,waveform.shape)

			data = np.array([time,waveform])
			data = data.T
			
			with open('data/{}/{}/{}__{}.txt'.format(pmtloc,scintloc,vfilename,samps), 'w') as op:
				for sample in range(time.size):
					#print(time[sample])
					#print(waveform[sample])
					#print(sample)
					op.write("%.6e;%.6e\n"%(time[sample],waveform[sample]))
				op.close()

			time = np.delete(time, 0, 0)
			waveform = np.delete(waveform, 0, 0)
			samps +=1
			k += 1
			#######"Loading Bar"###################
			print("Set [",samps,"/",numosamps,"] of [",len(lines),"] . . . Compiled")
			#######"Loading Bar"###################
plt.subplot(1,2,1)
plt.hist(masked_energy, bins=400, range=[0,400], color='orange')
plt.xlim(0,400)
plt.xlabel("Energy")
plt.ylabel("Counts")
plt.subplot(1,2,2)
plt.scatter(masked_energy,masked_psd, color='orange')
plt.xlabel("Energy")
plt.ylabel("PSD")
d = np.array([masked_energy,masked_psd])
d = d.T
np.savetxt('data/{}/{}/MASKEDkev_psd_energy.txt'.format(pmtloc,scintloc), d, delimiter=';')
plt.show()