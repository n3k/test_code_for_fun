#########
IADD = 1
ISUB = 2
IMUL = 3
ILT = 4
IEQ = 5
BR = 6
BRT = 7
BRF = 8
ICONST = 9
LOAD = 10
GLOAD = 11
STORE = 12
GSTORE = 13
PRINT = 14
POP = 15
HALT = 16
CALL = 17
RET = 18
##########

######### ACTIVATION RECORD LAYOUT ###########
"""
    sp -> local_2 +2
          local_1 +1
    fp -> ret      +0
          fp      -1
          numArgs -2
          arg0    -3
          arg1    -4
          arg2    -5
          .
"""
#######

LOCAL_0 = 1
LOCAL_1 = 2
LOCAL_2 = 3
LOCAL_3 = 4
LOCAL_4 = 5
LOCAL_5 = 6

ARG_0 = -3
ARG_1 = -4
ARG_2 = -5
ARG_3 = -6
ARG_4 = -7
ARG_5 = -8
ARG_6 = -9
ARG_7 = -10
ARG_8 = -11
ARG_9 = -12


class Instruction:

    def __init__(self, name, nargs=0):
        self.name = name
        self.nargs = nargs


opcodes = [
    Instruction("DUMMY"),
    Instruction("IADD"),
    Instruction("ISUB"),
    Instruction("IMUL"),
    Instruction("ILT"),
    Instruction("IEQ"),
    Instruction("BR", 1),
    Instruction("BRT", 1),
    Instruction("BRF", 1),
    Instruction("ICONST", 1),
    Instruction("LOAD", 1),
    Instruction("GLOAD", 1),
    Instruction("STORE", 1),
    Instruction("GSTORE", 1),
    Instruction("PRINT"),
    Instruction("POP"),
    Instruction("HALT"),
    Instruction("CALL", 2),
    Instruction("RET"),
]
