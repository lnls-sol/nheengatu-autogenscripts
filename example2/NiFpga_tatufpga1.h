/*
 * Generated with the FPGA Interface C API Generator 18.0.0
 * for NI-RIO 18.0.0 or later.
 */

#ifndef __NiFpga_tatufpga1_h__
#define __NiFpga_tatufpga1_h__

#ifndef NiFpga_Version
   #define NiFpga_Version 1800
#endif

#include "NiFpga.h"

/**
 * The filename of the FPGA bitfile.
 *
 * This is a #define to allow for string literal concatenation. For example:
 *
 *    static const char* const Bitfile = "C:\\" NiFpga_tatufpga1_Bitfile;
 */
#define NiFpga_tatufpga1_Bitfile "NiFpga_tatufpga1.lvbitx"

/**
 * The signature of the FPGA bitfile.
 */
static const char* const NiFpga_tatufpga1_Signature = "4120C23945F0D5C83C3F6DF44B537C8C";

typedef enum
{
   NiFpga_tatufpga1_IndicatorBool_BI_TatuIO4_RBV = 0x18192,
   NiFpga_tatufpga1_IndicatorBool_BI_TatuIO5_RBV = 0x18196,
   NiFpga_tatufpga1_IndicatorBool_BI_TatuIO6_RBV = 0x1819A,
   NiFpga_tatufpga1_IndicatorBool_BI_TatuIO7_RBV = 0x1819E,
   NiFpga_tatufpga1_IndicatorBool_BI_rele0_RBV = 0x1816E,
   NiFpga_tatufpga1_IndicatorBool_BI_rele1_RBV = 0x18172,
   NiFpga_tatufpga1_IndicatorBool_BI_rele2_RBV = 0x18176,
   NiFpga_tatufpga1_IndicatorBool_BI_rele3_RBV = 0x1817A,
   NiFpga_tatufpga1_IndicatorBool_Done_SCALER = 0x1806A,
   NiFpga_tatufpga1_IndicatorBool_TatuPortP0 = 0x18022,
   NiFpga_tatufpga1_IndicatorBool_TatuPortP1 = 0x18026,
   NiFpga_tatufpga1_IndicatorBool_TatuPortP2 = 0x1802A,
   NiFpga_tatufpga1_IndicatorBool_TatuPortP3 = 0x1802E,
} NiFpga_tatufpga1_IndicatorBool;

typedef enum
{
   NiFpga_tatufpga1_IndicatorU16_FXP_InputTriggerIO0_RBV = 0x1800A,
   NiFpga_tatufpga1_IndicatorU16_FXP_InputTriggerIO1_RBV = 0x18006,
   NiFpga_tatufpga1_IndicatorU16_FXP_InputTriggerIO2_RBV = 0x18002,
   NiFpga_tatufpga1_IndicatorU16_FXP_InputTriggerIO3_RBV = 0x18012,
} NiFpga_tatufpga1_IndicatorU16;

typedef enum
{
   NiFpga_tatufpga1_IndicatorU32_looptime = 0x18074,
} NiFpga_tatufpga1_IndicatorU32;

typedef enum
{
   NiFpga_tatufpga1_IndicatorU64_BI_portas = 0x181A0,
   NiFpga_tatufpga1_IndicatorU64_FXP_HeartBeatFPGA = 0x1815C,
} NiFpga_tatufpga1_IndicatorU64;

typedef enum
{
   NiFpga_tatufpga1_IndicatorSgl_AI_flyscaler_0 = 0x18078,
   NiFpga_tatufpga1_IndicatorSgl_AI_flyscaler_1 = 0x1807C,
   NiFpga_tatufpga1_IndicatorSgl_AI_flyscaler_2 = 0x18080,
   NiFpga_tatufpga1_IndicatorSgl_AI_flyscaler_3 = 0x18084,
   NiFpga_tatufpga1_IndicatorSgl_AI_flyscanpts = 0x18164,
} NiFpga_tatufpga1_IndicatorSgl;

typedef enum
{
   NiFpga_tatufpga1_ControlBool_BO_FlyScanRecord = 0x1816A,
   NiFpga_tatufpga1_ControlBool_BO_ResetAll = 0x1818E,
   NiFpga_tatufpga1_ControlBool_BO_TatuActive = 0x1815A,
   NiFpga_tatufpga1_ControlBool_BO_rele0 = 0x1817E,
   NiFpga_tatufpga1_ControlBool_BO_rele1 = 0x18182,
   NiFpga_tatufpga1_ControlBool_BO_rele2 = 0x18186,
   NiFpga_tatufpga1_ControlBool_BO_rele3 = 0x1818A,
   NiFpga_tatufpga1_ControlBool_Enable_SCALER = 0x18062,
   NiFpga_tatufpga1_ControlBool_OneShot_SCALER = 0x1805E,
   NiFpga_tatufpga1_ControlBool_scalertrigger = 0x18072,
} NiFpga_tatufpga1_ControlBool;

