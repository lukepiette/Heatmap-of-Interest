import numpy as np
import scipy.stats
import sys

def calculatePSD(array,sample_f):
    ps = np.abs(np.fft.fft(array))**2

    time_step = 1 / sample_f 
    freqs = np.fft.fftfreq(array.size, time_step)
    idx = np.argsort(freqs)

    return freqs[idx], ps[idx], idx


def getstats15hz(array, sample_f=256):
        
    freq,psd,idx=calculatePSD(array, sample_f=sample_f);
    psd=psd[freq>14];
    freq=freq[freq>14];
    psd = psd[freq<50]
    freq = freq[freq<50]    
    avg=np.average(psd);
    
    id1=np.where(freq>14.9);
    id2=np.where(freq>15.1);
    psdband=psd[id1[0][0]:id2[0][0]];
    peak15=np.max(psdband)
    
    id1=np.where(freq>29.9);
    id2=np.where(freq>30.1);
    psdband=psd[id1[0][0]:id2[0][0]];
    peak30=np.max(psdband)
    
    peaksum = peak15 + peak30
    divide = peaksum/avg

    return divide
        

