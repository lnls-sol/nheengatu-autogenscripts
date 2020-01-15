#!/bin/sh

command -v rdesktop >/dev/null 2>&1 || 
    { echo >&2 "\033[0;31mrdesktop application required to open the Virtual Machine interface.\033[0;30m"
      echo "Install with the following command:\n<sudo apt install rdesktop>"; exit 1; 
      }


rdesktop -g 1900x1040 tesla-VM
#tesla-VM IP : 10.2.103.35
