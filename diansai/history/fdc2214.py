import ctypes
import os

_file = 'fdc2214.so'
_path = os.path.join(*(os.path.split(__file__)[:-1]+(_file,)))
_mode = ctypes.cdll.LoadLibrary(_path)

# void FDC2214_init()
FDC2214_init = _mode.FDC2214
FDC2214_init.restype = None

# uint32_t FDC2214_readCh0(void)
FDC2214_readCh0 = _mode.FDC2214_readCh0
FDC2214_readCh0.restype = ctypes.c_uint32

# FDC2214_sleep()
FDC2214_sleep = _mode.FDC2214_sleep
FDC2214_sleep.restype = None

# FDC2214__configINTB()
FDC2214__configINTB = _mode.FDC2214__configINTB
FDC2214__configINTB.restype = None

# FDC2214__clockSetup()
FDC2214__clockSetup = _mode.FDC2214_clockSetup
FDC2214__clockSetup.restype = None

# FDC2214_allChannelsEnable()
FDC2214_allChannelsEnable = _mode.FDC2214_allChannelsEnable
FDC2214_allChannelsEnable.restype = None

# FDC2214_wake()
FDC2214_wake = _mode.FDC2214_wake
FDC2214_wake.restype = None
