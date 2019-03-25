# crio-utils

This repository contains miscellaneous script for various purposes.

## gen_cfg.py

This script generates a configuration file from a set of files and the 
FPGA C API generated header.

### Help
    $ ./gen_cfg.py -h
 
### Running example
    $ ./gen_cfg.py ./gen_cfg_example/NiFpga_fpga_all_example.h -s ./gen_cfg_example/ -u


### Notes
    $ gen_cfg_example/
    $ ├── BI.list
    $ ├── NiFpga_fpga_all_example.h
    $ └── RT.list
 
 * NiFpga_fpga_all_example.h: Header file generated with FPGA C API
 * RT.list: If SM is enabled, this file must exist, and should contain the order of the variables in the labview RT VI
 * (BI).list: If exists a BI (BI) in the *.h file, a file with its name will be searched for. This file contains the bit <-> name mappings

#### RT variable naming in RT.list file
Must abide by the following syntax RT_VARTYPE_VARNAMEX. VARNAME must be one of the following
 * AI, AO, BI, BO

X can be a unique number assigned by the user. The VARTYPE has to be one of the following
 * BOL, DBL, SGL, I64, I32, I16, I08, U64, U32, U16, U08


## labview2018vm.sh

This script launches the VM that has the Labview 2018 32-bits running on a windows 10 64-bit machine (tesla)

### Running example
    $ ./labview2018vm