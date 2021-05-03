class zeroFunc():
    def __init__(self):
        self.zeroDone = False
        self.startZero = False

def formatMsg(dialRead):
    outMsg = "no"

    try:
        one = int(dialRead[6])
        tenth = int(dialRead[8])
        hundredth = int(dialRead[9])
        thousandth = int(dialRead[10])

        if (one == 2):
            if (tenth+hundredth+thousandth == 0):
                outMsg = "stp"
            else:
                outMsg = "s0+"
        else:
            if (one == 1):
                if (tenth > 7):

                    outMsg="s2-"
                else:
                    outMsg = "s1-"
            else:
                outMsg = "m0-"
        return outMsg
    except:
        return "no"