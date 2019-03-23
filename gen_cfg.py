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

### HELPER FUNCTIONS
def printToFile(file, key, items):
    f.write("[{}]\n".format(key))
    for key,value in items.items():
        f.write("{}={}\n".format(key,value))   
    f.write("\n\n")     


def buildTemplate(tplhdr, tplbdy, beamline, dtype, pins, db, fname, freq = -1):
    tpls = tplhdr.format(db)
    if(freq != -1): #SCALER
        for key in pins.keys():
            tpls = tpls + tplbdy.format(beamline, dtype, freq, key)
    else: # OTHER
        for key, val in pins.items():
            tpls = tpls + tplbdy.format(beamline, dtype, key)

    tpls = tpls + "\n}"
    with open("{}/{}.template".format(args.dst, fname) , "w") as f:
        print("Generating {}/{}.template file".format(args.dst, fname))
        f.write(tpls)
        


description = 'This programs extracts the address in the header file generated by the FPGA C API, and generates ini and template files for EPICS.'

header = '; Automatically generated ini file for CRIO library\n\
; The settings required to setup the CRIO environment are here\n\
; - Destination Crio IP: The IP address of the target CRIO\n\
;                        For safety, our intention is to keep this\n\
;                        IP as the loopback address (127.0.0.1)\n\
; - Path: is the path to the bitfile that will be used to configure\n\
;         the FPGA of the target CRIO.\n\
; - Bitfile Name: Is the name of the bitfile\n\
; - Signature: Is the signature of that specific bitfile\n\
; - Use Shared Memory: Set to 1 if labviewRT will open a shared memory\n\
; - Shared Memory Path: If Use Shared Memory is set to 1, then this path\n\
;                       will be used.\n\
\n\
;\n\
;Naming Considerations:\n\
;    RT Variables:\n\
;        The keyword RT_ is reserved for variables that are defined \n\
;        in labview RT. Do not use this reserved word in your names\n\
;        unless it is an RT variable, otherwise it will be ignored!\n\
;        Keywords for realtime double, single, signed 8, 16, 32, 64 \n\
;        and unsigned 8, 16, 32, 64 are defined as follows\n\
;        Double          : RT_DBL_<NAME>\n\
;        Single          : RT_SGL_<NAME>\n\
;        Unsigned 64 bit : RT_U64_<NAME>\n\
;        Unsigned 32 bit : RT_U32_<NAME>\n\
;        Unsigned 16 bit : RT_U16_<NAME>\n\
;        Unsigned 08 bit : RT_U08_<NAME>\n\
;        Signed 64 bit   : RT_I64_<NAME>\n\
;        Signed 32 bit   : RT_I32_<NAME>\n\
;        Signed 16 bit   : RT_I16_<NAME>\n\
;        Signed 08 bit   : RT_I08_<NAME>\n\
;\n\
;    FPGA variables naming:\n\
;        FPGA variables must have one of the following keywords:\n\
;        AI, AO, BI, BO \n\
;\n\
;\n\
;Checks implemented in the library:\n\
; Checking for same address / index within a category has been\n\
; implemented. An exception is throw upon occurance.\n\
\n\
\n\
\n\n'


# initiate the parser
parser = argparse.ArgumentParser(description=description)

# Input parameters
parser.add_argument("input",  help="Name of input header file to be processed")
parser.add_argument("-u", "--useSM", help="Use shared memory", action='store_true')
parser.add_argument("-d", "--dst", default="out", help="Name of the output folder. Default is <out>")
parser.add_argument("--ip", help="Destination IP of the CRIO. Default is <127.0.0.1>", default = '127.0.0.1')
parser.add_argument( "-p", "--path", help="Bitfile path. Default is </CHANGEME/>", default = '/CHANGEME/')
parser.add_argument("-s", "--src", help="Folder containing all files necessary for ini/template generation", default = '.')
parser.add_argument("--smfname", help="Shared memory file path and name", default = '/labview_linux_sm')
parser.add_argument("--aikey", help="AI keyword that any AI variable will start with in the headerfile. Default is <Mod>", default = 'Mod')
parser.add_argument("--aokey", help="AO keyword that any AO variable will start with in the headerfile Default is <Mod>", default = 'Mod')
parser.add_argument("--bokey", help="BO keyword that any BO variable will start with in the headerfile. Default is <Mod>", default = 'Mod')
parser.add_argument("--bikey", help="BI keyword that any AI variable will start with in the headerfile. Default is <BI>", default = 'BI')
parser.add_argument("--scalerkey", help="Scaler keyword that any Scaler variable will be followed with in the headerfile. Default is <SCALER>", default = 'SCALER')
parser.add_argument("--beamline", help="Name of the beamline (for template file generation). Default is <SOL>", default = 'SOL')
parser.add_argument("--freq", help="Scaler Frequency. Default is <10000000>", default = '10000000')
parser.add_argument("--bidtyp", help="DTYPE of BI record", default = 'CrioBI')
parser.add_argument("--aidtyp", help="DTYPE of AI record", default = 'CrioAI')
parser.add_argument("--bodtyp", help="DTYPE of BO record", default = 'CrioBO')
parser.add_argument("--aodtyp", help="DTYPE of AO record", default = 'CrioAO')
parser.add_argument("--crio", help="Name of the CRIO. Default is <CHANGEME>", default = 'CHANGEME')
parser.add_argument("--scalerdtyp", help="DTYPE of Scaler record", default = 'CRIO Scaler')


