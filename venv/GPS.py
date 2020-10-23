from rtlsdr import RtlSdr
from pylab import *
from matplotlib import pyplot as plt
from scipy import signal
import gps
reload(GPS)

class GPSclass():
    def __init__(self):
        sdr = RtlSdr()
        CA = np.loadtxt('CA.txt', dtype=np.int16, unpack=True)
        


































