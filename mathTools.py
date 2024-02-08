
import math


def mintosec(timestr):
    m = int(timestr[0:2]) * 60
    s = int(timestr[3:5])
    h = int(timestr[6:]) * 0.01

    return m + s + h

def sectomin(f):
    m = f // 60
    s = f - m * 60 // 1
    h = (f - math.floor(f)) *100


    ms = "%02.0f" % m
    ss = "%02.0f" % s
    hs = "%02.0f" % h

    return ms + ":" + ss + "." + hs


