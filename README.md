# crio-utils

This repository contains miscellaneous script for various purposes.

## gen_cfg.py

This script generates a configuration file from a set of files and the 
FPGA C API generated header.

### Help
    $ ./gen_cfg.py -h
 
    
### cfg.csv template generation example
    
    $ ./gen_cfg.py -s ./gen_cfg_example/ -u --waveformkey waveform_ --binum 24 --extract
    $ ./gen_cfg.py -s ./gen_cfg_mbb_example/ --mbbikey MBBI --mbbokey MBBO --crio CRIO5 --loc A -u --extract
    $ ./gen_cfg.py -s ./gen_cfg_example_9045/ --mbbikey MBBI --mbbokey MBBO --crio CRIO5 --loc A -u --extract
    
### cfg.ini and EPICS substitutions generation examples

    $ ./gen_cfg.py -s ./gen_cfg_example/ -u --waveformkey waveform_ --binum 24
    $ ./gen_cfg.py -s ./gen_cfg_mbb_example/ --mbbikey MBBI --mbbokey MBBO --crio CRIO5 --loc A -u
    $ ./gen_cfg.py -s ./gen_cfg_example_9045/ --mbbikey MBBI --mbbokey MBBO --crio CRIO5 --loc A -u
    $ ./gen_cfg.py --bikey BI_  --src example3/ --bokey BO --binum 4 -u --loc B --crio CRIO05


### Notes
    $ gen_cfg_example/
    $ ├── NiFpga_fpga_all_example.lvbitx
    $ ├── NiFpga_fpga_all_example.h
    $ ├── cfg.csv
    $ └── RT.list
 
 * NiFpga_fpga_all_example.h: Header file generated with FPGA C API
 * RT.list: If SM is enabled, this file must exist, and should contain the order of the variables in the labview RT VI (content automatically generated)
 * NiFpga_fpga_all_example.lvbitx: bit stream. It will only be copied by the script to the destination folder
 * cfg.csv : example of an already filled cfg.csv file. The script generates a template that will be filled by the user

#### RT variable naming in RT.list file
Must abide by the following syntax RT_VARTYPE_VARNAMEX. VARNAME must be one of the following
 * AI, AO, BI, BO, WF

X can be a unique number assigned by the user. The VARTYPE has to be one of the following
 * BOL, DBL, SGL, I64, I32, I16, I08, U64, U32, U16, U08

In case of waveforms (WF), the variable name must be followed by the array number of elements

## crio-ioc.cmd

This is the standard cmd file. Can be used as is.

## labview2018vm.sh

This script launches the VM that has the Labview 2018 32-bits running on a windows 10 64-bit machine (tesla)

### Running example
    $ ./labview2018vm
