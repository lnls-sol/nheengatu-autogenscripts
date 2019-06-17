/*
 * Generated with the FPGA Interface C API Generator 18.0.0
 * for NI-RIO 18.0.0 or later.
 */

#ifndef __NiFpga_fpga_all_example_h__
#define __NiFpga_fpga_all_example_h__

#ifndef NiFpga_Version
   #define NiFpga_Version 1800
#endif

#include "NiFpga.h"

/**
 * The filename of the FPGA bitfile.
 *
 * This is a #define to allow for string literal concatenation. For example:
 *
 *    static const char* const Bitfile = "C:\\" NiFpga_fpga_all_example_Bitfile;
 */
#define NiFpga_fpga_all_example_Bitfile "NiFpga_fpga_all_example.lvbitx"

/**
 * The signature of the FPGA bitfile.
 */
static const char* const NiFpga_fpga_all_example_Signature = "809D35369A7293F0FD95F203319A923D";

typedef enum
{
   NiFpga_fpga_all_example_IndicatorBool_Done_SCALER1 = 0x180B2,
   NiFpga_fpga_all_example_IndicatorBool_Done_SCALER2 = 0x180C6,
} NiFpga_fpga_all_example_IndicatorBool;

typedef enum
{
   NiFpga_fpga_all_example_IndicatorU32_Looptime = 0x180E0,
} NiFpga_fpga_all_example_IndicatorU32;

typedef enum
{
   NiFpga_fpga_all_example_IndicatorU64_BI = 0x18040,
   NiFpga_fpga_all_example_IndicatorU64_aifxp1 = 0x1816C,
   NiFpga_fpga_all_example_IndicatorU64_aifxp2 = 0x18164,
   NiFpga_fpga_all_example_IndicatorU64_aifxp3 = 0x1815C,
   NiFpga_fpga_all_example_IndicatorU64_aifxp4 = 0x18154,
   NiFpga_fpga_all_example_IndicatorU64_aifxp5 = 0x1814C,
   NiFpga_fpga_all_example_IndicatorU64_aifxp6 = 0x18144,
} NiFpga_fpga_all_example_IndicatorU64;

typedef enum
{
   NiFpga_fpga_all_example_IndicatorSgl_aiMod4AI0 = 0x18030,
   NiFpga_fpga_all_example_IndicatorSgl_aiMod4AI1 = 0x18034,
   NiFpga_fpga_all_example_IndicatorSgl_aiMod4AI2 = 0x18038,
   NiFpga_fpga_all_example_IndicatorSgl_aiMod4AI3 = 0x1803C,
   NiFpga_fpga_all_example_IndicatorSgl_aiMod7AI0 = 0x18010,
   NiFpga_fpga_all_example_IndicatorSgl_aiMod7AI1 = 0x18014,
   NiFpga_fpga_all_example_IndicatorSgl_aiMod7AI2 = 0x18018,
   NiFpga_fpga_all_example_IndicatorSgl_aiMod7AI3 = 0x1801C,
   NiFpga_fpga_all_example_IndicatorSgl_aiMod8AI0 = 0x1800C,
   NiFpga_fpga_all_example_IndicatorSgl_aiMod8AI1 = 0x18008,
   NiFpga_fpga_all_example_IndicatorSgl_aiMod8AI2 = 0x18004,
   NiFpga_fpga_all_example_IndicatorSgl_aiMod8AI3 = 0x18000,
} NiFpga_fpga_all_example_IndicatorSgl;

