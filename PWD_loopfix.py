import os
import struct
import numpy as np
import matplotlib.pyplot as plt
from statistics import mode, StatisticsError
from database_functions import *
import glob

from argparse import ArgumentParser

vres = 2.0 / (2**14 -1) # voltage resolution in volts
tres = 4e-9             # time resolution in seconds

parser = ArgumentParser(prog = 'Pulse Waveform Database', description='This is a database for scintillatior pulse waveforms for gamma-ray astronomy.')
parser.add_argument('-a', '--add', help='The file (which file you want to use as data)')
parser.add_argument('-p', '--pmt', help='Which Photomultiplier Tube was used', required=True)
parser.add_argument('-s', '--scintillator', help='Type of scintillator(s) used', required=True)
parser.add_argument('-c', '--psd-cut', type=float, nargs=2, help='The start and first end of the PSD cut range')
parser.add_argument('-y', '--source', help='The (gamma-ray) source element/isotope used (e.g. Cs137)', required=True)
parser.add_argument('-o', '--output-scintillator', help='The name of output scintillator for saving purposes')
parser.add_argument('-b', '--baseline', default=100, type=int, help='Number of samples to use when computing waveform baseline.')
parser.add_argument('-e', '--energy-target', type=int, nargs=2, help='The Energy Target Range in keV')
parser.add_argument('-w', '--number-of-waveforms', type=int, help='The number of waveforms you would like saved')
parser.add_argument('-l', '--list-available-input-files', action='store_true', help='Show available input and currently saved output files')
parser.add_argument('-x', '--plot', action='store_true', help='Plot psd v. energy to infom psd cuts and energy selection')
#parser.add_argument('-strip', '--strip_array', action='store_true', help='strip waveform from array for smaller files and outside use')

args = parser.parse_args()

if args.add is not None:
    dir = "raw/%s/%s/" %(args.pmt, args.scintillator)  #directory name
    print(dir)
    print("\n")
    path = os.path.join(dir, args.source + ".bin")        #will use .bin files later
    os.system("mkdir -p " + dir)                              #makes directory (if it doesn't exist)
    os.system("cp '%s' '%s'" %(args.add, path))                  #copies --add file to path
    os.system("ls raw/%s/%s/" %(args.pmt, args.scintillator))     #lists file in directory (just to check)

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

dir = "raw/%s/%s/" %(args.pmt, args.scintillator)
path = os.path.join(dir, args.source + ".bin")

scint_out = args.output_scintillator if args.output_scintillator is not None else args.scintillator
vfilename = args.source + '_data_' + scint_out # base output file name for waveforms
vfilename = 'data/{}/{}/{}_%05d.txt'.format(args.pmt, args.scintillator, vfilename) 

"""
    if args.output_scintillator is not None:
        out_dir = "data/%s/%s/" %(args.pmt[0], args.output_scintillator[0])  #output directory name
        print(out_dir)
        print("\n")
        path = os.path.join(dir, args.source[0] + ".bin")
        os.system("mkdir -p " + out_dir)            #makes the output directory
    else:
        out_dir = "data/%s/%s/" %(args.pmt[0], args.scintillator[0])  #output directory name
        print(out_dir)
        print("\n")
        path = os.path.join(dir, args.source[0] + ".bin")
        os.system("mkdir -p " + out_dir)            #makes the output directory
"""
    
# open the file
f = open(path, 'rb')

