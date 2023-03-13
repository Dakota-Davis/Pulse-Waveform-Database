import os
import numpy as np
import matplotlib.pyplot as plt
from statistics import mode, StatisticsError
from database_functions import *
import glob

from argparse import ArgumentParser

parser = ArgumentParser(prog = 'Pulse Waveform Database', description='This is a database for scintillatior pulse waveforms for gamma-ray astronomy.')
parser.add_argument('-a', '--add', help='The file (which file you want to use as data)')
parser.add_argument('-p', '--pmt', type=str, nargs=1, help='Which Photomultiplier Tube was used', required=True)
parser.add_argument('-scint', '--scintillator', type=str, nargs=1, help='Type of scintillator(s) used', required=True)
parser.add_argument('-c', '--psd-cut', type=float, nargs=2, help='The start and first end of the PSD cut range')
parser.add_argument('-s', '--source', type=str, nargs=1, help='The (gamma-ray) source element/isotope used (e.g. Cs137)', required=True)
parser.add_argument('-r', '--run-number', type=int, nargs=1, help='The file run number for saving purposes')
parser.add_argument('-etarg', '--energy-target', type=int, nargs=2, help='The Energy Target Range in keV')
parser.add_argument('-w', '--number_of_waveforms', type=int, nargs=1, help='The number of waveforms you would like saved')
parser.add_argument('-list', '--list-available-input-files', action='store_true', help='Show available input and currently saved output files')

args = parser.parse_args()

if args.add is not None:
    dir = "raw\%s\%s\" %(args.pmt[0], args.scintillator[0])  #directory name
    print(dir)
    print("\n")
    path = os.path.join(dir, args.source[0] + ".csv")        #will use .bin files later
    os.system("mkdir -p " + dir)                              #makes directory (if it doesn't exist)
    os.system("cp %s %s" %(args.add, path))                  #copies --add file to path
    os.system("ls raw\%s\%s\" %(args.pmt[0], args.scintillator[0]))     #lists file in directory (just to check)

#Just some prints to help display what the user has specified    
print("\nSelected File: ",args.add)
print("PMT Used: ",args.pmt)
print("Scintillator(s) Used: ",args.scintillator)
print("PSD Cut Range: ",args.psd_cut)
print("Energy Target Range: ",args.energy_target)
print("Gamma-ray Source: ",args.source)


if args.list_available_input_files:
    glob_paths = sorted(glob.glob("raw/*/*/*"))
    print("\nAvailable Input Data:")

    for path in glob_paths:
        print("File Path:",path)
        print("Data File:",path.split('/')[-1])
        
    glob_paths = glob.glob("data/*/*/*")
    print("\nCurrently Saved Output Data Files:")
    
    for path in glob_paths:
        print(path)
        #print("Data File:",path.split('/')[-1])

if args.psd_cut is not None:        #temporary check to prevent running errors while writing new code 
    dir = "raw/%s/%s/" %(args.pmt[0], args.scintillator[0])
    path = os.path.join(dir, args.source[0] + ".csv")
    

    out_dir = "data/%s/%s/" %(args.pmt[0], args.scintillator[0])  #output directory name
    print(out_dir)
    print("\n")
    path = os.path.join(dir, args.source[0] + ".csv")        #will use .bin files later
    os.system("mkdir -p " + out_dir)            #makes the output directory
    
    
    f = open(path) #Opens file
    header = f.readline()
    
    lines = f.readlines() #Reads file
    #print(lines)


    samps = 0 #Samples gathered
    numosamps = 0 #Number of Samples wanted
    if args.number_of_waveforms is None: #Automates samples gathered for saving later on
        numosamps = len(lines)
    if args.number_of_waveforms is not None:
        if args.number_of_waveforms[0] > len(lines) or args.number_of_waveforms[0] < 1:
            parser.error('Specified Samples out of Range. . . Enter a number between 1 and the file length [{}]'.format(len(lines)))
        if args.number_of_waveforms[0] <= len(lines):
            numosamps = args.number_of_waveforms[0]

    energy = [] #ENERGY ARRAY
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
        vfilename = args.source[0] + '_data_run_' + str(args.run_number[0]) + "_" + args.scintillator[0] #File names



    for line in lines:
        ener = int(line.split(";")[1])
        energy.append(ener)
        samples = [int(s) for s in line.split(";")[4:]] #Data samples for the set
        ener_short = int(line.split(';')[2])
        energy_short.append(ener_short)

        voltage = np.array(samples) * 2.0 / (2**14 -1)  #Conversion from 2V range using 14 bit digitizer
        time = 4e-9 * np.arange(voltage.size)           #Times of each voltage sample are seperated by 4 nanoseconds

        #baseline = voltage[:nbase].sum() / nbase
        #voltage -= baseline
        waveforms.append(voltage)

    eMode = mode(energy) #Finds most common (highest) energy peak to scale against the most common source peaks

    psd = np.zeros(len(lines), np.float64)

    for e in range(len(energy)): #Scales energy and energy short to preset mode peak of source

        if energy[e] != 0: #Calculates PSD from energy long and short 
            psd[e] = float(energy[e] - energy_short[e]) / float(energy[e])

    energy = np.array(energy)
    waveforms = np.array(waveforms)

    data = np.array([energy,psd])
    data = data.T
    np.savetxt('data/{}/{}/ALLkev_psd_energy.txt' .format(pmtloc,scintloc), data, delimiter=';')

    ##########################
    #####ENERGY HIST HERE#####
    plt.subplot(1,2,1)
    plt.hist(energy, bins=400, range=[0,400], color='black')#4096
    plt.xlim(0,400)
    plt.subplot(1,2,2)
    plt.scatter(energy, psd, color='black')
    plt.ylim(0,1)
    #plt.show()
    ##########################
    #####TAKE INPUTS HERE?####
    ##########################


    #for l in range(len(psd)):
    

    mask = (psd < args.psd_cut[1]) & (psd > args.psd_cut[0]) & (energy < args.energy_target[1]) & (energy > args.energy_target[0]) #Both psd and energy cuts for sorting data
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

        time = np.insert(time, 0, masked_psd[j], axis=0) #Inserts psd into array for saving to 1 file
        waveform = np.insert(waveform, 0, masked_energy[j], axis=0) #Inserts energy into array for saving to 1 file 
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
    """
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
    """
    #this is a tab test
    