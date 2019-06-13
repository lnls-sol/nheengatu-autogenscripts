#!/usr/bin/python3

##############################################################
#   CRIO address and template extraction/generation script
#   Author : Dawood Alnajjar
#   CNPEM - LNLS - BEAMLINE Software Group
#   March 23, 2019
##############################################################

import re
import sys
import argparse
import collections
import os 
from string import Template
from shutil import copyfile
import glob
import datetime

### HELPER FUNCTIONS
def printToFile(file, key, items):
    f.write("[{}]\n".format(key))
    for key,value in items.items():
        if (key != 'TypeEPICS'):
            f.write("{}={}\n".format(key,value))   
    f.write("\n\n")     


def buildSub(tplhdr, tplbdy, beamline, dtype, pins, dbtemplate, fname, record, csv):
    tpls = tplhdr.format(dbtemplate)
    if(record == 0): #SCALER
        for key in pins.keys():
            tpls = tpls + tplbdy.format(beamline, csv[key]['DB NAME'], dtype, key, csv[key]['DESCRIPTION'])
    else: # Waveform
        if (record == 1):
            for indx, key in enumerate(pins.keys()):
                tpls = tpls + tplbdy.format(beamline, csv[key]['DB NAME'], dtype, key, csv[key]['TypeEPICS'], csv[key]['SIZE'],csv[key]['DESCRIPTION'])
        else:
            for indx, key in enumerate(pins.keys()):
                if (key == 'BI0'):
                    continue
                tpls = tpls + tplbdy.format(beamline, csv[key]['DB NAME'], dtype, key, csv[key]['DESCRIPTION'])

    tpls = tpls + "\n}"
    with open("{}/{}.db.sub".format(args.dst, fname) , "w") as f:
        print("Generating {}/{}.db.sub file".format(args.dst, fname))
        f.write(tpls)     


description = 'This programs extracts the address in the header file generated by the FPGA C API, and generates ini and template files for EPICS.'

header = ';-----------------------------------------------------------------\n\
; Automatically generated ini file for CRIO Nheengatu library\n\
; Generate on {0}\n\
;\n\
;INI records:\n\
;  - [Settings]\n\
;  - [BIAddresses]\n\
;  - [BI0]\n\
;  - [AO]\n\
;  - [AI]\n\
;  - [FXP_XX]\n\
;  - [BO]\n\
;  - [SCALERS]\n\
;  - [SCALERXX]\n\
;  - [WAVEFORMS]\n\
;  - [WAVEFORMXX]\n\
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
;        Single address of BI vector (upto 64-bits). Must have BI0 as the single item.\n\
;      - BI0:\n\
;        A list with all the BIs that will be read by Nheengatu and their respective index\n\
;      - AO:\n\
;        A list with all the AOs that will be read by Nheengatu and their respective addresses\n\
;      - AI:\n\
;        A list with all the AIs that will be read by Nheengatu and their respective addresses\n\
;      - BO:\n\
;        A list with all the BOs that will be read by Nheengatu and their respective addresses\n\
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
;BI0. The library looks for this specific string, so it must be BI0 although \n\
;you may have named it differently in the FPGA VI.\n\
;-----------------------------------------------------------------\n\
\n\n\n\n'


# initiate the parser
parser = argparse.ArgumentParser(description=description)

