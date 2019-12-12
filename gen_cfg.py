#!/usr/bin/python3


###############################################################################
#
# This software is distributed under the following ISC license:
#
# Copyright © 2017 BRAZILIAN SYNCHROTRON LIGHT SOURCE <sol@lnls.br>
#   Dawood Alnajjar <dawood.alnajjar@lnls.br>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS.  IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION
# OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN
# CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#
# CRIO address and template extraction/generation script
#
###############################################################################



import re
import sys
import argparse
import collections
import os 
from string import Template
from shutil import copyfile
import glob
import datetime
from termcolor import colored
import shutil
    
### HELPER FUNCTIONS
def printToCFGFile(f, cfgkey, items, csv, use_csv):
    f.write("[{}]\n".format(cfgkey))
    for key,value in items.items():
        if (use_csv == 1):
            if (cfgkey == 'BI_VECTOR'):
                if value in csv:
                    f.write("{}={}\n".format(key,value)) 
            elif key in csv:
                f.write("{}={}\n".format(key,value)) 
        else:
            f.write("{}={}\n".format(key,value))    
          
    f.write("\n\n")     


def printToReqFile(f, keys, csv, bl, eq):
    for key,value in keys.items():
        if key in csv:
            if (csv[key]['AUTOSAVE'] == 1):
                f.write("{0}:{1}:{2}\n".format(bl, eq, csv[key]['EQ']))   

def printToInitFile(f, keys, csv, bl, eq):
    for key,value in keys.items():
        if key in csv:
            if (csv[key]['INITIALIZE'] == 1):
                f.write("dbpf {0}:{1}:{2} {3}\n".format(bl, eq, csv[key]['EQ'], csv[key]['INIT VAL']))   
            

def buildSub(tplhdr, tplbdy, beamline, dtype, pins, dbtemplate, fname, csv):
    tpls = tplhdr.format(dbtemplate)
    if(fname == "scaler"): #SCALER
        for key in pins.keys():
            if key in csv:
                if (csv[key]['DISABLE'] == '1'):
                    print(colored("WARNING: Key {0} disabled. Is this intentional?".format(key), 'red')) 
                    continue
                else:
                    tpls = tpls + tplbdy.format(beamline, csv[key]['EQ'], dtype, key, csv[key]['DESC'])
            else:
                print(colored("WARNING: Found {0} in header but not in csv. Is this intentional?".format(key), 'red'))              
    else: # Waveform
        if (fname == "waveform"):
            for indx, key in enumerate(pins.keys()):
                if key in csv:
                    if (csv[key]['DISABLE'] == '1'):
                        print(colored("WARNING: Key {0} disabled. Is this intentional?".format(key), 'red')) 
                        continue
                    else:                
                        tpls = tpls + tplbdy.format(beamline, csv[key]['EQ'], dtype, key, csv[key]['TypeEPICS'], csv[key]['SIZE'],csv[key]['DESC'])
                else:
                    print(colored("WARNING: Found {0} in header but not in csv. Is this intentional?".format(key), 'red'))                      
        else: # MBBI
            if (fname == "mbbi"):
                for indx, key in enumerate(pins.keys()):
                    if key in csv:
                        if (csv[key]['DISABLE'] == '1'):
                            print(colored("WARNING: Key {0} disabled. Is this intentional?".format(key), 'red')) 
                            continue
                        else:                    
                            tpls = tpls + tplbdy.format(beamline        , csv[key]['EQ']  , csv[key]['DESC'], \
                                                key             , dtype           , csv[key]['SCAN'], \
                                                csv[key]['ZRST'], csv[key]['ZRVL'], csv[key]['ZRSV'], \
                                                csv[key]['ONST'], csv[key]['ONVL'], csv[key]['ONSV'], \
                                                csv[key]['TWST'], csv[key]['TWVL'], csv[key]['TWSV'], \
                                                csv[key]['THST'], csv[key]['THVL'], csv[key]['THSV'], \
                                                csv[key]['FRST'], csv[key]['FRVL'], csv[key]['FRSV'], \
                                                csv[key]['FVST'], csv[key]['FVVL'], csv[key]['FVSV'], \
                                                csv[key]['SXST'], csv[key]['SXVL'], csv[key]['SXSV'], \
                                                csv[key]['SVST'], csv[key]['SVVL'], csv[key]['SVSV'], \
                                                csv[key]['EIST'], csv[key]['EIVL'], csv[key]['EISV'], \
                                                csv[key]['NIST'], csv[key]['NIVL'], csv[key]['NISV'], \
                                                csv[key]['TEST'], csv[key]['TEVL'], csv[key]['TESV'], \
                                                csv[key]['ELST'], csv[key]['ELVL'], csv[key]['ELSV'], \
                                                csv[key]['TVST'], csv[key]['TVVL'], csv[key]['TVSV'], \
                                                csv[key]['TTST'], csv[key]['TTVL'], csv[key]['TTSV'], \
                                                csv[key]['FTST'], csv[key]['FTVL'], csv[key]['FTSV'], \
                                                csv[key]['FFST'], csv[key]['FFVL'], csv[key]['FFSV'], \
                                                csv[key]['COSV'], csv[key]['UNSV'] )
                    else:
                        print(colored("WARNING: Found {0} in header but not in csv. Is this intentional?".format(key), 'red'))        
            else: # MBBO
                if (fname == "mbbo"):
                    for indx, key in enumerate(pins.keys()):
                        if key in csv:
                            if (csv[key]['DISABLE'] == '1'):
                                print(colored("WARNING: Key {0} disabled. Is this intentional?".format(key), 'red')) 
                                continue
                            else:                        
                                tpls = tpls + tplbdy.format(beamline        , csv[key]['EQ']  , csv[key]['DESC'], \
                                                    key             , dtype           , \
                                                    csv[key]['ZRST'], csv[key]['ZRVL'], csv[key]['ZRSV'], \
                                                    csv[key]['ONST'], csv[key]['ONVL'], csv[key]['ONSV'], \
                                                    csv[key]['TWST'], csv[key]['TWVL'], csv[key]['TWSV'], \
                                                    csv[key]['THST'], csv[key]['THVL'], csv[key]['THSV'], \
                                                    csv[key]['FRST'], csv[key]['FRVL'], csv[key]['FRSV'], \
                                                    csv[key]['FVST'], csv[key]['FVVL'], csv[key]['FVSV'], \
                                                    csv[key]['SXST'], csv[key]['SXVL'], csv[key]['SXSV'], \
                                                    csv[key]['SVST'], csv[key]['SVVL'], csv[key]['SVSV'], \
                                                    csv[key]['EIST'], csv[key]['EIVL'], csv[key]['EISV'], \
                                                    csv[key]['NIST'], csv[key]['NIVL'], csv[key]['NISV'], \
                                                    csv[key]['TEST'], csv[key]['TEVL'], csv[key]['TESV'], \
                                                    csv[key]['ELST'], csv[key]['ELVL'], csv[key]['ELSV'], \
                                                    csv[key]['TVST'], csv[key]['TVVL'], csv[key]['TVSV'], \
                                                    csv[key]['TTST'], csv[key]['TTVL'], csv[key]['TTSV'], \
                                                    csv[key]['FTST'], csv[key]['FTVL'], csv[key]['FTSV'], \
                                                    csv[key]['FFST'], csv[key]['FFVL'], csv[key]['FFSV'], \
                                                    csv[key]['IVOA'], csv[key]['IVOV'], \
                                                    csv[key]['COSV'], csv[key]['UNSV'] )
                        else:
                            print(colored("WARNING: Found {0} in header but not in csv. Is this intentional?".format(key), 'red'))                        
                else: #AO, AI, BO, BI                  
                    for indx, key in enumerate(pins.keys()):
                        if (key == 'BI_VECTOR'):
                            continue
                        if key in csv:
                            if (csv[key]['DISABLE'] == '1'):
                                print(colored("WARNING: Key {0} disabled. Is this intentional?".format(key), 'red')) 
                                continue
                            else:                        
                                tpls = tpls + tplbdy.format(beamline, csv[key]['EQ'], dtype, key, csv[key]['DESC'])
                            if ( not csv[key]['EQ']):
                                print(colored("WARNING: EQ of {0} is empty. Is this intentional?".format(key), 'red'))
                        else:
                            print(colored("WARNING: Found {0} in header but not in csv. Is this intentional?".format(key), 'red'))
            

    tpls = tpls + "\n}"
    with open("{}/{}.db.sub".format(args.dst, fname) , "w") as f:
        print("Generating {}/{}.db.sub file".format(args.dst, fname))
        f.write(tpls)     


description = 'This programs extracts the address in the header file generated by the FPGA C API, and generates ini and template files for EPICS.'

