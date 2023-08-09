Pulse-Waveform Database Readme
------------------------------

This code consists of 

    PRIMARY SCRIPTS:
    
    * data_runner.py  --  this script reads and runs the .bin files from raw and plots psd and energy graphs for the sorting and saving of waveforms
    * plotter.py  --  this script takes saved waveforms and plots an average waveform (or it can plot one specific waveform)
    
    
    SECONDARY SCRIPTS:
    
    * database_functions.py -- this script contains the functions utilized by the two primary scripts
    * main.sh -- this is a bash script that will run the primary scripts with preset commands to sort and save data
    

Important Notes:

    * PSD(a variable to characterize an individual pulse shape, specific to a scintillator) is calculated from

        (Energy Long Gate - Energy Short Gate) / (Energy Long Gate)


Examples:

1.
    python3 data_runner.py -p hamamatsu_r12699 -s scionix_naitl_csina -y co60 --plot
    
    *This example is similar to the first run of the data_runner.py script. This will return a psd v. energy heatplot and an energy histogram to help inform psd and energy cuts for sorting and saving.
    
2.
    python3 data_runner.py -p hamamatsu_r12699 -s scionix_naitl_csina -y co60 -c 0.15 .35 -e 1210 1400 -o 1332kev_peak_naitl -w 100 --plot
    
    *This example is similar to the second run of the data_runner.py script. This will sort waveforms and return a psd v. energy heatplot and an energy histogram with specified cuts demonstrated as overlays on the graphs. This run will also save sorted waveforms (the number saved determined by the -w arg).
    
3. 
    python3 plotter.py -i data/hamamatsu_r12699/scionix_naitl_csina/co60_data_1332kev_peak_naitl_* -p hamamatsu_r12699 -s scionix_naitl_csina -o 1332kev_naitl --show
    
    *This example is similar to the first run of the plotter.py script. This will take saved waveforms of a similar specified file name and plot an average waveform. This run will also return information on the waveform such as PSD average, area under the curve, and T90. Additionally, this run will save that average waveform (the file name will be the -o arg + _Average_Waveform, e.g., 1332kev_naitl_Average_Waveform).


Command Line Arguments Guide:

    General (works on both scripts):
        -h (--help)

    data_runner.py Args:
        -a (--add)
        -p (--pmt)
        -s (--scintillator)
        -c (--psd-cut)
        -y (--source)
        -o (--output-file-name)
        -b (--baseline)
        -e (--energy-target)
        -w (--number-of-waveforms)
        -l (--list-available-input-files)
        -x (--plot)
     
    plotter.py Args:
        -i (--input-data)
        -p (--pmt-used)
        -s (--scintillator)
        -z (--show)
        -o (--output-file-name)



FAQs:

Q: What is main.sh for?
A: main.sh is a bash script that will run each .bin file for each scintillator and photosensor for the 88, 662, and 1332 keV energy peaks. It will also plot the average waveforms for each of those peaks from each run. It can be used as an example of how to run the primary scripts.

Q: What does the -a (--add) arg do in data_runner.py?
A: The --add arg in the data_runner.py script is used for adding new .bin data files to the raw data repository (the input for this arg will be the file location of the new .bin file). These files can later be used for running data. To use a new .bin file, it is not necessary to add it more than once. Once added, the .bin file that will be run is selected automatically based on inputs for the -p, -s, and -y args when running data_runner.py (since its save location is determined using these args).

    EXAMPLE:    You have an un-added .bin file called file.bin and it is located in the folder named example_folder. To add it, use
    
                        python3 data_runner.py -a example_folder/file.bin -p example_pmt -s example_scintillator -y example_source
    
                Now you have added file.bin to the raw repository, and it has been saved to
                
                        raw/example_pmt/example_scintillator/example_source.bin

                To use file.bin for more runs of data_runner.py, use the same inputs for the -p, -s, and -y args as when you used to add file.bin to raw.
                
                        -p example_pmt
                        -s example_scintillator
                        -y example_source

Q: 
A: 