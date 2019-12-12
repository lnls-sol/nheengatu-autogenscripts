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
static const char* const NiFpga_bool_test_Signature = "8A3C267413974588DD800384CC102CEC";

typedef enum
{
   NiFpga_bool_test_IndicatorBool_BI_led0 = 0x18006,
   NiFpga_bool_test_IndicatorBool_BI_led1 = 0x1800A,
   NiFpga_bool_test_IndicatorBool_BI_led2 = 0x18016,
   NiFpga_bool_test_IndicatorBool_BI_led3 = 0x1801A,
} NiFpga_bool_test_IndicatorBool;

typedef enum
{
   NiFpga_bool_test_IndicatorU64_BI_VECTOR = 0x18020,
} NiFpga_bool_test_IndicatorU64;

typedef enum
{
   NiFpga_bool_test_ControlBool_BO0 = 0x18002,
   NiFpga_bool_test_ControlBool_BO1 = 0x1800E,
   NiFpga_bool_test_ControlBool_BO2 = 0x18012,
   NiFpga_bool_test_ControlBool_BO3 = 0x1801E,
} NiFpga_bool_test_ControlBool;

#endif