header = '\n\
;-----------------------------------------------------------------\n\
; Automatically generated ini file for CRIO Nheengatu library\n\
; CNPEM - LNLS - SIRIUS \n\
; Author : Dawood Alnajjar \n\
; ----------------------------------------------------------------\n\
; Generate on {0}\n\
;\n\
;INI records:\n\
;  - [Settings]\n\
;  - [BIAddresses]\n\
;  - [BI_VECTOR]\n\
;  - [AO]\n\
;  - [AI]\n\
;  - [FXP_XX]\n\
;  - [BO]\n\
;  - [SCALERS]\n\
;  - [SCALERXX]\n\
;  - [WAVEFORMS]\n\
;  - [WAVEFORMXX]\n\
;  - [MBBI]\n\
;  - [MBBO]\n\
;\n\
;      - Settings:\n\
;        The settings required to setup the CRIO environment are here\n\
;           - Destination Crio IP: The IP address of the target CRIO\n\
;                        For safety, our intention is to keep this\n\
;                        IP as the loopback address (127.0.0.1)\n\
;           - Path: is the path to the bitfile that will be used to configure\n\
;                   the FPGA of the target CRIO.\n\
;           - Bitfile Name: Is the name of the bitfile\n\
;           - Signature: Is the Signature of that specific bitfile\n\
;           - Use Shared Memory: Set to 1 if labviewRT will open a shared memory\n\
;           - Shared Memory Path: If Use Shared Memory is set to 1, then this path\n\
;                       will be used.\n\
;           - Shared Memory Size: If Use Shared Memory is set to 1, then the size is used\n\
;      - WAVEFORMS:\n\
;        Nheengatu will look for the details of every wavefrom in another record\n\
;        The Waveform fields are \n\
;          - <Type> : can be I08, I16, I32, I64, U08, U16, U32, U64, SGL, DBL \n\
;          - <Address> : RT index \n\
;          - <Size> : Number of elements in the array \n\
;      - BIAddresses:\n\
;        Address of BI vector (upto 64-bits) and other boolean indicators. Must have BI_VECTOR as the single item.\n\
;      - BI_VECTOR:\n\
;        A list with all the BIs that will be read by Nheengatu and their respective index\n\
;      - AO:\n\
;        A list with all the AOs that will be written by Nheengatu and their respective addresses\n\
;      - AI:\n\
;        A list with all the AIs that will be read by Nheengatu and their respective addresses\n\
;      - BO:\n\
;        A list with all the BOs that will be written by Nheengatu and their respective addresses\n\
;      - SCALERS:\n\
;        A list with all the BOs that will be read by Nheengatu and their respective addresses.\n\
;        Each item in this list will need a new record with the following parameters\n\
;          - <Gate> : Gate array address\n\
;          - <Number of Counters> : Number of counters implemented\n\
;          - <Done> : address of the done flag\n\
;          - <OneShot>: Address of the oneshot flag\n\
;          - <Counters> : Address of the counter array\n\
;          - <Preset Values>: Address of the preset array\n\
;          - <Enable>: address if the enable array\n\
;      - FXP_XX:\n\
;        For each FXP in AI/AO, and FXP record is needed with the following parameters\n\
;          - <Word Length> (currently fixed to 64) \n\
;          - <Sign> can be 0 (unSigned) or 1 (Signed) \n\
;          - <Integer Word Length> can be any value between 0 and 64. \n\
;      - MBBI:\n\
;        A list with all the MBBIs that will be read by Nheengatu and their respective addresses\n\
;      - MBBO:\n\
;        A list with all the MBBOs that will be written by Nheengatu and their respective addresses\n\
;\n\
;\n\
;Naming Considerations:\n\
;    FPGA Variables: \n\
;        Fixed point AI and AO variables should start with "FXP" keyword. \n\
;        Every FXP variable need to have the following attributes defined \n\
;        in another record as mentioned above.  \n\
;\n\
; \n\
; \n\
;    RT Variables:\n\
;        The keyword RT_ is reserved for variables that are defined \n\
;        in labview RT. Do not use this reserved word in your names\n\
;        unless it is an RT variable, otherwise it will be ignored!\n\
;        In case of AI, AO, BI, BO, WF, Keywords for realtime double, single, \n\
;        Signed 8, 16, 32, 64 and unSigned 8, 16, 32, 64 are defined as follows\n\
;        Double          : RT_DBL_<NAME>\n\
;        Single          : RT_SGL_<NAME>\n\
;        UnSigned 64 bit : RT_U64_<NAME>\n\
;        UnSigned 32 bit : RT_U32_<NAME>\n\
;        UnSigned 16 bit : RT_U16_<NAME>\n\
;        UnSigned 08 bit : RT_U08_<NAME>\n\
;        Signed 64 bit   : RT_I64_<NAME>\n\
;        Signed 32 bit   : RT_I32_<NAME>\n\
;        Signed 16 bit   : RT_I16_<NAME>\n\
;        Signed 08 bit   : RT_I08_<NAME>\n\
;\n\
;\n\
;Checks implemented in the library:\n\
; Checking for same address / index within a category has been\n\
; implemented. An exception is throw upon occurance.\n\
;\n\
;\n\
;Note that the binary input address that comes from the FPGA is always set to\n\
;BI_VECTOR. The library looks for this specific string, so it must be BI_VECTOR although \n\
;you may have named it differently in the FPGA VI.\n\
;-----------------------------------------------------------------\n\
\n\n\n\n'


# initiate the parser
parser = argparse.ArgumentParser(description=description)

# Input parameters
parser.add_argument("-u", "--useSM", help="Use shared memory", action='store_true')
parser.add_argument("-d", "--dst", default="crio-ioc", help="Name of the output folder. Default is <crio-ioc>")
parser.add_argument( "-p", "--path", help="Bitfile path. Default is </usr/local/epics/apps/config/crio-ioc/>", default = '/usr/local/epics/apps/config/crio-ioc/')
parser.add_argument("-s", "--src", help="Folder containing all files necessary for ini/template generation", default = '')
parser.add_argument("--binum", help="The total number of BI variables. Default is <0>", default = '0')
parser.add_argument("--extract", help="Extract data from headerfile", action='store_true')
parser.add_argument("--ip", help="Destination IP of the CRIO. Default is <127.0.0.1>", default = '127.0.0.1')
parser.add_argument("--smfname", help="Shared memory file path and name", default = '/labview_linux_sm')
parser.add_argument("--smsize", help="Shared memory size. Default is <4096>", default = '4096')
parser.add_argument("--aikey", help="AI keyword that any AI variable will start with in the headerfile. Default is <ai>", default = 'ai')
parser.add_argument("--aokey", help="AO keyword that any AO variable will start with in the headerfile Default is <ao>", default = 'ao')
parser.add_argument("--bokey", help="BO keyword that any BO variable will start with in the headerfile. Default is <bo>", default = 'bo')
parser.add_argument("--bikey", help="BI keyword that any BI variable will start with in the headerfile. Default is <BI>", default = 'BI')
parser.add_argument("--mbbikey", help="mbbi keyword that any mbbi variable will start with in the headerfile. Default is <mbbi>", default = 'mbbi')
parser.add_argument("--mbbokey", help="mbbo keyword that any mbbo variable will start with in the headerfile. Default is <mbbo>", default = 'mbbo')
parser.add_argument("--fxpkey", help="Fixedpoint keyword that any AI/AO variable will have after that AI/AO keyword in the headerfile. Default is <fxp>", default = 'fxp')
parser.add_argument("--scalerkey", help="Scaler keyword that any Scaler variable will be followed with in the headerfile. Default is <SCALER>", default = 'SCALER')
parser.add_argument("--waveformkey",help="Waveform keyword that any Waveform variable will be followed with in the headerfile. Default is <WF>", default = 'WF')
parser.add_argument("--beamline", help="Name of the beamline (for template file generation). Default is <SOL>", default = 'SOL')
parser.add_argument("--bidtyp", help="DTYPE of BI record", default = 'CrioBI')
parser.add_argument("--aidtyp", help="DTYPE of AI record", default = 'CrioAI')
parser.add_argument("--bodtyp", help="DTYPE of BO record", default = 'CrioBO')
parser.add_argument("--aodtyp", help="DTYPE of AO record", default = 'CrioAO')
parser.add_argument("--mbbodtyp", help="DTYPE of MBBO record", default = 'CrioMBBO')
parser.add_argument("--mbbidtyp", help="DTYPE of MBBI record", default = 'CrioMBBI')
parser.add_argument("--wfdtyp", help="DTYPE of WF record", default = 'CrioWAVEFORM')
parser.add_argument("--crio", help="Name of the CRIO. Default is <CRIO1>", default = 'CRIO1')
parser.add_argument("--loc", help="Name of the location of the CRIO. Default is Cabine <A>", default = 'A')
parser.add_argument("--scalerdtyp", help="DTYPE of Scaler record", default = 'CRIO Scaler')
parser.add_argument("--cfgcsv", help="csv file name. Default=cfg.csv", default = 'cfg.csv')
parser.add_argument("--refcsv", help="when extract, use existing csv file <default=cfg.csv> as reference when extracting the new one.", action='store_true')
parser.add_argument("--delimiter", help="Delimiter in csv file. Default is ,", default = ',')