# Input parameters
parser.add_argument("-u", "--useSM", help="Use shared memory", action='store_true')
parser.add_argument("-d", "--dst", default="crio-ioc", help="Name of the output folder. Default is <crio-ioc>")
parser.add_argument( "-p", "--path", help="Bitfile path. Default is </usr/local/epics/apps/config/crio-ioc/>", default = '/usr/local/epics/apps/config/crio-ioc/')
parser.add_argument("-s", "--src", help="Folder containing all files necessary for ini/template generation", default = '.')
parser.add_argument("--binum", help="The total number of BI variables. Default is <0>", default = '0')
parser.add_argument("--extract", help="Extract data from headerfile", action='store_true')
parser.add_argument("--ip", help="Destination IP of the CRIO. Default is <127.0.0.1>", default = '127.0.0.1')
parser.add_argument("--smfname", help="Shared memory file path and name", default = '/labview_linux_sm')
parser.add_argument("--smsize", help="Shared memory size. Default is <4096>", default = '4096')
parser.add_argument("--aikey", help="AI keyword that any AI variable will start with in the headerfile. Default is <ai>", default = 'ai')
parser.add_argument("--aokey", help="AO keyword that any AO variable will start with in the headerfile Default is <ao>", default = 'ao')
parser.add_argument("--bokey", help="BO keyword that any BO variable will start with in the headerfile. Default is <bo>", default = 'bo')
parser.add_argument("--bikey", help="BI keyword that any BI variable will start with in the headerfile. Default is <BI>", default = 'BI')
parser.add_argument("--fxpkey", help="Fixedpoint keyword that any AI/AO variable will have after that AI/AO keyword in the headerfile. Default is <fxp>", default = 'fxp')
parser.add_argument("--scalerkey", help="Scaler keyword that any Scaler variable will be followed with in the headerfile. Default is <SCALER>", default = 'SCALER')
parser.add_argument("--waveformkey",help="Waveform keyword that any Waveform variable will be followed with in the headerfile. Default is <WF>", default = 'WF')
parser.add_argument("--beamline", help="Name of the beamline (for template file generation). Default is <SOL>", default = 'SOL')
parser.add_argument("--bidtyp", help="DTYPE of BI record", default = 'CrioBI')
parser.add_argument("--aidtyp", help="DTYPE of AI record", default = 'CrioAI')
parser.add_argument("--bodtyp", help="DTYPE of BO record", default = 'CrioBO')
parser.add_argument("--aodtyp", help="DTYPE of AO record", default = 'CrioAO')
parser.add_argument("--wfdtyp", help="DTYPE of WF record", default = 'CrioWAVEFORM')
parser.add_argument("--crio", help="Name of the CRIO. Default is <CRIO1>", default = 'CRIO1')
parser.add_argument("--scalerdtyp", help="DTYPE of Scaler record", default = 'CRIO Scaler')
parser.add_argument("--cfgcsv", help="csv file name. Default=cfg.csv", default = 'cfg.csv')


# read arguments from the command line
args = parser.parse_args()

biaddr = {}
boaddr = {}
aoaddr = {}
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
csvwf = collections.defaultdict(dict)
csvslr = collections.defaultdict(dict)
settings = {'Destination Crio IP' : args.ip,
            'Path':args.path,
            'Use Shared Memory': 1 if(args.useSM) else 0,
            'Shared Memory Path': args.smfname,
            'Shared Memory Size': args.smsize}
rtvarCount = 0;
fpgavarCount = 0;


              

        
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
    copyfile(headerFilesFound[0], args.dst+"/reference/reference.h")
    if (args.useSM):
        copyfile(args.src+"/RT.list", args.dst+"/reference/RT.list")
 
 
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
        else:
            # Extracting BI, BO, AI, AO, AI FXP and AO FXP
            result = re.search('IndicatorU64_('+args.bikey+'[a-zA-Z0-9_]*) = 0x([A-F0-9]{5})', line)
            if (result is not None):
                biaddr["BI0"]=(result.group(2))
                fpgavarCount += 1
                if (args.binum != 0):
                    bidict = { i : "DI{0}".format(i) for i in range(int(args.binum)) }
                else:
                    print("Found BI0 in header file, and yet binum input parameter was set to 0\n")
                    sys.exit
            else:
                result = re.search('IndicatorSgl_('+args.aikey+'[a-zA-Z0-9_]*) = 0x([A-F0-9]{5})', line)
                if (result is not None):
                    aiaddr[result.group(1)]=(result.group(2))
                    fpgavarCount += 1                
                else:
                    result = re.search('ControlSgl_('+args.aokey+'[a-zA-Z0-9_]*) = 0x([A-F0-9]{5})', line)
                    if (result is not None):
                        aoaddr[result.group(1)]=(result.group(2))         
                        fpgavarCount += 1
                    else:
                        result = re.search('ControlBool_('+args.bokey+'[a-zA-Z0-9_]*) = 0x([A-F0-9]{5})', line)
                        if (result is not None):
                            boaddr[result.group(1)]=(result.group(2))                              
                            fpgavarCount += 1
                        else:
                            result = re.search('IndicatorU64_('+args.aikey+args.fxpkey+'([a-zA-Z0-9_])*) = 0x([A-F0-9]{5})', line)
                            if (result is not None):
                                aiaddr["FXP_"+result.group(1)]=(result.group(3))
                                fpgavarCount += 1   
                            else:
                                result = re.search('ControlU64_('+args.aokey+args.fxpkey+'([a-zA-Z0-9_])*) = 0x([A-F0-9]{5})', line)
                                if (result is not None):
                                    aoaddr["FXP_"+result.group(1)]=(result.group(3))
                                    fpgavarCount += 1                                                              


