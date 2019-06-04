#!/home/ABTLUS/dawood.alnajjar/work/crio-ioc/bin/linux-x86_64/CRIO
< /home/ABTLUS/dawood.alnajjar/work/crio-ioc/iocBoot/iocCRIO/envPaths

#!/usr/local/epics/apps/crio-ioc/bin/linux-x86_64/CRIO
#< /usr/local/epics/apps/crio-ioc/iocBoot/iocCRIO/envPaths


cd ${TOP}

## Register all support components
dbLoadDatabase "dbd/CRIO.dbd"
CRIO_registerRecordDeviceDriver pdbbase

crioSupSetup("/usr/local/epics/apps/config/crio-ioc/cfg.ini" , 1)

## Load record instances

cd ${TOP}/iocBoot/${IOC}

dbLoadTemplate "/usr/local/epics/apps/config/crio-ioc/bi.db.sub"
dbLoadTemplate "/usr/local/epics/apps/config/crio-ioc/bo.db.sub"
dbLoadTemplate "/usr/local/epics/apps/config/crio-ioc/ai.db.sub"
dbLoadTemplate "/usr/local/epics/apps/config/crio-ioc/ao.db.sub"
dbLoadTemplate "/usr/local/epics/apps/config/crio-ioc/scaler.db.sub"
dbLoadTemplate "/usr/local/epics/apps/config/crio-ioc/waveform.db.sub"
iocInit

dbl