# read arguments from the command line
args = parser.parse_args()

# read header file
with open(args.input) as f:
    lines = f.readlines()

if (args.useSM !=0 and args.useSM != 1):
    print("useSM parameter must be 0 or 1.")
    parser.print_help()
    sys.exit(2)    
    
# *.ini key dictionaries
settings = {'Destination Crio IP' : args.ip,
            'Path':args.path,
            'Use Shared Memory': 1 if(args.useSM) else 0,
            'Shared Memory Path': args.smfname}
biaddr = {}
boaddr = {}
aoaddr = {}
aiaddr = {}
bilist = []
rtlist = []
bidict = collections.OrderedDict()
scalers = collections.defaultdict(dict)
rtvarCount = 0;
fpgavarCount = 0;



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
    
    
    # Extracting Settings                       
    result = re.search('_Signature\s*=\s*\"([A-F0-9]{32})\"', line)
    if (result is not None):
        settings['Signature']=(result.group(1))
    else:
        result = re.search('_Bitfile \"([a-zA-Z0-9_]+.lvbitx)\"', line)
        if (result is not None):
            settings['Bitfile Name']=(result.group(1))
        else:
            # Extracting BI, BO, AI, AO  
            result = re.search('IndicatorU64_('+args.bikey+'[a-zA-Z0-9_]*) = 0x([A-F0-9]{5})', line)
            if (result is not None):
                biaddr[result.group(1)]=(result.group(2))
                fpgavarCount += 1
                #found BI. Parse associated BI file.
                bi = result.group(1)
                bilist = [bi.rstrip() for bi in open('{}/{}.list'.format(args.src, bi))]
                bidict = { i : bilist[i] for i in range(0, len(bilist) ) }
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


#process RT variables if enabled
if (args.useSM == 1):
    rtlist = [rt.rstrip() for rt in open('{}/RT.list'.format(args.src))]
    for i, val in enumerate(rtlist):
        result = re.search('RT_[A-Z0-9]{3}_AO', val)
        if (result is not None):
            aoaddr[val]=i 
            rtvarCount += 1
        result = re.search('RT_BOL_BO', val)
        if (result is not None):
            boaddr[val]=i
            rtvarCount += 1            
        result = re.search('RT_[A-Z0-9]{3}_AI', val)
        if (result is not None):
            aiaddr[val]=i
            rtvarCount += 1            
        result = re.search('RT_BOL_BI', val)
        if (result is not None):
            biaddr[val]=i
            rtvarCount += 1            

if not os.path.exists(args.dst):
    os.makedirs(args.dst)

print( "{} RT variables processed\n{} FPGA addresses extracted".format(rtvarCount, fpgavarCount))
with open("{}/cfg.ini".format(args.dst) , "w") as f:
    print("Generating {}/cfg.ini".format(args.dst))
    f.write(header)
    printToFile(f, 'Settings', settings)
    printToFile(f, 'BIAddresses', biaddr)
    printToFile(f, bi, bidict)
    printToFile(f, 'AO', aoaddr)
    printToFile(f, 'AI', aiaddr)
    printToFile(f, 'BO', boaddr)
    # Convert scaler names to list then to dictionary for printing
    scalerNameList = list(scalers.keys())
    scalerNamesDict = { scalerNameList[i] : i for i in range(0, len(scalerNameList) ) }
    printToFile(f, 'SCALERS', scalerNamesDict)
    for scaler in scalers:
        printToFile(f, scaler, scalers[scaler])




        

#template definitions
tplhdr = 'file \"$(TOP)/db/{0}\"\n{{\npattern\n{{BL, EQ, DTYP, PIN}}\n'
tplbdy = '{{\"{0}", \"'+args.crio+':CHANGEME:CHANGEME\", \"{1}\", \"{2}\"}}\n'
tplsclrhdr = 'file \"$(TOP)/db/{0}\"\n{{\npattern\n{{BL, EQ, DTYP, FREQ, PIN}}\n'
tplsclrbdy = '{{\"{0}", \"'+args.crio+':CHANGEME:CHANGEME\", \"{1}\", \"{2}\", \"{3}\"}}\n'


#Generate templates   
buildTemplate(tplhdr, tplbdy, args.beamline, args.aodtyp, aoaddr, "devAOCRIO.db", 'ao')
buildTemplate(tplhdr, tplbdy, args.beamline, args.aidtyp, aiaddr, "devAICRIO.db", 'ai')
buildTemplate(tplhdr, tplbdy, args.beamline, args.bidtyp, biaddr, "devBICRIO.db", 'bi')
buildTemplate(tplhdr, tplbdy, args.beamline, args.bodtyp, boaddr, "devBOCRIO.db", 'bo')
buildTemplate(tplsclrhdr, tplsclrbdy, args.beamline, args.scalerdtyp, scalerNamesDict, "devScalerCRIO.db", 'scaler', args.freq)       