typedef enum
{
   NiFpga_tatufpga1_ControlU64_FXP_InputTriggerIO0 = 0x1800C,
   NiFpga_tatufpga1_ControlU64_FXP_InputTriggerIO1 = 0x18014,
   NiFpga_tatufpga1_ControlU64_FXP_InputTriggerIO2 = 0x18018,
   NiFpga_tatufpga1_ControlU64_FXP_InputTriggerIO3 = 0x1801C,
   NiFpga_tatufpga1_ControlU64_FXP_pulseDurationGench0 = 0x1804C,
   NiFpga_tatufpga1_ControlU64_FXP_pulseDurationGench1 = 0x18048,
   NiFpga_tatufpga1_ControlU64_FXP_pulseDurationGench2 = 0x18044,
   NiFpga_tatufpga1_ControlU64_FXP_pulseDurationGench3 = 0x18040,
   NiFpga_tatufpga1_ControlU64_FXP_pulsePeriodGench0 = 0x18030,
   NiFpga_tatufpga1_ControlU64_FXP_pulsePeriodGench1 = 0x18034,
   NiFpga_tatufpga1_ControlU64_FXP_pulsePeriodGench2 = 0x18038,
   NiFpga_tatufpga1_ControlU64_FXP_pulsePeriodGench3 = 0x1803C,
} NiFpga_tatufpga1_ControlU64;

typedef enum
{
   NiFpga_tatufpga1_ControlSgl_AO_ConditionIO4_0 = 0x180E8,
   NiFpga_tatufpga1_ControlSgl_AO_ConditionIO4_1 = 0x180EC,
   NiFpga_tatufpga1_ControlSgl_AO_ConditionIO4_2 = 0x180F0,
   NiFpga_tatufpga1_ControlSgl_AO_ConditionIO5_0 = 0x180F4,
   NiFpga_tatufpga1_ControlSgl_AO_ConditionIO5_1 = 0x180F8,
   NiFpga_tatufpga1_ControlSgl_AO_ConditionIO5_2 = 0x180FC,
   NiFpga_tatufpga1_ControlSgl_AO_ConditionIO6_0 = 0x18100,
   NiFpga_tatufpga1_ControlSgl_AO_ConditionIO6_1 = 0x18104,
   NiFpga_tatufpga1_ControlSgl_AO_ConditionIO6_2 = 0x18108,
   NiFpga_tatufpga1_ControlSgl_AO_ConditionIO7_0 = 0x1810C,
   NiFpga_tatufpga1_ControlSgl_AO_ConditionIO7_1 = 0x18110,
   NiFpga_tatufpga1_ControlSgl_AO_ConditionIO7_2 = 0x18114,
   NiFpga_tatufpga1_ControlSgl_AO_DelayIO4_0 = 0x18088,
   NiFpga_tatufpga1_ControlSgl_AO_DelayIO4_1 = 0x180BC,
   NiFpga_tatufpga1_ControlSgl_AO_DelayIO4_2 = 0x180C0,
   NiFpga_tatufpga1_ControlSgl_AO_DelayIO5_0 = 0x180C4,
   NiFpga_tatufpga1_ControlSgl_AO_DelayIO5_1 = 0x180C8,
   NiFpga_tatufpga1_ControlSgl_AO_DelayIO5_2 = 0x180CC,
   NiFpga_tatufpga1_ControlSgl_AO_DelayIO6_0 = 0x180D0,
   NiFpga_tatufpga1_ControlSgl_AO_DelayIO6_1 = 0x180D4,
   NiFpga_tatufpga1_ControlSgl_AO_DelayIO6_2 = 0x180D8,
   NiFpga_tatufpga1_ControlSgl_AO_DelayIO7_0 = 0x180DC,
   NiFpga_tatufpga1_ControlSgl_AO_DelayIO7_1 = 0x180E0,
   NiFpga_tatufpga1_ControlSgl_AO_DelayIO7_2 = 0x180E4,
   NiFpga_tatufpga1_ControlSgl_AO_OutputIO4_0 = 0x1808C,
   NiFpga_tatufpga1_ControlSgl_AO_OutputIO4_1 = 0x18090,
   NiFpga_tatufpga1_ControlSgl_AO_OutputIO4_2 = 0x18094,
   NiFpga_tatufpga1_ControlSgl_AO_OutputIO5_0 = 0x18098,
   NiFpga_tatufpga1_ControlSgl_AO_OutputIO5_1 = 0x1809C,
   NiFpga_tatufpga1_ControlSgl_AO_OutputIO5_2 = 0x180A0,
   NiFpga_tatufpga1_ControlSgl_AO_OutputIO6_0 = 0x180A4,
   NiFpga_tatufpga1_ControlSgl_AO_OutputIO6_1 = 0x180A8,
   NiFpga_tatufpga1_ControlSgl_AO_OutputIO6_2 = 0x180AC,
   NiFpga_tatufpga1_ControlSgl_AO_OutputIO7_0 = 0x180B0,
   NiFpga_tatufpga1_ControlSgl_AO_OutputIO7_1 = 0x180B4,
   NiFpga_tatufpga1_ControlSgl_AO_OutputIO7_2 = 0x180B8,
   NiFpga_tatufpga1_ControlSgl_AO_PulseIO4_0 = 0x18118,
   NiFpga_tatufpga1_ControlSgl_AO_PulseIO4_1 = 0x1811C,
   NiFpga_tatufpga1_ControlSgl_AO_PulseIO4_2 = 0x18120,
   NiFpga_tatufpga1_ControlSgl_AO_PulseIO5_0 = 0x18124,
   NiFpga_tatufpga1_ControlSgl_AO_PulseIO5_1 = 0x18128,
   NiFpga_tatufpga1_ControlSgl_AO_PulseIO5_2 = 0x1812C,
   NiFpga_tatufpga1_ControlSgl_AO_PulseIO6_0 = 0x18130,
   NiFpga_tatufpga1_ControlSgl_AO_PulseIO6_1 = 0x18134,
   NiFpga_tatufpga1_ControlSgl_AO_PulseIO6_2 = 0x18138,
   NiFpga_tatufpga1_ControlSgl_AO_PulseIO7_0 = 0x1813C,
   NiFpga_tatufpga1_ControlSgl_AO_PulseIO7_1 = 0x18140,
   NiFpga_tatufpga1_ControlSgl_AO_PulseIO7_2 = 0x18144,
   NiFpga_tatufpga1_ControlSgl_AO_modeGench0 = 0x18148,
   NiFpga_tatufpga1_ControlSgl_AO_modeGench1 = 0x1814C,
   NiFpga_tatufpga1_ControlSgl_AO_modeGench2 = 0x18150,
   NiFpga_tatufpga1_ControlSgl_AO_modeGench3 = 0x18154,
   NiFpga_tatufpga1_ControlSgl_AO_shiftLeft = 0x1806C,
} NiFpga_tatufpga1_ControlSgl;