typedef enum
{
   NiFpga_fpga_all_example_ControlBool_Enable_SCALER1 = 0x180BA,
   NiFpga_fpga_all_example_ControlBool_Enable_SCALER2 = 0x180CE,
   NiFpga_fpga_all_example_ControlBool_Mod1DIO0 = 0x18052,
   NiFpga_fpga_all_example_ControlBool_Mod1DIO1 = 0x1804E,
   NiFpga_fpga_all_example_ControlBool_Mod1DIO2 = 0x1804A,
   NiFpga_fpga_all_example_ControlBool_Mod1DIO3 = 0x18046,
   NiFpga_fpga_all_example_ControlBool_Mod2DIO0 = 0x18062,
   NiFpga_fpga_all_example_ControlBool_Mod2DIO1 = 0x1805E,
   NiFpga_fpga_all_example_ControlBool_Mod2DIO2 = 0x1805A,
   NiFpga_fpga_all_example_ControlBool_Mod2DIO3 = 0x18056,
   NiFpga_fpga_all_example_ControlBool_Mod3DIO16 = 0x18066,
   NiFpga_fpga_all_example_ControlBool_Mod3DIO17 = 0x1806A,
   NiFpga_fpga_all_example_ControlBool_Mod3DIO18 = 0x1806E,
   NiFpga_fpga_all_example_ControlBool_Mod3DIO19 = 0x18072,
   NiFpga_fpga_all_example_ControlBool_Mod3DIO20 = 0x18076,
   NiFpga_fpga_all_example_ControlBool_Mod3DIO21 = 0x1807A,
   NiFpga_fpga_all_example_ControlBool_Mod3DIO22 = 0x1807E,
   NiFpga_fpga_all_example_ControlBool_Mod3DIO23 = 0x18082,
   NiFpga_fpga_all_example_ControlBool_Mod3DIO24 = 0x18086,
   NiFpga_fpga_all_example_ControlBool_Mod3DIO25 = 0x1808A,
   NiFpga_fpga_all_example_ControlBool_Mod3DIO26 = 0x1808E,
   NiFpga_fpga_all_example_ControlBool_Mod3DIO27 = 0x18092,
   NiFpga_fpga_all_example_ControlBool_Mod3DIO28 = 0x18096,
   NiFpga_fpga_all_example_ControlBool_Mod3DIO29 = 0x1809A,
   NiFpga_fpga_all_example_ControlBool_Mod3DIO30 = 0x1809E,
   NiFpga_fpga_all_example_ControlBool_Mod3DIO31 = 0x180A2,
   NiFpga_fpga_all_example_ControlBool_OneShot_SCALER1 = 0x180BE,
   NiFpga_fpga_all_example_ControlBool_OneShot_SCALER2 = 0x180D2,
   NiFpga_fpga_all_example_ControlBool_SampleAnalog_SCALER2 = 0x180C2,
} NiFpga_fpga_all_example_ControlBool;

typedef enum
{
   NiFpga_fpga_all_example_ControlU64_aofxp1 = 0x18140,
   NiFpga_fpga_all_example_ControlU64_aofxp2 = 0x1813C,
   NiFpga_fpga_all_example_ControlU64_aofxp3 = 0x18138,
   NiFpga_fpga_all_example_ControlU64_aofxp4 = 0x18134,
   NiFpga_fpga_all_example_ControlU64_aofxp5 = 0x18130,
   NiFpga_fpga_all_example_ControlU64_aofxp6 = 0x1812C,
} NiFpga_fpga_all_example_ControlU64;

typedef enum
{
   NiFpga_fpga_all_example_ControlSgl_aoMod5AO0 = 0x1802C,
   NiFpga_fpga_all_example_ControlSgl_aoMod5AO1 = 0x18028,
   NiFpga_fpga_all_example_ControlSgl_aoMod5AO2 = 0x18024,
   NiFpga_fpga_all_example_ControlSgl_aoMod5AO3 = 0x18020,
} NiFpga_fpga_all_example_ControlSgl;

typedef enum
{
   NiFpga_fpga_all_example_IndicatorArrayI8_waveform_i82 = 0x18100,
} NiFpga_fpga_all_example_IndicatorArrayI8;

typedef enum
{
   NiFpga_fpga_all_example_IndicatorArrayI8Size_waveform_i82 = 3,
} NiFpga_fpga_all_example_IndicatorArrayI8Size;

typedef enum
{
   NiFpga_fpga_all_example_IndicatorArrayU8_waveform_u82 = 0x18108,
} NiFpga_fpga_all_example_IndicatorArrayU8;