if len(sys.argv)==1:
    parser.print_help(sys.stderr)
    sys.exit(1)
    
    
# read arguments from the command line
args = parser.parse_args()


dlm = args.delimiter
    
biaddr = {}
boaddr = {}
aoaddr = {}
mbbiaddr = {}
mbboaddr = {}
aiaddr = {}
rtlist = []
bidict = collections.OrderedDict()
scalers = collections.defaultdict(dict)
waveforms = collections.defaultdict(dict)
fxps  = collections.defaultdict(dict)
csvai = collections.defaultdict(dict)
csvbi = collections.defaultdict(dict)
csvbo = collections.defaultdict(dict)
csvao = collections.defaultdict(dict)
csvmbbi = collections.defaultdict(dict)
csvmbbo = collections.defaultdict(dict)
csvwf = collections.defaultdict(dict)
csvslr = collections.defaultdict(dict)

csvairef = collections.defaultdict(dict)
csvbiref = collections.defaultdict(dict)
csvboref = collections.defaultdict(dict)
csvaoref = collections.defaultdict(dict)
csvmbbiref = collections.defaultdict(dict)
csvmbboref = collections.defaultdict(dict)
csvwfref = collections.defaultdict(dict)
csvslrref = collections.defaultdict(dict)

settings = {'Destination Crio IP' : args.ip,
            'Path':args.path,
            'Use Shared Memory': 1 if(args.useSM) else 0,
            'Shared Memory Path': args.smfname,
            'Shared Memory Size': args.smsize}
rtvarCount = 0;
fpgavarCount = 0;


if not os.path.exists(args.src):
    print("Source folder not found <{0}>. Is this the correct path?".format( args.src))
    sys.exit()
        
# search for header file
headerFilesFound = glob.glob("{0}/*.h".format(args.src));
if (len(headerFilesFound) > 1): 
    print("Found {0} header files in {1} folder. Exclude others and try again.".format(len(headerFilesFound), args.src))
    print(headerFilesFound)
    sys.exit()

with open(headerFilesFound[0]) as f:
    lines = f.readlines()

    

# Prepare output folder
if not (args.extract) : 
    if os.path.exists(args.dst):
        os.system("rm -rf {0}".format(args.dst)) 
    os.makedirs(args.dst)
    os.makedirs(args.dst+"/reference")
    callCommand = " ".join(sys.argv)
    with open(args.dst+"/reference/command.sh", "w") as f:
        f.write("#!/bin/bash\n")  
        f.write(callCommand)        
    copyfile(args.src+"/"+args.cfgcsv, args.dst+"/reference/"+args.cfgcsv)
    shutil.copy2(headerFilesFound[0], args.dst+"/reference")
    if (args.useSM):
        if (os.path.isfile(args.src+"/RT.list")):
            copyfile(args.src+"/RT.list", args.dst+"/reference/RT.list")
        else :
            print('RT.list file not available while -u switch activated.')
            sys.exit()
else:
    if(os.path.isfile(args.src+"/"+args.cfgcsv)):
        copyfile(args.src+"/"+args.cfgcsv, args.src+"/cfg_old.csv")
    if not os.path.exists(args.dst):
        os.makedirs(args.dst)
        
# extract data from header and RT.list whether extract is chosen or not.                           
for line in lines:

    # Extracting scaler data
    result = re.search('ControlArrayU32_PresetValues_('+args.scalerkey+'[a-zA-Z0-9_]*) = 0x([A-F0-9]{5})', line)
    if (result is not None):
        scalers[result.group(1)]['Preset Values']=(result.group(2))
        fpgavarCount += 1
    else:
        result = re.search('ControlBool_Enable_('+args.scalerkey+'[a-zA-Z0-9_]*) = 0x([A-F0-9]{5})', line)
        if (result is not None):
            scalers[result.group(1)]['Enable']=(result.group(2))
            fpgavarCount += 1    
        else:
            result = re.search('ControlArrayBool_Gate_('+args.scalerkey+'[a-zA-Z0-9_]*) = 0x([A-F0-9]{5})', line)
            if (result is not None):
                scalers[result.group(1)]['Gate']=(result.group(2))
                fpgavarCount += 1  
            else:
                result = re.search('ControlBool_OneShot_('+args.scalerkey+'[a-zA-Z0-9_]*) = 0x([A-F0-9]{5})', line)
                if (result is not None):
                    scalers[result.group(1)]['OneShot']=(result.group(2))
                    fpgavarCount += 1                  
                else:
                    result = re.search('IndicatorArrayU32_Counter_('+args.scalerkey+'[a-zA-Z0-9_]*) = 0x([A-F0-9]{5})', line)
                    if (result is not None):
                        scalers[result.group(1)]['Counters']=(result.group(2))
                        fpgavarCount += 1                   
                    else:
                        result = re.search('IndicatorArrayU32Size_Counter_('+args.scalerkey+'[a-zA-Z0-9_]*) = ([0-9]+)', line)
                        if (result is not None):
                            scalers[result.group(1)]['Number of Counters']=(result.group(2))
                            fpgavarCount += 1                 
                        else:
                            result = re.search('IndicatorBool_Done_('+args.scalerkey+'[a-zA-Z0-9_]*) = 0x([A-F0-9]{5})', line)
                            if (result is not None):
                                scalers[result.group(1)]['Done']=(result.group(2))
                                fpgavarCount += 1                    

    # Extracting waveform data
    result = re.search('IndicatorArray(I8|U8|I16|U16|I32|U32|I64|U64|Sgl)_('+args.waveformkey+'[a-zA-Z0-9_]*) = 0x([A-F0-9]{5})', line)
    if (result is not None):
        waveforms[result.group(2)]['Address']=(result.group(3))
        if (result.group(1) == 'I8'):
            waveforms[result.group(2)]['Type']=('I08')
            csvwf[result.group(2)]['TypeEPICS']='CHAR'
        else :
            if (result.group(1) == 'U8'):
                waveforms[result.group(2)]['Type']=('U08')
                csvwf[result.group(2)]['TypeEPICS']='UCHAR'
            else:
                waveforms[result.group(2)]['Type']=(result.group(1).upper())
                if (result.group(1) == 'U16'):
                    csvwf[result.group(2)]['TypeEPICS']='USHORT'
                else:
                    if (result.group(1) == 'I16'):
                        csvwf[result.group(2)]['TypeEPICS']='SHORT' 
                    else:
                        if (result.group(1) == 'I32'):
                            csvwf[result.group(2)]['TypeEPICS']='LONG'
                        else:
                            if (result.group(1) == 'U32'):
                                csvwf[result.group(2)]['TypeEPICS'] = 'ULONG'
                            else:
                                if (result.group(1) == 'Sgl'):
                                    csvwf[result.group(2)]['TypeEPICS'] = 'FLOAT'     
                                else : 
                                    csvwf[result.group(2)]['TypeEPICS'] = 'DOUBLE'                  
        fpgavarCount += 1
    else:
        result = re.search('IndicatorArray(I8|U8|I16|U16|I32|U32|I64|U64|Sgl)Size_('+args.waveformkey+'[a-zA-Z0-9_]*) = ([0-9]+)', line)
        if (result is not None):
            waveforms[result.group(2)]['Size']=(result.group(3))
            fpgavarCount += 1   
          
     
    
    # Extracting Settings                       
    result = re.search('_Signature\s*=\s*\"([A-F0-9]{32})\"', line)
    if (result is not None):
        settings['Signature']=(result.group(1))
    else:
        result = re.search('_Bitfile \"([a-zA-Z0-9_]+.lvbitx)\"', line)
        if (result is not None):
            settings['Bitfile Name']=(result.group(1))
            copyfile("{0}/{1}".format(args.src,result.group(1)), "{0}/{1}".format(args.dst,result.group(1)))
            copyfile("{0}/{1}".format(args.src,result.group(1)), "{0}/reference/{1}".format(args.dst,result.group(1)))
        else:
            # Extracting BI, BO, AI, AO, AI FXP and AO FXP
            #Extracting BI Vector if exists
            result = re.search('IndicatorU64_('+args.bikey+'[a-zA-Z0-9_]*) = 0x([A-F0-9]{5})', line)
            if (result is not None):
                biaddr["BI_VECTOR"]=(result.group(2))
                if (int(args.binum) != 0):
                    bidict = { i : "DI{0}".format(i) for i in range(int(args.binum)) }
                    fpgavarCount += int(args.binum)
                else:
                    print(colored("WARNING: Found BI vector in header file, and yet binum input parameter was set to 0. Is this intentional?",'red')) 
            else:
                # Extract boolean indicator (BI)
                result = re.search('IndicatorBool_('+args.bikey+'[a-zA-Z0-9_]*) = 0x([A-F0-9]{5})', line)
                if (result is not None):
                    biaddr[result.group(1)]=(result.group(2))
                    fpgavarCount += 1
                else:
                    # Extract Single precision floating point indicator (AI)
                    result = re.search('IndicatorSgl_('+args.aikey+'[a-zA-Z0-9_]*) = 0x([A-F0-9]{5})', line)
                    if (result is not None):
                        aiaddr[result.group(1)]=(result.group(2))
                        fpgavarCount += 1                
                    else:
                        # Extract Single precision floating point control (AO)
                        result = re.search('ControlSgl_('+args.aokey+'[a-zA-Z0-9_]*) = 0x([A-F0-9]{5})', line)
                        if (result is not None):
                            aoaddr[result.group(1)]=(result.group(2))         
                            fpgavarCount += 1
                        else:
                            # Extract boolean control (BO)
                            result = re.search('ControlBool_('+args.bokey+'[a-zA-Z0-9_]*) = 0x([A-F0-9]{5})', line)
                            if (result is not None):
                                boaddr[result.group(1)]=(result.group(2))                              
                                fpgavarCount += 1
                            else:
                                # Extract fixed point indicator (AI)
                                result = re.search('IndicatorU64_('+args.fxpkey+'([a-zA-Z0-9_])*) = 0x([A-F0-9]{5})', line)
                                if (result is not None):
                                    aiaddr["FXP_"+result.group(1)]=(result.group(3))
                                    fpgavarCount += 1   
                                else:
                                    # Extract fixed point control (AO)
                                    result = re.search('ControlU64_('+args.fxpkey+'([a-zA-Z0-9_])*) = 0x([A-F0-9]{5})', line)
                                    if (result is not None):
                                        aoaddr["FXP_"+result.group(1)]=(result.group(3))
                                        fpgavarCount += 1              
                                    else:
                                        # Extract MBB indicator (MBBO)
                                        result = re.search('IndicatorU16_('+args.mbbikey+'([a-zA-Z0-9_])*) = 0x([A-F0-9]{5})', line)
                                        if (result is not None):
                                            mbbiaddr[result.group(1)]=(result.group(3))
                                            fpgavarCount += 1   
                                        else:
                                            # Extract MBB control (MBBI)
                                            result = re.search('ControlU16_('+args.mbbokey+'([a-zA-Z0-9_])*) = 0x([A-F0-9]{5})', line)
                                            if (result is not None):
                                                mbboaddr[result.group(1)]=(result.group(3))
                                                fpgavarCount += 1                                         

