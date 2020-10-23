from datetime import datetime

from rtlsdr import RtlSdr
from pylab import *
from matplotlib import pyplot as plt
from scipy import signal

def main():

    now = datetime.datetime.now()

    current_time = now.strftime("%H:%M:%S.%f")
    print("Current Time =", current_time)
    #aquire location

    #start calibration process (needed?)

    #start syc process

    sdr = RtlSdr()              # rtl-sdr instance
    # configure device
    timeToSample = 1            # in sec
    sampleRate = 2.4e6          # in Mhz
    sdr.sample_rate = sampleRate
    sdr.center_freq = 433e6     # in Mhz
    sdr.gain = 30               # in dB
    print("gain set to:" ,sdr.get_gain())
    print(now)

    numberOfSamples = sampleRate * timeToSample
    fig=figure()
    ax = fig.add_subplot(111, projection='3d')      # used for 3d IQ/time plot
    samples = sdr.read_samples(numberOfSamples)     # aquire samples
    sdr.close()
    # I/Q seperation
    real = samples.real
    imag = samples.imag
    samp = np.arange(0, numberOfSamples, 1) # used as an axis
    #ax.scatter(samp[0:-1:100],real[0:-1:100],imag[0:-1:100],marker='^',s=2)#used for pumba slack

    simulateRecivers(real,sampleRate)      # used to simulation
    #plt.subplot(3, 1, 2)
    # xlabel('Real axis')#used for pumba slack
    # ylabel('img axis')#used for pumba slack
    '''
    pxx,farr=psd(samples, NFFT=1024, Fs=sampleRate / 1e6, Fc=sdr.center_freq / 1e6)
    plt.subplot(2, 1, 1)
    plt.plot(samp, imag)
    plt.subplot(2, 1, 2)
    plt.plot(farr,pxx)
    '''
    show()



#   this function simulates multiple recivers
#   reciver is an ndarray
def simulateRecivers(rawSampled,Fs):
    samp = np.arange(0, len(rawSampled), 1)             # used for axis
    reciver2 = np.roll(rawSampled,5)                    # create a delayed reciver
    reciver3 = np.roll(rawSampled,3)
    discreteDelay12,timeDelay12 = getDelay(rawSampled,reciver2,Fs)
    discreteDelay23,timeDelay23 = getDelay(reciver2, reciver3, Fs)
    discreteDelay31,timeDelay31 = getDelay(reciver3, rawSampled, Fs)
    print(discreteDelay12," ",timeDelay12)
    print(discreteDelay23," ",timeDelay23)
    print(discreteDelay31," ",timeDelay31)

#   gets the delay between two signals
def getDelay(signal1,signal2,Fs):
    corr = signal.correlate(signal1, signal2, 'same')  # cross correlate reciveres
    # subplot(311)
    # axis = np.arange(0, len(rawSampled), 1)
    # plt.plot(axis,signal1)
    # subplot(312)
    # plt.plot(axis,signal2)
    # subplot(313)
    # plt.plot(np.arange(0, len(corr), 1),corr)
    maxpos = np.argmax(corr)                           # postion of max correlation
    discreteDelay = ((len(corr) / 2) - maxpos)         # descrete shift
    timeDelay = discreteDelay * 1 / Fs                 # Time Delay
    return discreteDelay, timeDelay
main()