typedef enum
{
   NiFpga_fpga_all_example_IndicatorArrayU8Size_waveform_u82 = 3,
} NiFpga_fpga_all_example_IndicatorArrayU8Size;

typedef enum
{
   NiFpga_fpga_all_example_IndicatorArrayI16_waveform_i162 = 0x180F8,
} NiFpga_fpga_all_example_IndicatorArrayI16;

typedef enum
{
   NiFpga_fpga_all_example_IndicatorArrayI16Size_waveform_i162 = 3,
} NiFpga_fpga_all_example_IndicatorArrayI16Size;

typedef enum
{
   NiFpga_fpga_all_example_IndicatorArrayU16_waveform_u162 = 0x18110,
} NiFpga_fpga_all_example_IndicatorArrayU16;

typedef enum
{
   NiFpga_fpga_all_example_IndicatorArrayU16Size_waveform_u162 = 3,
} NiFpga_fpga_all_example_IndicatorArrayU16Size;

typedef enum
{
   NiFpga_fpga_all_example_IndicatorArrayI32_waveform_i322 = 0x180F0,
} NiFpga_fpga_all_example_IndicatorArrayI32;

typedef enum
{
   NiFpga_fpga_all_example_IndicatorArrayI32Size_waveform_i322 = 3,
} NiFpga_fpga_all_example_IndicatorArrayI32Size;

typedef enum
{
   NiFpga_fpga_all_example_IndicatorArrayU32_AnalogInputs_SCALER2 = 0x180DC,
   NiFpga_fpga_all_example_IndicatorArrayU32_Counter_SCALER1 = 0x180AC,
   NiFpga_fpga_all_example_IndicatorArrayU32_Counter_SCALER2 = 0x180C8,
   NiFpga_fpga_all_example_IndicatorArrayU32_waveform_u32 = 0x18124,
} NiFpga_fpga_all_example_IndicatorArrayU32;

typedef enum
{
   NiFpga_fpga_all_example_IndicatorArrayU32Size_AnalogInputs_SCALER2 = 1,
   NiFpga_fpga_all_example_IndicatorArrayU32Size_Counter_SCALER1 = 2,
   NiFpga_fpga_all_example_IndicatorArrayU32Size_Counter_SCALER2 = 2,
   NiFpga_fpga_all_example_IndicatorArrayU32Size_waveform_u32 = 3,
} NiFpga_fpga_all_example_IndicatorArrayU32Size;

typedef enum
{
   NiFpga_fpga_all_example_IndicatorArrayI64_waveform_i642 = 0x180E8,
} NiFpga_fpga_all_example_IndicatorArrayI64;

typedef enum
{
   NiFpga_fpga_all_example_IndicatorArrayI64Size_waveform_i642 = 3,
} NiFpga_fpga_all_example_IndicatorArrayI64Size;

typedef enum
{
   NiFpga_fpga_all_example_IndicatorArrayU64_waveform_u642 = 0x18120,
} NiFpga_fpga_all_example_IndicatorArrayU64;

typedef enum
{
   NiFpga_fpga_all_example_IndicatorArrayU64Size_waveform_u642 = 3,
} NiFpga_fpga_all_example_IndicatorArrayU64Size;

typedef enum
{
   NiFpga_fpga_all_example_IndicatorArraySgl_waveform_sgl2 = 0x1811C,
} NiFpga_fpga_all_example_IndicatorArraySgl;

typedef enum
{
   NiFpga_fpga_all_example_IndicatorArraySglSize_waveform_sgl2 = 3,
} NiFpga_fpga_all_example_IndicatorArraySglSize;

typedef enum
{
   NiFpga_fpga_all_example_ControlArrayBool_Gate_SCALER1 = 0x180B6,
   NiFpga_fpga_all_example_ControlArrayBool_Gate_SCALER2 = 0x180D6,
   NiFpga_fpga_all_example_ControlArrayBool_Pulse_SCALER1 = 0x180A6,
} NiFpga_fpga_all_example_ControlArrayBool;

