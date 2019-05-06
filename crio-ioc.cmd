#!/usr/local/epics/apps/crio-ioc/bin/linux-x86_64/CRIO

< /usr/local/epics/apps/crio-ioc/iocBoot/iocCRIO/envPaths

cd ${TOP}

## Register all support components
dbLoadDatabase "dbd/CRIO.dbd"
CRIO_registerRecordDeviceDriver pdbbase

crioSupSetup("/usr/local/epics/apps/config/crio-ioc/cfg.ini" , 1)

## Load record instances

cd ${TOP}/iocBoot/${IOC}

dbLoadTemplate "/usr/local/epics/apps/config/crio-ioc/bi.template"
dbLoadTemplate "/usr/local/epics/apps/config/crio-ioc/bo.template"
dbLoadTemplate "/usr/local/epics/apps/config/crio-ioc/ai.template"
dbLoadTemplate "/usr/local/epics/apps/config/crio-ioc/ao.template"
dbLoadTemplate "/usr/local/epics/apps/config/crio-ioc/scaler.template"


iocInit

dbl