#process RT variables if enabled

if (args.useSM):
    if (not os.path.isfile(args.src+"/RT.list")):
        print('RT.list file not available while -u switch activated. exiting...')
        sys.exit()
    rtlist = [rt.rstrip() for rt in open('{}/RT.list'.format(args.src))]
    for i, val in enumerate(rtlist):
        result = re.search('RT_MBI', val)
        if (result is not None):
            mbbiaddr[val]=i 
            rtvarCount += 1
        else: 
            result = re.search('RT_MBO', val)
            if (result is not None):
                mbboaddr[val]=i 
                rtvarCount += 1
            else:     
                result = re.search('RT_[A-Z0-9]{3}_AO', val)
                if (result is not None):
                    aoaddr[val]=i 
                    rtvarCount += 1
                else: 
                    result = re.search('RT_BOL_BO', val)
                    if (result is not None):
                        boaddr[val]=i
                        rtvarCount += 1   
                    else:         
                        result = re.search('RT_[A-Z0-9]{3}_AI', val)
                        if (result is not None):
                            aiaddr[val]=i
                            rtvarCount += 1 
                        else:           
                            result = re.search('RT_BOL_BI', val)
                            if (result is not None):
                                biaddr[val]=i
                                rtvarCount += 1     
                            else:
                                result = re.search('(RT_(I08|U08|I16|U16|I32|U32|I64|U64|SGL|DBL|BOL)_WF[a-zA-Z0-9_]*)[\s*]([0-9]+)', val)
                                if (result is not None):
                                    waveforms[result.group(1)]['Address']=i
                                    waveforms[result.group(1)]['Size']=result.group(3)
                                    waveforms[result.group(1)]['Type']=result.group(2).upper()
                                    
                                    if (result.group(2) == 'I08'):
                                        csvwf[result.group(1)]['TypeEPICS']='CHAR'
                                    else :
                                        if (result.group(2) == 'U08'):
                                            csvwf[result.group(1)]['TypeEPICS']='UCHAR'
                                        else:
                                            if (result.group(2) == 'U16'):
                                                csvwf[result.group(1)]['TypeEPICS']='USHORT'
                                            else:
                                                if (result.group(2) == 'I16'):
                                                    csvwf[result.group(1)]['TypeEPICS']='SHORT' 
                                                else:
                                                    if (result.group(2) == 'I32'):
                                                        csvwf[result.group(1)]['TypeEPICS']='LONG'
                                                    else:
                                                        if (result.group(2) == 'U32'):
                                                            csvwf[result.group(1)]['TypeEPICS'] = 'ULONG'
                                                        else:
                                                            if (result.group(2) == 'SGL'):
                                                                csvwf[result.group(1)]['TypeEPICS'] = 'FLOAT'     
                                                            else : 
                                                                if (result.group(2) == 'BOL'):
                                                                    csvwf[result.group(1)]['TypeEPICS']='CHAR'                                                     
                                                                else:
                                                                    csvwf[result.group(1)]['TypeEPICS'] = 'DOUBLE'                                                  
                                    rtvarCount += 1    
                                else:                    
                                    print("Found {} in RT.list file, but could not classify it.".format(val))       


print( "{} RT variables processed\n{} FPGA addresses extracted".format(rtvarCount, fpgavarCount))


