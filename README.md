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


## labview2018vm.sh

This script launches the VM that has the Labview 2018 32-bits running on a windows 10 64-bit machine (tesla)

### Running example
    $ ./labview2018vm