#process RT variables if enabled

if (args.useSM):
    rtlist = [rt.rstrip() for rt in open('{}/RT.list'.format(args.src))]
    for i, val in enumerate(rtlist):
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
            if (val == ",,,,,"):
                print('Found empty line {0} in csv file. Ignoring'.format(index+1))
                continue
            lineSplit = val.split(',')
            result = re.search('AI INI NAME', lineSplit[0])
            if (result is not None):
                current = "AI"
                continue
            else :
                result = re.search('BI INI NAME', lineSplit[0])
                if (result is not None):
                    current = "BI"
                    continue
                else :
                    result = re.search('BO INI NAME', lineSplit[0])
                    if (result is not None):
                        current = "BO"
                        continue
                    else :    
                        result = re.search('AO INI NAME', lineSplit[0])
                        if (result is not None):
                            current = "AO"
                            continue
                        else :
                            result = re.search('SCALER INI NAME', lineSplit[0])
                            if (result is not None):
                                current = "SCALER"
                                continue
                            else :               
                                result = re.search('WAVEFORM INI NAME', lineSplit[0])
                                if (result is not None):
                                    current = "WAVEFORM"
                                    continue
            if (current == 'AI'):
                #AI INI NAME,AI DB NAME,AI DESCRIPTION,AI Sign(FXP),AI Word Length(FXP),AI INTEGER LENGTH(FXP)
                #    0            1          2              3               4                   5
                csvai[lineSplit[0]]['DB NAME'] = lineSplit[1]
                csvai[lineSplit[0]]['DESCRIPTION'] = lineSplit[2]
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
                    #AO INI NAME,AO DB NAME,AO DESCRIPTION,AO Sign(FXP),AO Word Length(FXP),AO INTEGER LENGTH(FXP)
                    #    0            1          2              3               4                   5
                    csvao[lineSplit[0]]['DB NAME'] = lineSplit[1]
                    csvao[lineSplit[0]]['DESCRIPTION'] = lineSplit[2]
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
                        csvbi[lineSplit[0]]['DB NAME'] = lineSplit[1]
                        csvbi[lineSplit[0]]['DESCRIPTION'] = lineSplit[2]
                    else: 
                        if (current == 'BO'):
                            #BO INI NAME,BO DB NAME,BO DESCRIPTION
                            #    0            1          2             
                            csvbo[lineSplit[0]]['DB NAME'] = lineSplit[1]
                            csvbo[lineSplit[0]]['DESCRIPTION']    = lineSplit[2]        
                        else: 
                            if (current == 'WAVEFORM'):
                                #WAVEFORM INI NAME, DB NAME, DESCRIPTION, SIZE
                                #    0            1          2              3
                                csvwf[lineSplit[0]]['DB NAME'] = lineSplit[1]
                                csvwf[lineSplit[0]]['DESCRIPTION'] = lineSplit[2]
                                csvwf[lineSplit[0]]['SIZE'] = int(lineSplit[3])
                            else: 
                                if (current == 'SCALER'):
                                    #SCALER INI NAME,SCALER DB NAME,SCALER DESCRIPTION 
                                    #    0                   1              2            
                                    csvslr[lineSplit[0]]['DB NAME'] = lineSplit[1]
                                    csvslr[lineSplit[0]]['DESCRIPTION'] = lineSplit[2]
                                else:
                                    print("Could not classify data on line {0} in *.csv file".format(index))

    # generate cfg.ini
    with open("{}/cfg.ini".format(args.dst) , "w") as f:
        print("Generating {}/cfg.ini".format(args.dst))
        f.write(header.format(datetime.datetime.now()))
        printToFile(f, 'Settings', settings)
        printToFile(f, 'BIAddresses', biaddr)
        printToFile(f, 'BI0', bidict)
        printToFile(f, 'AO', aoaddr)
        printToFile(f, 'AI', aiaddr)
        printToFile(f, 'BO', boaddr)
        # Convert scaler names to list then to dictionary for printing
        scalerNameList = list(scalers.keys())
        scalerNamesDict = { scalerNameList[i] : '' for i in range(0, len(scalerNameList) ) }
        printToFile(f, 'SCALERS', scalerNamesDict)
        for scaler in scalers:
            printToFile(f, scaler, scalers[scaler])
        for fxp in fxps:
            printToFile(f, fxp, fxps[fxp])            
        waveformNameList = list(waveforms.keys())
        waveformNamesDict = { waveformNameList[i] : '' for i in range(0, len(waveformNameList) ) }
        printToFile(f, 'WAVEFORMS', waveformNamesDict)        
        for waveform in waveforms:
            printToFile(f, waveform, waveforms[waveform])                                                             



             

    #template definitions
    tplhdr = 'file \"$(TOP)/db/{0}\"\n{{\npattern\n{{BL, EQ, DTYP, PIN, DESC}}\n'
    tplbdy = '{{\"{0}", \"'+args.crio+':{1}\", \"{2}\", \"{3}\", \"{4}\"}}\n'
    tplsclrhdr = 'file \"$(TOP)/db/{0}\"\n{{\npattern\n{{BL, EQ, DTYP, FREQ, PIN, DESC}}\n'
    tplsclrbdy = '{{\"{0}", \"'+args.crio+':{1}\", \"{2}\", \"10000000\", \"{3}\", \"{4}\"}}\n'
    tplwfhdr = 'file \"$(TOP)/db/{0}\"\n{{\npattern\n{{BL, EQ, DTYP, PIN, FTVL, NELM, DESC}}\n'
    tplwfbdy = '{{\"{0}", \"'+args.crio+':{1}\", \"{2}\", \"{3}\", \"{4}\", \"{5}\", \"{6}\"}}\n'

    #Generate substitutions  
    bidict_inverted = {v: k for k, v in bidict.items()} 
    bidict_inverted = {**biaddr, **bidict_inverted}
    buildSub(tplhdr, tplbdy, args.beamline, args.aodtyp, aoaddr, "devAOCRIO.db.template", 'ao', 2, csvao)
    buildSub(tplhdr, tplbdy, args.beamline, args.aidtyp, aiaddr, "devAICRIO.db.template", 'ai', 2, csvai)
    buildSub(tplhdr, tplbdy, args.beamline, args.bidtyp, bidict_inverted, "devBICRIO.db.template", 'bi', 2, csvbi)
    buildSub(tplhdr, tplbdy, args.beamline, args.bodtyp, boaddr, "devBOCRIO.db.template", 'bo', 2, csvbo)
    buildSub(tplsclrhdr, tplsclrbdy, args.beamline, args.scalerdtyp, scalerNamesDict, "devSCALERCRIO.db.template", 'scaler', 0, csvslr)
    buildSub(tplwfhdr, tplwfbdy, args.beamline, args.wfdtyp, waveformNamesDict, "devWAVEFORMCRIO.db.template", 'waveform', 1, csvwf)

    print("Check {0} folder, and modify the substitution files.".format(args.dst))

