# crio-utils

This repository contains miscellaneous script for various purposes.

## gen_cfg.py

This script generates a configuration file from a set of files and the 
FPGA C API generated header.

### Help
    $ ./gen_cfg.py -h
 
### Running example
    $ ./gen_cfg.py ./gen_cfg_example/NiFpga_CrioLinux_ALL.h 1 24 -s ./gen_cfg_example/

### Notes
    $ gen_cfg_example/
    $ ├── BI.list
    $ ├── NiFpga_CrioLinux_ALL.h
    $ └── RT.list
 
 * NiFpga_CrioLinux_ALL.h: Header file generated with FPGA C API
 * RT.list: If SM is enabled, this file must exist, and should contain the order of the variables in the labview RT VI
 * (BI).list: If exists a BI (BI) in the *.h file, a file with its name will be searched for. This file contains the bit <-> name mappings