# All tasks when extraction is not chosen
if not (args.extract) : 

    # Generate *.csv file      
    with open("{0}/{1}".format(args.src, args.cfgcsv) , "r") as f:
        lines = f.readlines()
        current = "None"
        for index, val in enumerate(lines):
            val = val.strip()
            removedDelimiter = val.replace(dlm , "")
            removedDelimiter = removedDelimiter.replace(" ", "")
            if (not removedDelimiter):
                continue
            lineSplit = val.split(dlm)
            result = re.search('^AI INI NAME', lineSplit[0])
            if (result is not None):
                current = "AI"
                continue
            else :
                result = re.search('^BI INI NAME', lineSplit[0])
                if (result is not None):
                    current = "BI"
                    continue
                else :
                    result = re.search('^BO INI NAME', lineSplit[0])
                    if (result is not None):
                        current = "BO"
                        continue
                    else :    
                        result = re.search('^AO INI NAME', lineSplit[0])
                        if (result is not None):
                            current = "AO"
                            continue
                        else :
                            result = re.search('^SCALER INI NAME', lineSplit[0])
                            if (result is not None):
                                current = "SCALER"
                                continue
                            else :               
                                result = re.search('^WAVEFORM INI NAME', lineSplit[0])
                                if (result is not None):
                                    current = "WAVEFORM"
                                    continue
                                else :               
                                    result = re.search('^MBBI INI NAME', lineSplit[0])
                                    if (result is not None):
                                        current = "MBBI"
                                        continue 
                                    else :               
                                        result = re.search('^MBBO INI NAME', lineSplit[0])
                                        if (result is not None):
                                            current = "MBBO"
                                            continue                                                                           
            if (current == 'AI'):
                #AI INI NAME,AI DB NAME,AI DESCRIPTION,AI Sign(FXP),AI Word Length(FXP),AI INTEGER LENGTH(FXP)
                #    0            1          2              3               4                   5
                csvai[lineSplit[0]]['EQ'] = lineSplit[1]
                csvai[lineSplit[0]]['DESC'] = lineSplit[2]
                csvai[lineSplit[0]]['DISABLE'] = lineSplit[6]
                result = re.search('FXP_', lineSplit[0])
                if (result is not None):
                    try:
                        csvai[lineSplit[0]]['Sign'] = int(lineSplit[3])
                        csvai[lineSplit[0]]['Word Length'] = int(lineSplit[4])
                        csvai[lineSplit[0]]['Integer Word Length'] = int(lineSplit[5])
                        fxps[lineSplit[0]]['Sign'] = int(lineSplit[3])
                        fxps[lineSplit[0]]['Word Length'] = int(lineSplit[4])
                        fxps[lineSplit[0]]['Integer Word Length'] = int(lineSplit[5])
                    except (ValueError) as err:
                        print ("Error with CSV entry {0} line {1}".format(lineSplit[0], index+1))
                        print(err)
                        sys.exit()  
                        
            else: 
                if (current == 'AO'):
                    #AO INI NAME,AO DB NAME,AO DESCRIPTION,AO Sign(FXP),AO Word Length(FXP),AO INTEGER LENGTH(FXP), AUTOSAVE, INITIALIZE, INIT VAL
                    #    0            1          2              3               4                   5                 6           7          8
                    csvao[lineSplit[0]]['EQ'] = lineSplit[1]
                    csvao[lineSplit[0]]['DESC'] = lineSplit[2]
                    csvao[lineSplit[0]]['AUTOSAVE'] = int(lineSplit[6]) 
                    csvao[lineSplit[0]]['INITIALIZE'] = int(lineSplit[7]) 
                    csvao[lineSplit[0]]['INIT VAL'] = int(lineSplit[8]) 
                    csvao[lineSplit[0]]['DISABLE'] = lineSplit[9]
                    result = re.search('FXP_', lineSplit[0])
                    if (result is not None): 
                        try:                   
                            csvao[lineSplit[0]]['Sign'] = int(lineSplit[3])
                            csvao[lineSplit[0]]['Word Length'] = int(lineSplit[4])
                            csvao[lineSplit[0]]['Integer Word Length'] = int(lineSplit[5]) 
                            fxps[lineSplit[0]]['Sign'] = int(lineSplit[3])
                            fxps[lineSplit[0]]['Word Length'] = int(lineSplit[4])
                            fxps[lineSplit[0]]['Integer Word Length'] = int(lineSplit[5])                              
                        except (ValueError) as err:
                            print ("Error with CSV entry {0} line {1}".format(lineSplit[0], index+1))
                            print(err)
                            sys.exit()                            
                else: 
                    if (current == 'BI'):
                        #BI INI NAME,BI DB NAME,BI DESCRIPTION
                        #    0            1          2             
                        csvbi[lineSplit[0]]['EQ'] = lineSplit[1]
                        csvbi[lineSplit[0]]['DESC'] = lineSplit[2]
                        csvbi[lineSplit[0]]['DISABLE'] = lineSplit[3]
                    else: 
                        if (current == 'BO'):
                            #BO INI NAME,BO DB NAME,BO DESCRIPTION, AUTOSAVE
                            #    0            1          2             3
                            csvbo[lineSplit[0]]['EQ'] = lineSplit[1]
                            csvbo[lineSplit[0]]['DESC'] = lineSplit[2]   
                            csvbo[lineSplit[0]]['AUTOSAVE']   = int(lineSplit[3])
                            csvbo[lineSplit[0]]['INITIALIZE'] = int(lineSplit[4]) 
                            csvbo[lineSplit[0]]['INIT VAL'] = int(lineSplit[5])  
                            csvbo[lineSplit[0]]['DISABLE'] = lineSplit[6]                            
                        else: 
                            if (current == 'WAVEFORM'):
                                #WAVEFORM INI NAME, DB NAME, DESCRIPTION, SIZE
                                #    0            1          2              3
                                csvwf[lineSplit[0]]['EQ'] = lineSplit[1]
                                csvwf[lineSplit[0]]['DESC'] = lineSplit[2]
                                csvwf[lineSplit[0]]['SIZE'] = int(lineSplit[3])
                                csvwf[lineSplit[0]]['DISABLE'] = lineSplit[4]
                            else: 
                                if (current == 'SCALER'):
                                    #SCALER INI NAME,SCALER DB NAME,SCALER DESCRIPTION 
                                    #    0                   1              2            
                                    csvslr[lineSplit[0]]['EQ'] = lineSplit[1]
                                    csvslr[lineSplit[0]]['DESC'] = lineSplit[2]
                                    csvslr[lineSplit[0]]['DISABLE'] = lineSplit[3]
                                else:
                                    if (current == 'MBBI'):
                                        csvmbbi[lineSplit[0]]['EQ'] = lineSplit[1]
                                        csvmbbi[lineSplit[0]]['DESC'] = lineSplit[2]
                                        csvmbbi[lineSplit[0]]['ZRST'] = lineSplit[3]
                                        csvmbbi[lineSplit[0]]['ZRVL'] = lineSplit[4]
                                        csvmbbi[lineSplit[0]]['ZRSV'] = lineSplit[5]
                                        csvmbbi[lineSplit[0]]['ONST'] = lineSplit[6]
                                        csvmbbi[lineSplit[0]]['ONVL'] = lineSplit[7]
                                        csvmbbi[lineSplit[0]]['ONSV'] = lineSplit[8]
                                        csvmbbi[lineSplit[0]]['TWST'] = lineSplit[9]
                                        csvmbbi[lineSplit[0]]['TWVL'] = lineSplit[10]
                                        csvmbbi[lineSplit[0]]['TWSV'] = lineSplit[11]
                                        csvmbbi[lineSplit[0]]['THST'] = lineSplit[12]
                                        csvmbbi[lineSplit[0]]['THVL'] = lineSplit[13]
                                        csvmbbi[lineSplit[0]]['THSV'] = lineSplit[14]
                                        csvmbbi[lineSplit[0]]['FRST'] = lineSplit[15]
                                        csvmbbi[lineSplit[0]]['FRVL'] = lineSplit[16]
                                        csvmbbi[lineSplit[0]]['FRSV'] = lineSplit[17]
                                        csvmbbi[lineSplit[0]]['FVST'] = lineSplit[18]
                                        csvmbbi[lineSplit[0]]['FVVL'] = lineSplit[19]
                                        csvmbbi[lineSplit[0]]['FVSV'] = lineSplit[20]
                                        csvmbbi[lineSplit[0]]['SXST'] = lineSplit[21]
                                        csvmbbi[lineSplit[0]]['SXVL'] = lineSplit[22]
                                        csvmbbi[lineSplit[0]]['SXSV'] = lineSplit[23]
                                        csvmbbi[lineSplit[0]]['SVST'] = lineSplit[24]
                                        csvmbbi[lineSplit[0]]['SVVL'] = lineSplit[25]
                                        csvmbbi[lineSplit[0]]['SVSV'] = lineSplit[26]
                                        csvmbbi[lineSplit[0]]['EIST'] = lineSplit[27]
                                        csvmbbi[lineSplit[0]]['EIVL'] = lineSplit[28]
                                        csvmbbi[lineSplit[0]]['EISV'] = lineSplit[29]
                                        csvmbbi[lineSplit[0]]['NIST'] = lineSplit[30]
                                        csvmbbi[lineSplit[0]]['NIVL'] = lineSplit[31]
                                        csvmbbi[lineSplit[0]]['NISV'] = lineSplit[32]
                                        csvmbbi[lineSplit[0]]['TEST'] = lineSplit[33]
                                        csvmbbi[lineSplit[0]]['TEVL'] = lineSplit[34]
                                        csvmbbi[lineSplit[0]]['TESV'] = lineSplit[35]
                                        csvmbbi[lineSplit[0]]['ELST'] = lineSplit[36]
                                        csvmbbi[lineSplit[0]]['ELVL'] = lineSplit[37]
                                        csvmbbi[lineSplit[0]]['ELSV'] = lineSplit[38]
                                        csvmbbi[lineSplit[0]]['TVST'] = lineSplit[39]
                                        csvmbbi[lineSplit[0]]['TVVL'] = lineSplit[40]
                                        csvmbbi[lineSplit[0]]['TVSV'] = lineSplit[41]
                                        csvmbbi[lineSplit[0]]['TTST'] = lineSplit[42]
                                        csvmbbi[lineSplit[0]]['TTVL'] = lineSplit[43]
                                        csvmbbi[lineSplit[0]]['TTSV'] = lineSplit[44]
                                        csvmbbi[lineSplit[0]]['FTST'] = lineSplit[45]
                                        csvmbbi[lineSplit[0]]['FTVL'] = lineSplit[46]
                                        csvmbbi[lineSplit[0]]['FTSV'] = lineSplit[47]
                                        csvmbbi[lineSplit[0]]['FFST'] = lineSplit[48]
                                        csvmbbi[lineSplit[0]]['FFVL'] = lineSplit[49]
                                        csvmbbi[lineSplit[0]]['FFSV'] = lineSplit[50]
                                        csvmbbi[lineSplit[0]]['COSV'] = lineSplit[51]
                                        csvmbbi[lineSplit[0]]['UNSV'] = lineSplit[52]
                                        csvmbbi[lineSplit[0]]['SCAN'] = lineSplit[53]
                                        csvmbbi[lineSplit[0]]['DISABLE'] = lineSplit[54]
                                        
                                    else:
                                        if (current == 'MBBO'):
                                            csvmbbo[lineSplit[0]]['EQ'] = lineSplit[1]
                                            csvmbbo[lineSplit[0]]['DESC'] = lineSplit[2]
                                            csvmbbo[lineSplit[0]]['ZRST'] = lineSplit[3]
                                            csvmbbo[lineSplit[0]]['ZRVL'] = lineSplit[4]
                                            csvmbbo[lineSplit[0]]['ZRSV'] = lineSplit[5]
                                            csvmbbo[lineSplit[0]]['ONST'] = lineSplit[6]
                                            csvmbbo[lineSplit[0]]['ONVL'] = lineSplit[7]
                                            csvmbbo[lineSplit[0]]['ONSV'] = lineSplit[8]
                                            csvmbbo[lineSplit[0]]['TWST'] = lineSplit[9]
                                            csvmbbo[lineSplit[0]]['TWVL'] = lineSplit[10]
                                            csvmbbo[lineSplit[0]]['TWSV'] = lineSplit[11]
                                            csvmbbo[lineSplit[0]]['THST'] = lineSplit[12]
                                            csvmbbo[lineSplit[0]]['THVL'] = lineSplit[13]
                                            csvmbbo[lineSplit[0]]['THSV'] = lineSplit[14]
                                            csvmbbo[lineSplit[0]]['FRST'] = lineSplit[15]
                                            csvmbbo[lineSplit[0]]['FRVL'] = lineSplit[16]
                                            csvmbbo[lineSplit[0]]['FRSV'] = lineSplit[17]
                                            csvmbbo[lineSplit[0]]['FVST'] = lineSplit[18]
                                            csvmbbo[lineSplit[0]]['FVVL'] = lineSplit[19]
                                            csvmbbo[lineSplit[0]]['FVSV'] = lineSplit[20]
                                            csvmbbo[lineSplit[0]]['SXST'] = lineSplit[21]
                                            csvmbbo[lineSplit[0]]['SXVL'] = lineSplit[22]
                                            csvmbbo[lineSplit[0]]['SXSV'] = lineSplit[23]
                                            csvmbbo[lineSplit[0]]['SVST'] = lineSplit[24]
                                            csvmbbo[lineSplit[0]]['SVVL'] = lineSplit[25]
                                            csvmbbo[lineSplit[0]]['SVSV'] = lineSplit[26]
                                            csvmbbo[lineSplit[0]]['EIST'] = lineSplit[27]
                                            csvmbbo[lineSplit[0]]['EIVL'] = lineSplit[28]
                                            csvmbbo[lineSplit[0]]['EISV'] = lineSplit[29]
                                            csvmbbo[lineSplit[0]]['NIST'] = lineSplit[30]
                                            csvmbbo[lineSplit[0]]['NIVL'] = lineSplit[31]
                                            csvmbbo[lineSplit[0]]['NISV'] = lineSplit[32]
                                            csvmbbo[lineSplit[0]]['TEST'] = lineSplit[33]
                                            csvmbbo[lineSplit[0]]['TEVL'] = lineSplit[34]
                                            csvmbbo[lineSplit[0]]['TESV'] = lineSplit[35]
                                            csvmbbo[lineSplit[0]]['ELST'] = lineSplit[36]
                                            csvmbbo[lineSplit[0]]['ELVL'] = lineSplit[37]
                                            csvmbbo[lineSplit[0]]['ELSV'] = lineSplit[38]
                                            csvmbbo[lineSplit[0]]['TVST'] = lineSplit[39]
                                            csvmbbo[lineSplit[0]]['TVVL'] = lineSplit[40]
                                            csvmbbo[lineSplit[0]]['TVSV'] = lineSplit[41]
                                            csvmbbo[lineSplit[0]]['TTST'] = lineSplit[42]
                                            csvmbbo[lineSplit[0]]['TTVL'] = lineSplit[43]
                                            csvmbbo[lineSplit[0]]['TTSV'] = lineSplit[44]
                                            csvmbbo[lineSplit[0]]['FTST'] = lineSplit[45]
                                            csvmbbo[lineSplit[0]]['FTVL'] = lineSplit[46]
                                            csvmbbo[lineSplit[0]]['FTSV'] = lineSplit[47]
                                            csvmbbo[lineSplit[0]]['FFST'] = lineSplit[48]
                                            csvmbbo[lineSplit[0]]['FFVL'] = lineSplit[49]
                                            csvmbbo[lineSplit[0]]['FFSV'] = lineSplit[50]
                                            csvmbbo[lineSplit[0]]['IVOA'] = lineSplit[51]
                                            csvmbbo[lineSplit[0]]['IVOV'] = lineSplit[52]
                                            csvmbbo[lineSplit[0]]['COSV'] = lineSplit[53]
                                            csvmbbo[lineSplit[0]]['UNSV'] = lineSplit[54]
                                            csvmbbo[lineSplit[0]]['INITIALIZE'] = lineSplit[55]
                                            csvmbbo[lineSplit[0]]['INIT VAL'] = lineSplit[56]
                                            csvmbbo[lineSplit[0]]['DISABLE'] = lineSplit[57]
                                            
                                        else:
                                            print("Could not classify data on line {0} in *.csv file".format(index))

    # generate cfg.ini
    with open("{}/cfg.ini".format(args.dst) , "w") as f:
        print("Generating {}/cfg.ini".format(args.dst))
        f.write(header.format(datetime.datetime.now()))
        printToCFGFile(f, 'Settings', settings, dict(), 0)
        printToCFGFile(f, 'BIAddresses', biaddr, dict(), 0)
        printToCFGFile(f, 'BI_VECTOR', bidict, csvbi, 1)
        printToCFGFile(f, 'AO', aoaddr, csvao, 1)
        printToCFGFile(f, 'AI', aiaddr, csvai, 1)
        printToCFGFile(f, 'BO', boaddr, csvbo, 1)
        printToCFGFile(f, 'MBBI', mbbiaddr, csvmbbi, 1)
        printToCFGFile(f, 'MBBO', mbboaddr, csvmbbo, 1)
        
        # Convert scaler names to list then to dictionary for printing
        scalerNameList = list(scalers.keys())
        scalerNamesDict = { scalerNameList[i] : '' for i in range(0, len(scalerNameList) ) }
        printToCFGFile(f, 'SCALERS', scalerNamesDict, csvslr, 1)
        for scaler in scalers:
            printToCFGFile(f, scaler, scalers[scaler], dict(), 0)
        for fxp in fxps:
            printToCFGFile(f, fxp, fxps[fxp], dict(), 0)            
        waveformNameList = list(waveforms.keys())
        waveformNamesDict = { waveformNameList[i] : '' for i in range(0, len(waveformNameList) ) }
        printToCFGFile(f, 'WAVEFORMS', waveformNamesDict, csvwf, 1)        
        for waveform in waveforms:
            printToCFGFile(f, waveform, waveforms[waveform], dict(), 0)                                                             

    # generate req file
    with open("{}/crioioc.req".format(args.dst) , "w") as f:
        print("Generating {}/crioioc.req".format(args.dst))
        printToReqFile(f, boaddr, csvbo, args.beamline, args.crio)
        printToReqFile(f, aoaddr, csvao, args.beamline, args.crio)


    # generate init-pv.cmd file
    with open("{}/init-pv.cmd".format(args.dst) , "w") as f:
        print("Generating {}/init-pv.cmd".format(args.dst))
        printToInitFile(f, boaddr, csvbo, args.beamline, args.crio)
        printToInitFile(f, aoaddr, csvao, args.beamline, args.crio)
        printToInitFile(f, mbboaddr, csvmbbo, args.beamline, args.crio)

    # generate init-recsync.cmd file
    with open("{}/init-recsync.cmd".format(args.dst) , "w") as f:
        print("Generating {}/recsync-pv.cmd".format(args.dst))
        f.write("epicsEnvSet(\"IOCNAME\", \""+args.beamline+"-"+args.loc+"-"+args.crio+"\")\n")           
        f.write('dbLoadRecords \"${RECCASTER}/db/reccaster.db", "P='+args.beamline+":"+args.loc+":"+args.crio+":REC:\"\n")  

    #template definitions
    tplhdr = 'file \"$(TOP)/db/{0}\"\n{{\npattern\n{{BL, LOC, EQ, DTYP, PIN, DESC}}\n'
    tplbdy = '{{\"{0}", \"'+args.loc+'", "'+args.crio+':{1}\", \"{2}\", \"{3}\", \"{4}\"}}\n'
    tplsclrhdr = 'file \"$(TOP)/db/{0}\"\n{{\npattern\n{{BL, LOC, EQ, DTYP, FREQ, PIN, DESC}}\n'
    tplsclrbdy = '{{\"{0}", \"'+args.loc+'", "'+args.crio+':{1}\", \"{2}\", \"10000000\", \"{3}\", \"{4}\"}}\n'
    tplwfhdr = 'file \"$(TOP)/db/{0}\"\n{{\npattern\n{{BL, LOC, EQ, DTYP, PIN, FTVL, NELM, DESC}}\n'
    tplwfbdy = '{{\"{0}", \"'+args.loc+'","'+args.crio+':{1}\", \"{2}\", \"{3}\", \"{4}\", \"{5}\", \"{6}\"}}\n'
    
    tplmbbohdr = 'file \"$(TOP)/db/{0}\"\n{{\npattern\n{{BL, LOC, EQ, DESC, PIN, DTYP, ZRST, ZRVL, ZRSV, ONST, ONVL, ONSV, TWST, TWVL, TWSV, THST, THVL,\
THSV, FRST, FRVL, FRSV, FVST, FVVL, FVSV, SXST, SXVL, SXSV, SVST, SVVL, SVSV, EIST, EIVL,\
EISV, NIST, NIVL, NISV, TEST, TEVL, TESV, ELST, ELVL, ELSV, TVST, TVVL, TVSV, TTST, TTVL,\
TTSV, FTST, FTVL, FTSV, FFST, FFVL, FFSV, IVOA, IVOV, COSV, UNSV }}\n'
    tplmbbobdy = '{{\"{0}", \"'+args.loc+'", "'+args.crio+':{1}\" \"{2}\", \"{3}\", \"{4}\", \"{5}\", \"{6}\", \"{7}\", \"{8}\", \"{9}\", \"{10}\", \"{11}\",\
\"{12}\", \"{13}\", \"{14}\", \"{15}\", \"{16}\", \"{17}\", \"{18}\", \"{19}\", \"{20}\", \"{21}\", \"{22}\", \"{23}\",\
\"{24}\", \"{25}\", \"{26}\", \"{27}\", \"{28}\", \"{29}\", \"{30}\", \"{31}\", \"{32}\", \"{33}\", \"{34}\", \"{35}\",\
\"{36}\", \"{37}\", \"{38}\", \"{39}\", \"{40}\", \"{41}\", \"{42}\", \"{43}\", \"{44}\", \"{45}\", \"{46}\", \"{47}\",\
\"{48}\", \"{49}\", \"{50}\", \"{51}\", \"{52}\", \"{53}\", \"{54}\", \"{55}\", \"{56}\"}}'
    
    tplmbbihdr = 'file \"$(TOP)/db/{0}\"\n{{\npattern\n{{BL, LOC, EQ, DESC, PIN, DTYP, SCAN, ZRST, ZRVL, ZRSV, ONST, ONVL, ONSV, TWST, TWVL, TWSV,\
THST, THVL, THSV, FRST, FRVL, FRSV, FVST, FVVL, FVSV, SXST, SXVL, SXSV, SVST, SVVL,\
SVSV, EIST, EIVL, EISV, NIST, NIVL, NISV, TEST, TEVL, TESV, ELST, ELVL, ELSV, TVST,\
TVVL, TVSV, TTST, TTVL, TTSV, FTST, FTVL, FTSV, FFST, FFVL, FFSV, COSV, UNSV}}\n'
                                                         
    tplmbbibdy = '{{\"{0}", \"'+args.loc+'","'+args.crio+':{1}\", \"{2}\", \"{3}\", \"{4}\", \"{5}\", \"{6}\", \"{7}\", \"{8}\", \"{9}\", \"{10}\", \"{11}\",\
\"{12}\", \"{13}\", \"{14}\", \"{15}\", \"{16}\", \"{17}\", \"{18}\", \"{19}\", \"{20}\", \"{21}\", \"{22}\", \"{23}\",\
\"{24}\", \"{25}\", \"{26}\", \"{27}\", \"{28}\", \"{29}\", \"{30}\", \"{31}\", \"{32}\", \"{33}\", \"{34}\", \"{35}\",\
\"{36}\", \"{37}\", \"{38}\", \"{39}\", \"{40}\", \"{41}\", \"{42}\", \"{43}\", \"{44}\", \"{45}\", \"{46}\", \"{47}\",\
\"{48}\", \"{49}\", \"{50}\", \"{51}\", \"{52}\", \"{53}\", \"{54}\", \"{55}\"}}\n'
        
    #Generate substitutions  
    bidict_inverted = {v: k for k, v in bidict.items()} 
    bidict_inverted = {**biaddr, **bidict_inverted}
    buildSub(tplhdr, tplbdy, args.beamline, args.aodtyp, aoaddr, "devAOCRIO.db.template", 'ao',  csvao)
    buildSub(tplhdr, tplbdy, args.beamline, args.aidtyp, aiaddr, "devAICRIO.db.template", 'ai', csvai)
    buildSub(tplhdr, tplbdy, args.beamline, args.bidtyp, bidict_inverted, "devBICRIO.db.template", 'bi', csvbi)
    buildSub(tplhdr, tplbdy, args.beamline, args.bodtyp, boaddr, "devBOCRIO.db.template", 'bo', csvbo)
    buildSub(tplmbbihdr, tplmbbibdy, args.beamline, args.mbbidtyp, mbbiaddr, "devMBBICRIO.db.template", 'mbbi', csvmbbi)
    buildSub(tplmbbohdr, tplmbbobdy, args.beamline, args.mbbodtyp, mbboaddr, "devMBBOCRIO.db.template", 'mbbo', csvmbbo)
    buildSub(tplsclrhdr, tplsclrbdy, args.beamline, args.scalerdtyp, scalerNamesDict, "devSCALERCRIO.db.template", 'scaler', csvslr)
    buildSub(tplwfhdr, tplwfbdy, args.beamline, args.wfdtyp, waveformNamesDict, "devWAVEFORMCRIO.db.template", 'waveform', csvwf)

    print("Check {0} folder, and modify the substitution files.".format(args.dst))