# loop to read file
cnt = 0 # number of events read from file
nout = 0 # number of waveforms output
psd_flags = 0 # number of events with psd NaN
results = [] # stored (energy, psd) results for each event
saved_results = []
while True:
    board = f.read(2)
    if len(board) == 0:
        break
            
    board = struct.unpack('H',board)[0]
    channel = struct.unpack('H',f.read(2))[0]
    timestamp = struct.unpack('Q',f.read(8))[0]
    energy = struct.unpack('H',f.read(2))[0]
    energy_short = struct.unpack('H',f.read(2))[0]
    flags = struct.unpack('I',f.read(4))[0]
    nsample = struct.unpack('I',f.read(4))[0]
    samples = struct.unpack(nsample * 'H', f.read(2 * nsample))
        
    voltage = np.array(samples) * vres # Conversion from 2V range using 14 bit digitizer
    time = tres * np.arange(voltage.size)       # Times of each voltage sample are seperated by 4 nanoseconds
        
    # prevents divide by zero
    if energy == 0:
        psd = 0.
        psd_flags += 1
    else:
        psd = float(energy - energy_short) / float(energy)

    results.append([energy, psd])
        
    cnt += 1
    print(cnt)
        
    if args.psd_cut is not None and args.energy_target is not None:
            
        # Both psd and energy cuts for sorting data
        psd_selected = (psd < args.psd_cut[1]) & (psd > args.psd_cut[0])
        energy_selected = (energy < args.energy_target[1]) & (energy > args.energy_target[0]) 
            
        if psd_selected and energy_selected:
            saved_results.append([energy, psd])

            # calculate baseline subtracted voltage
            v = np.array(samples) * vres
            baseline = v[:args.baseline].sum() / args.baseline
            v -= baseline

            # write the file
            with open(vfilename % (nout + 1), 'w') as op:
                op.write("%.6e %.6e\n" % (energy, psd))
                for i in range(v.size):
                    op.write("%.6e %.6e\n" % (i * tres, v[i]))
            op.close()

            nout += 1
            if nout == 100:
                break

    # END if (psd_cut and energy_target)

    #if (cnt > 5000): break
f.close()
print("PSD Flags (energy = 0): ",psd_flags)

energy, psd = np.transpose(results)

if args.plot is True:
        ##########################
        #####ENERGY HIST HERE#####

        plt.figure(figsize=(12, 6))
        plt.subplot(1,2,1)
        ax1 = plt.gca()
        plt.scatter(energy, psd, color='black')
        plt.ylim(0,1)
        plt.xlabel("Energy")
        plt.ylabel("PSD")

        plt.subplot(1,2,2) 
        ax2 = plt.gca()
        plt.hist(energy, bins=100, color='black')
        plt.xlabel("Energy")
        plt.ylabel("Counts")
 
        if args.psd_cut is not None:
            mask = (psd < args.psd_cut[1]) & (psd > args.psd_cut[0])
            ax1.scatter(energy[mask], psd[mask], color='orange')
            ax2.hist(energy[mask], bins=100, color='orange')

                    
        plt.show()
        exit(0)
        """
        else:
            print("I am here 2")
            plt.scatter(energy, psd, color='black')
            plt.ylim(0,1)
            plt.xlabel("Energy")
            plt.ylabel("PSD")
            plt.show() 
                    
        if args.psd_cut is not None and args.energy_target is not None:
            print("I am here 3")
            mask = (psd < args.psd_cut[1]) & (psd > args.psd_cut[0])
            _, bins, _ = plt.hist(energy, bins=100, color='black') #sets the standard bin count for all energy (for use in masked histogram)
            plt.subplot(1,2,1) 
            plt.scatter(energy, psd, color='black')
            plt.ylim(0,1)
            plt.subplot(1,2,2)
            plt.hist(energy[mask], bins=bins, color='black')#4096
            plt.xlabel("Energy")
            plt.ylabel("Counts")
            plt.subplot(1,2,1)
            plt.scatter(masked_energy,masked_psd, color='orange')
            plt.xlabel("Energy")
            plt.ylabel("PSD")
            plt.subplot(1,2,2)
            plt.hist(masked_energy, bins=bins, color='orange')

            d = np.array([masked_energy,masked_psd])
            d = d.T
            #np.savetxt('data/{}/{}/MASKEDkev_psd_energy_{}.txt'.format(pmtloc,scintloc,args.output_scintillator[0]), d, delimiter=';')
            plt.show()
        """