typedef enum
{
   NiFpga_fpga_all_example_ControlArrayBoolSize_Gate_SCALER1 = 2,
   NiFpga_fpga_all_example_ControlArrayBoolSize_Gate_SCALER2 = 2,
   NiFpga_fpga_all_example_ControlArrayBoolSize_Pulse_SCALER1 = 1,
} NiFpga_fpga_all_example_ControlArrayBoolSize;

typedef enum
{
   NiFpga_fpga_all_example_ControlArrayI8_waveform_i8 = 0x180FC,
} NiFpga_fpga_all_example_ControlArrayI8;

typedef enum
{
   NiFpga_fpga_all_example_ControlArrayI8Size_waveform_i8 = 3,
} NiFpga_fpga_all_example_ControlArrayI8Size;

typedef enum
{
   NiFpga_fpga_all_example_ControlArrayU8_waveform_u8 = 0x18104,
} NiFpga_fpga_all_example_ControlArrayU8;

typedef enum
{
   NiFpga_fpga_all_example_ControlArrayU8Size_waveform_u8 = 3,
} NiFpga_fpga_all_example_ControlArrayU8Size;

typedef enum
{
   NiFpga_fpga_all_example_ControlArrayI16_waveform_i16 = 0x180F4,
} NiFpga_fpga_all_example_ControlArrayI16;

typedef enum
{
   NiFpga_fpga_all_example_ControlArrayI16Size_waveform_i16 = 3,
} NiFpga_fpga_all_example_ControlArrayI16Size;

typedef enum
{
   NiFpga_fpga_all_example_ControlArrayU16_waveform_u16 = 0x1810C,
} NiFpga_fpga_all_example_ControlArrayU16;

typedef enum
{
   NiFpga_fpga_all_example_ControlArrayU16Size_waveform_u16 = 3,
} NiFpga_fpga_all_example_ControlArrayU16Size;

typedef enum
{
   NiFpga_fpga_all_example_ControlArrayI32_waveform_i32 = 0x180EC,
} NiFpga_fpga_all_example_ControlArrayI32;

typedef enum
{
   NiFpga_fpga_all_example_ControlArrayI32Size_waveform_i32 = 3,
} NiFpga_fpga_all_example_ControlArrayI32Size;

typedef enum
{
   NiFpga_fpga_all_example_ControlArrayU32_PresetValues_SCALER1 = 0x180A8,
   NiFpga_fpga_all_example_ControlArrayU32_PresetValues_SCALER2 = 0x180D8,
   NiFpga_fpga_all_example_ControlArrayU32_waveform_u322 = 0x18128,
} NiFpga_fpga_all_example_ControlArrayU32;

typedef enum
{
   NiFpga_fpga_all_example_ControlArrayU32Size_PresetValues_SCALER1 = 2,
   NiFpga_fpga_all_example_ControlArrayU32Size_PresetValues_SCALER2 = 2,
   NiFpga_fpga_all_example_ControlArrayU32Size_waveform_u322 = 3,
} NiFpga_fpga_all_example_ControlArrayU32Size;

typedef enum
{
   NiFpga_fpga_all_example_ControlArrayI64_waveform_i64 = 0x180E4,
} NiFpga_fpga_all_example_ControlArrayI64;

typedef enum
{
   NiFpga_fpga_all_example_ControlArrayI64Size_waveform_i64 = 3,
} NiFpga_fpga_all_example_ControlArrayI64Size;

typedef enum
{
   NiFpga_fpga_all_example_ControlArrayU64_waveform_u64 = 0x18118,
} NiFpga_fpga_all_example_ControlArrayU64;

typedef enum
{
   NiFpga_fpga_all_example_ControlArrayU64Size_waveform_u64 = 3,
} NiFpga_fpga_all_example_ControlArrayU64Size;

typedef enum
{
   NiFpga_fpga_all_example_ControlArraySgl_waveform_sgl = 0x18114,
} NiFpga_fpga_all_example_ControlArraySgl;

typedef enum
{
   NiFpga_fpga_all_example_ControlArraySglSize_waveform_sgl = 3,
} NiFpga_fpga_all_example_ControlArraySglSize;

#endif