else:

    #Check if there is need to use reference cfg file
    if (args.refcsv):
        with open("{0}/{1}".format(args.src, "cfg_old.csv") , "r") as f:
            lines = f.readlines()
        current = "None"
        for index, val in enumerate(lines):
            #val = val.strip()
            removedDelimiter = val.replace(dlm, "")
            removedDelimiter = removedDelimiter.replace(" ", "")
            if (not removedDelimiter):
                continue
            lineSplit = val.split(dlm)
            result = re.search('^AI INI NAME', lineSplit[0])
            if (result is not None):
                current = "AI"
                continue
            else :
                result = re.search('^BI INI NAME', lineSplit[0])
                if (result is not None):
                    current = "BI"
                    continue
                else :
                    result = re.search('^BO INI NAME', lineSplit[0])
                    if (result is not None):
                        current = "BO"
                        continue
                    else :    
                        result = re.search('^AO INI NAME', lineSplit[0])
                        if (result is not None):
                            current = "AO"
                            continue
                        else :
                            result = re.search('^SCALER INI NAME', lineSplit[0])
                            if (result is not None):
                                current = "SCALER"
                                continue
                            else :               
                                result = re.search('^WAVEFORM INI NAME', lineSplit[0])
                                if (result is not None):
                                    current = "WAVEFORM"
                                    continue
                                else :               
                                    result = re.search('^MBBI INI NAME', lineSplit[0])
                                    if (result is not None):
                                        current = "MBBI"
                                        continue 
                                    else :               
                                        result = re.search('^MBBO INI NAME', lineSplit[0])
                                        if (result is not None):
                                            current = "MBBO"
                                            continue                                                                           
            if (current == 'AI'):
                csvairef[lineSplit[0]] = val
                        
            else: 
                if (current == 'AO'):
                    csvaoref[lineSplit[0]] = val
                         
                else: 
                    if (current == 'BI'):
                        csvbiref[lineSplit[0]] = val

                    else: 
                        if (current == 'BO'):
                            csvboref[lineSplit[0]] = val
                          
                        else: 
                            if (current == 'WAVEFORM'):
                                csvwfref[lineSplit[0]] = val
                            else: 
                                if (current == 'SCALER'):
                                    csvslrref[lineSplit[0]] = val
                                else:
                                    if (current == 'MBBI'):
                                        csvmbbiref[lineSplit[0]] = val
                                        
                                    else:
                                        if (current == 'MBBO'):
                                            csvmbboref[lineSplit[0]] = val 
    
    # generate *.csv file here using the data extracted
    with open("{0}/{1}".format(args.src, args.cfgcsv) , "w") as f:
        f.write("AI INI NAME"+dlm+"AI SUB-EQUIPMENT NAME"+dlm+"AI DESCRIPTION"+dlm+"AI Sign(FXP)"+dlm+"AI Word Length(FXP)"+dlm+"AI INTEGER LENGTH(FXP)"+dlm+"Disable\n") 
        result = None
        
              
        for i in list(aiaddr.keys()):
            #print(i)
            for j in list(scalers.keys()):
                result = re.search(j, i)
                if (result is not None):
                    break
            if (result is not None):
                #print(result)
                if i in csvairef:
                    f.write(csvairef[i])
                else:
                    f.write("{}".format(i)+dlm*3+"1"+dlm+"64"+dlm+"32"+dlm+"0\n")   
            else:
                if i in csvairef:
                    f.write(csvairef[i])
                else:            
                    f.write("{}".format(i)+dlm*6+"0\n")   
        f.write(""+dlm*8+"\n"+dlm*8+"\n")  
        
        
        f.write("BI INI NAME"+dlm+"BI SUB-EQUIPMENT NAME"+dlm+"BI DESCRIPTION"+dlm+"Disable\n") 
        for i in list(biaddr.keys()):
            if (i != "BI_VECTOR"):
                if i in csvbiref:
                    f.write(csvbiref[i])
                else: 
                    f.write("{}".format(i)+dlm*3+"0\n") 
                    
        for i in bidict.values():
            if i in csvbiref:
                f.write(csvbiref[i])
            else:
                f.write("{}".format(i)+dlm*3+"0\n")  
                           
        f.write(dlm*8+"\n"+dlm*8+"\n")       
                 
        f.write("BO INI NAME"+dlm+"BO SUB-EQUIPMENT NAME"+dlm+"BO DESCRIPTION"+dlm+" AUTOSAVE"+dlm+"INITIALIZE"+dlm+"INIT VAL"+dlm+"Disable\n") 
        for i in list(boaddr.keys()):
            if i in csvboref:
                f.write(csvboref[i])
            else:        
                f.write("{}".format(i)+dlm*3+"0"+dlm+"0"+dlm+"0"+dlm+"0\n") 
        f.write(dlm*8+"\n"+dlm*8+"\n")   

        f.write("AO INI NAME"+dlm+"AO SUB-EQUIPMENT NAME"+dlm+"AO DESCRIPTION"+dlm+"AO Sign(FXP)"+dlm+"AO Word Length(FXP)"+dlm+"AO INTEGER LENGTH(FXP)"+dlm+"AUTOSAVE"+dlm+"INITIALIZE"+dlm+"INIT VAL"+dlm+"Disable\n") 
        for i in list(aoaddr.keys()):
            for j in list(scalers.keys()):
                result = None
                result = re.search(j, i)
                if (result is not None):
                    break                
            if (result is not None):
                if i in csvaoref:
                    f.write(csvaoref[i])
                else:              
                    f.write("{}".format(i)+dlm*3+"1"+dlm+"64"+dlm+"64"+dlm+"0"+dlm+"0"+dlm+"0"+dlm+"0\n")   
            else:
                if i in csvaoref:
                    f.write(csvaoref[i])
                else:             
                    f.write("{}".format(i)+dlm*6+"0"+dlm+"0"+dlm+"0"+dlm+"0\n") 
        f.write(dlm+"\n"+dlm*8+"\n")     

        f.write("SCALER INI NAME"+dlm+"SCALER EQUIPMENT NAME"+dlm+"SCALER DESCRIPTION"+dlm+"Disable\n") 
        for i in list(scalers.keys()):
            if i in csvslrref:
                f.write(csvslrref[i])
            else:        
                f.write("{}".format(i)+dlm*3+"0\n") 
        f.write(dlm*8+"\n"+dlm*8+"\n")   

        f.write("WAVEFORM INI NAME"+dlm+"WAVEFORM SUB-EQUIPMENT NAME"+dlm+" DESCRIPTION"+dlm+" SIZE"+dlm+"Disable\n") 
        for i in list(waveforms.keys()):
            if i in csvwfref:
                f.write(csvwfref[i])
            else:         
                f.write(("{0}"+dlm*3+"{1}"+dlm+"0\n").format(i, waveforms[i]['Size']))  
        f.write(dlm*8+"\n"+dlm*8+"\n")     
        
        f.write("MBBI INI NAME"+dlm+"MBBI SUB-EQUIPMENT NAME"+dlm+" DESCRIPTION"+dlm+" ZRST"+dlm+" ZRVL"+dlm+" ZRSV"+dlm+" ONST"+dlm+" ONVL"+dlm+" ONSV"+dlm+" TWST"+dlm+" TWVL"+dlm+" TWSV"+dlm+" THST"+dlm+" THVL"+dlm+" THSV"+dlm+" FRST"+dlm+" FRVL"+dlm+" FRSV"+dlm+" FVST"+dlm+" FVVL"+dlm+" FVSV"+dlm+" SXST"+dlm+" SXVL"+dlm+" SXSV"+dlm+" SVST"+dlm+" SVVL"+dlm+" SVSV"+dlm+" EIST"+dlm+" EIVL"+dlm+" EISV"+dlm+" NIST"+dlm+" NIVL"+dlm+" NISV"+dlm+" TEST"+dlm+" TEVL"+dlm+" TESV"+dlm+" ELST"+dlm+" ELVL"+dlm+" ELSV"+dlm+" TVST"+dlm+" TVVL"+dlm+" TVSV"+dlm+" TTST"+dlm+" TTVL"+dlm+" TTSV"+dlm+" FTST"+dlm+" FTVL"+dlm+" FTSV"+dlm+" FFST"+dlm+" FFVL"+dlm+" FFSV"+dlm+" COSV"+dlm+" UNSV"+dlm+" SCAN"+dlm+"Disable\n") 
        for i in list(mbbiaddr.keys()):
            if i in csvmbbiref:
                f.write(csvmbbiref[i])
            else:         
                f.write("{}".format(i)+dlm*4+"0"+dlm+"INVALID"+dlm*2
+"1"+dlm+"INVALID"+dlm*2+"2"+dlm+"INVALID"+dlm*2+"3"+dlm+"INVALID"+dlm*2+"4"+dlm+"INVALID"+dlm*2+"5"+dlm+"INVALID"+dlm*2+"6"+dlm+"INVALID"+dlm*2+"7"+dlm+"INVALID"+dlm*2+"8"+dlm+"INVALID"+dlm*2+"9"+dlm+"INVALID"+dlm*2+"10"+dlm+"INVALID"+dlm*2+"11"+dlm+"INVALID"+dlm*2+"12"+dlm+"INVALID"+dlm*2+"13"+dlm+"INVALID"+dlm*2+"14"+dlm+"INVALID"+dlm*2+"15"+dlm+"INVALID"+dlm+"0"+dlm+"0"+dlm+".1 second"+dlm+"0\n") 
        f.write(dlm*8+"\n"+dlm*8+"\n")      
        
        f.write("MBBO INI NAME"+dlm+"MBBO SUB-EQUIPMENT NAME"+dlm+" DESCRIPTION"+dlm+" ZRST"+dlm+" ZRVL"+dlm+" ZRSV"+dlm+" ONST"+dlm+" ONVL"+dlm+" ONSV"+dlm+" TWST"+dlm+" TWVL"+dlm+" TWSV"+dlm+" THST"+dlm+" THVL"+dlm+" THSV"+dlm+" FRST"+dlm+" FRVL"+dlm+" FRSV"+dlm+" FVST"+dlm+" FVVL"+dlm+" FVSV"+dlm+" SXST"+dlm+" SXVL"+dlm+" SXSV"+dlm+" SVST"+dlm+" SVVL"+dlm+" SVSV"+dlm+" EIST"+dlm+" EIVL"+dlm+" EISV"+dlm+" NIST"+dlm+" NIVL"+dlm+" NISV"+dlm+" TEST"+dlm+" TEVL"+dlm+" TESV"+dlm+" ELST"+dlm+" ELVL"+dlm+" ELSV"+dlm+" TVST"+dlm+" TVVL"+dlm+" TVSV"+dlm+" TTST"+dlm+" TTVL"+dlm+" TTSV"+dlm+" FTST"+dlm+" FTVL"+dlm+" FTSV"+dlm+" FFST"+dlm+" FFVL"+dlm+" FFSV"+dlm+" IVOA"+dlm+" IVOV"+dlm+" COSV"+dlm+" UNSV"+dlm+" INITIALIZE"+dlm+" INIT VAL"+dlm+"Disable\n") 
        for i in list(mbboaddr.keys()):
            if i in csvmbboref:
                f.write(csvmbboref[i])
            else:         
                f.write("{}".format(i)+dlm*4+"0"+dlm+"INVALID"+dlm*2+"1"+dlm+"INVALID"+dlm*2+"2"+dlm+"INVALID"+dlm*2+"3"+dlm+"INVALID"+dlm*2+"4"+dlm+"INVALID"+dlm*2+"5"+dlm+"INVALID"+dlm*2+"6"+dlm+"INVALID"+dlm*2+"7"+dlm+"INVALID"+dlm*2+"8"+dlm+"INVALID"+dlm*2+"9"+dlm+"INVALID"+dlm*2+"10"+dlm+"INVALID"+dlm*2+"11"+dlm+"INVALID"+dlm*2+"12"+dlm+"INVALID"+dlm*2+"13"+dlm+"INVALID"+dlm*2+"14"+dlm+"INVALID"+dlm*2+"15"+dlm+"INVALID"+dlm+"1"+dlm+"0"+dlm+"0"+dlm+"0"+dlm+"0"+dlm+"0"+dlm+"0\n") 
        f.write(dlm*8+"\n"+dlm*8+"\n")                                      
        