else:
    # generate *.csv file here using the data extracted
    with open("{0}/{1}".format(args.src, args.cfgcsv) , "w") as f:
        f.write("AI INI NAME,AI DB NAME,AI DESCRIPTION,AI Sign(FXP),AI Word Length(FXP),AI INTEGER LENGTH(FXP)\n") 
        for i in list(aiaddr.keys()):
            f.write("{},,,,,\n".format(i))   
        f.write(",,,,,\n,,,,,\n")  
        
        
        f.write("BI INI NAME,BI DB NAME,BI DESCRIPTION\n") 
        for i in list(biaddr.keys()):
            if (i != "BI0"):
                f.write("{},,\n".format(i)) 
        for i in bidict.values():
            f.write("{},,\n".format(i))             
        f.write(",,,,,\n,,,,,\n")       
                 
        f.write("BO INI NAME,BO DB NAME,BO DESCRIPTION\n") 
        for i in list(boaddr.keys()):
            f.write("{},,\n".format(i)) 
        f.write(",,,,,\n,,,,,\n")   

        f.write("AO INI NAME,AO DB NAME,AO DESCRIPTION,AO Sign(FXP),AO Word Length(FXP),AO INTEGER LENGTH(FXP)\n") 
        for i in list(aoaddr.keys()):
            f.write("{},,,,,\n".format(i)) 
        f.write(",,,,,\n,,,,,\n")     

        f.write("SCALER INI NAME,SCALER DB NAME,SCALER DESCRIPTION\n") 
        for i in list(scalers.keys()):
            f.write("{},,\n".format(i)) 
        f.write(",,,,,\n,,,,,\n")   

        f.write("WAVEFORM INI NAME, DB NAME, DESCRIPTION, SIZE\n") 
        for i in list(waveforms.keys()):
            f.write("{0},,,{1}\n".format(i, waveforms[i]['Size'])) 
        f.write(",,,,,\n,,,,,\n")                                          
        
