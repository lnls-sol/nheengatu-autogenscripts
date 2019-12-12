/*
 * Generated with the FPGA Interface C API Generator 18.0.0
 * for NI-RIO 18.0.0 or later.
 */

#ifndef __NiFpga_bool_test_h__
#define __NiFpga_bool_test_h__

#ifndef NiFpga_Version
   #define NiFpga_Version 1800
#endif

#include "NiFpga.h"

/**
 * The filename of the FPGA bitfile.
 *
 * This is a #define to allow for string literal concatenation. For example:
 *
 *    static const char* const Bitfile = "C:\\" NiFpga_bool_test_Bitfile;
 */
#define NiFpga_bool_test_Bitfile "NiFpga_bool_test.lvbitx"

/**
 * The signature of the FPGA bitfile.
 */
static const char* const NiFpga_bool_test_Signature = "BCEFC2CA6F107120DA381B861940A752";

typedef enum
{
   NiFpga_bool_test_IndicatorBool_BI_led0 = 0x18006,
   NiFpga_bool_test_IndicatorBool_BI_led1 = 0x1800A,
   NiFpga_bool_test_IndicatorBool_BI_led2 = 0x18016,
   NiFpga_bool_test_IndicatorBool_BI_led3 = 0x1801A,
   NiFpga_bool_test_IndicatorBool_Done_SCALER = 0x1803A,
} NiFpga_bool_test_IndicatorBool;

typedef enum
{
   NiFpga_bool_test_IndicatorU16_MBBI0 = 0x180D2,
   NiFpga_bool_test_IndicatorU16_MBBI1 = 0x180CE,
} NiFpga_bool_test_IndicatorU16;

typedef enum
{
   NiFpga_bool_test_IndicatorU32_Looptime = 0x18054,
} NiFpga_bool_test_IndicatorU32;

typedef enum
{
   NiFpga_bool_test_IndicatorU64_BI_VECTOR = 0x18020,
   NiFpga_bool_test_IndicatorU64_aifxp1 = 0x1809C,
   NiFpga_bool_test_IndicatorU64_aifxp2 = 0x18094,
   NiFpga_bool_test_IndicatorU64_aifxp3 = 0x1808C,
   NiFpga_bool_test_IndicatorU64_aifxp4 = 0x18084,
   NiFpga_bool_test_IndicatorU64_aifxp5 = 0x1807C,
   NiFpga_bool_test_IndicatorU64_aifxp6 = 0x18074,
   NiFpga_bool_test_IndicatorU64_fxp_AnalogOutput0_SCALER = 0x18034,
   NiFpga_bool_test_IndicatorU64_fxp_AnalogOutput1_SCALER = 0x18030,
   NiFpga_bool_test_IndicatorU64_fxp_AnalogOutput2_SCALER = 0x1802C,
   NiFpga_bool_test_IndicatorU64_fxp_AnalogOutput3_SCALER = 0x18028,
} NiFpga_bool_test_IndicatorU64;

typedef enum
{
   NiFpga_bool_test_IndicatorSgl_AI0 = 0x180B4,
   NiFpga_bool_test_IndicatorSgl_AI1 = 0x180B8,
   NiFpga_bool_test_IndicatorSgl_AI2 = 0x180BC,
   NiFpga_bool_test_IndicatorSgl_AI3 = 0x180C0,
} NiFpga_bool_test_IndicatorSgl;

typedef enum
{
   NiFpga_bool_test_ControlBool_BO0 = 0x18002,
   NiFpga_bool_test_ControlBool_BO1 = 0x1800E,
   NiFpga_bool_test_ControlBool_BO2 = 0x18012,
   NiFpga_bool_test_ControlBool_BO3 = 0x1801E,
   NiFpga_bool_test_ControlBool_Enable_SCALER = 0x18052,
   NiFpga_bool_test_ControlBool_OneShot_SCALER = 0x1804E,
   NiFpga_bool_test_ControlBool_SampleAnalog_SCALER = 0x1804A,
} NiFpga_bool_test_ControlBool;

typedef enum
{
   NiFpga_bool_test_ControlU16_MBBO0 = 0x180C6,
   NiFpga_bool_test_ControlU16_MBBO1 = 0x180CA,
} NiFpga_bool_test_ControlU16;

typedef enum
{
   NiFpga_bool_test_ControlU64_aofxp1 = 0x18070,
   NiFpga_bool_test_ControlU64_aofxp2 = 0x1806C,
   NiFpga_bool_test_ControlU64_aofxp3 = 0x18068,
   NiFpga_bool_test_ControlU64_aofxp4 = 0x18064,
   NiFpga_bool_test_ControlU64_aofxp5 = 0x18060,
   NiFpga_bool_test_ControlU64_aofxp6 = 0x1805C,
   NiFpga_bool_test_ControlU64_fxp_ShiftLeft_SCALER = 0x1803C,
} NiFpga_bool_test_ControlU64;

typedef enum
{
   NiFpga_bool_test_ControlSgl_AO0 = 0x180A4,
   NiFpga_bool_test_ControlSgl_AO1 = 0x180A8,
   NiFpga_bool_test_ControlSgl_AO2 = 0x180AC,
   NiFpga_bool_test_ControlSgl_AO3 = 0x180B0,
} NiFpga_bool_test_ControlSgl;

typedef enum
{
   NiFpga_bool_test_IndicatorArrayU32_Counter_SCALER = 0x18024,
} NiFpga_bool_test_IndicatorArrayU32;

typedef enum
{
   NiFpga_bool_test_IndicatorArrayU32Size_Counter_SCALER = 5,
} NiFpga_bool_test_IndicatorArrayU32Size;

typedef enum
{
   NiFpga_bool_test_ControlArrayBool_Gate_SCALER = 0x18046,
} NiFpga_bool_test_ControlArrayBool;

typedef enum
{
   NiFpga_bool_test_ControlArrayBoolSize_Gate_SCALER = 5,
} NiFpga_bool_test_ControlArrayBoolSize;

typedef enum
{
   NiFpga_bool_test_ControlArrayU32_PresetValues_SCALER = 0x18040,
} NiFpga_bool_test_ControlArrayU32;

typedef enum
{
   NiFpga_bool_test_ControlArrayU32Size_PresetValues_SCALER = 5,
} NiFpga_bool_test_ControlArrayU32Size;

#endif
