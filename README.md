# crio-utils

This repository contains miscellaneous script for various purposes.

## gen_cfg.py

This script generates a configuration file from a set of files and the 
FPGA C API generated header.

### Help
 $ ./gen_cfg.py -h
 
### Running example
 $ ./gen_cfg.py ./gen_cfg_example/NiFpga_CrioLinux_ALL.h 1 24 -s ./gen_cfg_example/