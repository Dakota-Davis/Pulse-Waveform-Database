import os
import struct
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
parser.add_argument('-out', '--output-scintillator', type=str, nargs=1, help='The name of output scintillator for saving purposes')
parser.add_argument('-etarg', '--energy-target', type=int, nargs=2, help='The Energy Target Range in keV')
parser.add_argument('-w', '--number_of_waveforms', type=int, nargs=1, help='The number of waveforms you would like saved')
parser.add_argument('-list', '--list-available-input-files', action='store_true', help='Show available input and currently saved output files')
parser.add_argument('-plot', '--plot', action='store_true', help='Plot psd v. energy to infom psd cuts and energy selection')
#parser.add_argument('-strip', '--strip_array', action='store_true', help='strip waveform from array for smaller files and outside use')

args = parser.parse_args()

if args.add is not None:
    dir = "raw/%s/%s/" %(args.pmt[0], args.scintillator[0])  #directory name
    print(dir)
    print("\n")
    path = os.path.join(dir, args.source[0] + ".bin")        #will use .bin files later
    os.system("mkdir -p " + dir)                              #makes directory (if it doesn't exist)
    os.system("cp '%s' '%s'" %(args.add, path))                  #copies --add file to path
    os.system("ls raw/%s/%s/" %(args.pmt[0], args.scintillator[0]))     #lists file in directory (just to check)

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