typedef enum
{
   NiFpga_tatufpga1_IndicatorArrayU32_Counter_SCALER = 0x18064,
} NiFpga_tatufpga1_IndicatorArrayU32;

typedef enum
{
   NiFpga_tatufpga1_IndicatorArrayU32Size_Counter_SCALER = 5,
} NiFpga_tatufpga1_IndicatorArrayU32Size;

typedef enum
{
   NiFpga_tatufpga1_IndicatorArrayU64_appendedarray = 0x18160,
} NiFpga_tatufpga1_IndicatorArrayU64;

typedef enum
{
   NiFpga_tatufpga1_IndicatorArrayU64Size_appendedarray = 5,
} NiFpga_tatufpga1_IndicatorArrayU64Size;

typedef enum
{
   NiFpga_tatufpga1_ControlArrayBool_Gate_SCALER = 0x1805A,
} NiFpga_tatufpga1_ControlArrayBool;

typedef enum
{
   NiFpga_tatufpga1_ControlArrayBoolSize_Gate_SCALER = 5,
} NiFpga_tatufpga1_ControlArrayBoolSize;

typedef enum
{
   NiFpga_tatufpga1_ControlArrayU32_AnalogInputs_SCALER = 0x18050,
   NiFpga_tatufpga1_ControlArrayU32_PresetValues_SCALER = 0x18054,
} NiFpga_tatufpga1_ControlArrayU32;

typedef enum
{
   NiFpga_tatufpga1_ControlArrayU32Size_AnalogInputs_SCALER = 4,
   NiFpga_tatufpga1_ControlArrayU32Size_PresetValues_SCALER = 5,
} NiFpga_tatufpga1_ControlArrayU32Size;

typedef enum
{
   NiFpga_tatufpga1_TargetToHostFifoU64_FIFOFPGAparaRT = 0,
} NiFpga_tatufpga1_TargetToHostFifoU64;

#endif
