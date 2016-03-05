import sys,os

class Sys_paths:
	SEP = os.path.sep
	PROJ_BASE_DIR = sys.path[0] + SEP + ".."
	YML_DIR = PROJ_BASE_DIR + SEP + "etc"
	DATA_DIR = PROJ_BASE_DIR + SEP + "data"
	LOG_DIR = PROJ_BASE_DIR + SEP + "log"
	LIB_DIR = PROJ_BASE_DIR + SEP + "lib"
	BIN_DIR = PROJ_BASE_DIR + SEP + "bin"