if args.psd_cut is not None or args.plot is True:        #temporary check to prevent running errors while writing new code 
    dir = "raw/%s/%s/" %(args.pmt[0], args.scintillator[0])
    path = os.path.join(dir, args.source[0] + ".bin")
    
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
    
    
    f = open(path, 'rb') #Opens file
    #header = f.readline()
    
    #lines = f.readlines() #Reads file
    #print(lines)
    i=0             #what is this for?
    z=0
    energy_arr = []
    es_arr = []
    psd_arr = []
    psd_flags = 0
    samp_arr = []
    
    masked_psd = []
    masked_energy = []
    masked_waveforms = []
    
    #stripped_array = []
    
    while True:
        board = f.read(2)
        i+=1        #what is this for?
        if len(board) == 0:
            print("PSD flags (energy=0): ",psd_flags)    
            break
            
        board = struct.unpack('H',board)[0]
        channel = struct.unpack('H',f.read(2))[0]
        timestamp = struct.unpack('Q',f.read(8))[0]
        energy = struct.unpack('H',f.read(2))[0]
        energy_short = struct.unpack('H',f.read(2))[0]
        flags = struct.unpack('I',f.read(4))[0]
        nsample = struct.unpack('I',f.read(4))[0]
        samples = struct.unpack(nsample * 'H', f.read(2 * nsample))
        #print(samples[0])
        #print(board,channel,timestamp,energy,energy_short,flags,nsample)
        
        #if args.strip_array is not None:     taking out feature until fixed
        #    s_array = [struct.pack('H',board),struct.pack('H',channel),struct.pack('Q',timestamp),struct.pack('H',energy),struct.pack('H',energy_short),struct.pack('I',flags),struct.pack('I',nsample)]
        
        energy_arr.append(energy)       #testing bringing it back for plotting & overall run speed
        #es_arr.append(energy_short)
        #samp_arr.append(samples)        # <-- this is the memory issue
            #removed all 3 to make nothing list dependent (for now probably)
        
        #if args.strip_array is not None:
        #    stripped_array.append(s_array)
        
        #energy = [] #ENERGY ARRAY
        #energy_short = []
        #waveforms = []

        #waveforms = []
        #nbase = 100
        k = 0
        #######"Loading Bar"###################
        lb = 0
        #######"Loading Bar"###################
        """
        if len(args.scintillator) == 1:
            pmtloc = args.pmt[0]
            scintloc = args.scintillator[0]
            vfilename = args.source[0] + '_data_run_' + str(args.run_number[0]) + "_" + args.scintillator[0] #File names
        """    
        voltage = np.array(samples) * 2.0 / (2**14 -1) #Conversion from 2V range using 14 bit digitizer
        #print(voltage[0])
        #print(voltage)
        time = 4e-9 * np.arange(voltage.size)       #Times of each voltage sample are seperated by 4 nanoseconds
        #print(time)

            #waveforms.append(voltage)
            #print(voltage)
        
        #psd = np.zeros(len(energy_arr), np.float64)
        #psd = np.zeros(len(lines), np.float64)
        
        if energy != 0:     #prevents divide by zero
            psd = float(energy - energy_short) / float(energy)
            psd_arr.append(psd)
        else:
            psd = 1.1
            psd_arr.append(psd)
            psd_flags += 1
        #if psd == 0:
        #    print("here", energy,energy_short)
        #print(psd)

        #energy = np.array(energy_arr)
        #waveforms = np.array(waveforms)
        
        z+=1
        print(z)            #after this is the saving section
        
        
        """
        data = np.array([energy,psd])
        data = data.T
        np.savetxt('data/{}/{}/ALLkev_psd_energy.txt' .format(pmtloc,scintloc), data, delimiter=';')
        """
        if args.psd_cut is not None and args.energy_target is not None: #can this be moved out of the loop, probably
            if len(args.scintillator) == 1:
                pmtloc = args.pmt[0]
                scintloc = args.scintillator[0]
                if args.output_scintillator is not None:
                    scintloc = args.output_scintillator[0]
                    vfilename = args.source[0] + '_data_' + args.output_scintillator[0] #File names
                else:
                    vfilename = args.source[0] + '_data_' + args.scintillator[0] #File names
            
            """
            #do we need this? not entirely sure what it's used for... reduces run speed, too...      
            data = np.array([energy,psd])
            #data = data.T       
            #print(data)
            if z == 1:      #not sure whats going wrong, but this is only saving vertically (not all that critical though)
                with open('data/{}/{}/ALLkev_psd_energy_{}.txt' .format(pmtloc,scintloc,args.output_scintillator[0]), 'w') as ALLkev:
                    np.savetxt(ALLkev, data, delimiter=';')
                ALLkev.close()
            if z > 1:
                with open('data/{}/{}/ALLkev_psd_energy_{}.txt' .format(pmtloc,scintloc,args.output_scintillator[0]), 'a') as ALLkev:
                    np.savetxt(ALLkev, data, delimiter=';')
                ALLkev.close()
            """    
                
                
            psd_mask = (psd < args.psd_cut[1]) & (psd > args.psd_cut[0]) #Both psd and energy cuts for sorting data
            energy_mask = (energy < args.energy_target[1]) & (energy > args.energy_target[0]) 
            
            mask = psd_mask & energy_mask
            """
            masked_psd = psd[mask]
            masked_energy = energy[mask]

            #print(waveforms.shape)
            #print("Mask shape: ",mask.shape)

            masked_waveforms = waveforms[mask]
            #print(masked_waveforms,masked_waveforms.shape)
            #print("Mask sum: ",mask.sum())
            """
            if mask:
                #print(psd == psd_mask)
                masked_psd.append(psd)
                masked_energy.append(energy)
                masked_waveforms.append(voltage)        #may run into problem like samps_arr
                                                        #leave for now to check if working
                #print("ok")    
    f.close()
    #print(masked_waveforms)
    #exit(0)     #exit program
    
    if args.plot is True:
        ##########################
        #####ENERGY HIST HERE#####

        #plt.subplot(1,2,1)
        #plt.hist(energy, bins=400, range=[0,400], color='black')#4096
        #plt.xlim(0,400)
        #plt.subplot(1,2,2) 

        if args.psd_cut is not None:
            psd = np.array(psd_arr)
            energy = np.array(energy_arr)
            mask = (psd < args.psd_cut[1]) & (psd > args.psd_cut[0])
            #print(mask)
            #masked_psd = psd_arr[mask]      #redundant array?
            #masked_energy = np.array(energy_arr[mask]) #redundant array?

            plt.subplot(1,2,1)
            plt.scatter(energy, psd, color='black')
            plt.ylim(0,1)
            plt.xlabel("Energy")
            plt.ylabel("PSD")

            plt.subplot(1,2,2) 
            plt.hist(energy[mask], bins=100, color='black')#4096
            #plt.xlim(0,1000)
            plt.xlabel("Energy")
            plt.ylabel("Counts")
            plt.show()
                    
        else:
            #print(len(energy_arr),len(psd_arr))
            plt.scatter(energy_arr, psd_arr, color='black')
            plt.ylim(0,1)
            plt.xlabel("Energy")
            plt.ylabel("PSD")
            plt.show() 
                    
        if args.psd_cut is not None and args.energy_target is not None:
            psd = np.array(psd_arr)
            energy = np.array(energy_arr)
            print(len(energy_arr),len(energy))
            mask = (psd < args.psd_cut[1]) & (psd > args.psd_cut[0])
            #plt.subplot(1,2,1)
            _, bins, _ = plt.hist(energy, bins=100, color='black') #sets the standard bin count for all energy (for use in masked histogram)
            #plt.subplot(1,2,2) 
            #plt.hist(energy[psd_mask], bins=bins, color='black')
            #plt.hist(energy[psd_mask & energy_mask], bins=bins, color='orange')
            #plt.show()
            plt.subplot(1,2,1) 
            plt.scatter(energy, psd, color='black')
            plt.ylim(0,1)
            plt.subplot(1,2,2)
            plt.hist(energy[mask], bins=bins, color='black')#4096
            #plt.xlim(0,args.energy_target[1])
            plt.xlabel("Energy")
            plt.ylabel("Counts")
            plt.subplot(1,2,1)
            plt.scatter(masked_energy,masked_psd, color='orange')
            plt.xlabel("Energy")
            plt.ylabel("PSD")
            plt.subplot(1,2,2)
            plt.hist(masked_energy, bins=bins, color='orange')
            #plt.xlim(0,args.energy_target[1])

            d = np.array([masked_energy,masked_psd])
            d = d.T
            np.savetxt('data/{}/{}/MASKEDkev_psd_energy_{}.txt'.format(pmtloc,scintloc,args.output_scintillator[0]), d, delimiter=';')
            plt.show()
    
    samps = 0 #Samples gathered
    numosamps = 0 #Number of Samples wanted
    if args.number_of_waveforms is None: #Automates samples gathered for saving later on
        numosamps = len(energy_arr)
    if args.number_of_waveforms is not None:
        if args.number_of_waveforms[0] > len(energy_arr) or args.number_of_waveforms[0] < 1:
            parser.error('Specified Samples out of Range. . . Enter a number between 1 and the file length [{}]'.format(len(energy_arr)))
        if args.number_of_waveforms[0] <= len(energy_arr):
            numosamps = args.number_of_waveforms[0]
   
    
    #print(stripped_array)
    #if args.strip_array is not None:
    #    #print(stripped_array)
    #    pmtloc = args.pmt[0]
    #    scintloc = args.scintillator[0]
    #    stripped_data = np.array(stripped_array)
    #   stripped_data.tofile('data/{}/{}/stripped_data.bin'.format(pmtloc,scintloc))
    

    #samps = 0    
    #numosamps = 10
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
        print("Set [",samps,"/",numosamps,"] of [",len(energy_arr),"] . . . Saved")
        #######"Loading Bar"###################
