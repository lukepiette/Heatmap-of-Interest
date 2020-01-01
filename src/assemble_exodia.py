#!/usr/bin/env python
# coding: utf-8

# In[212]:


import psdthresh
import numpy as np

def clean_data(full):
    '''
    Parses the text file that contains data from the Muse
    '''

    elec_full = [[],[]]
    all_stuff = full.split(",")
    for i in all_stuff:
        try:
            jj = i.replace('\\n', '')
            jj = jj.replace('[', '')
            jj = jj.replace(']', '')
            jj = jj.replace("'", '')

            aa = jj.split('|')
            elec_full[0] += [aa[0][1:]]
            kk = aa[1].split(' ')
            tt = []
            for i in kk:
                if len(i) > 0:
                    tt += [i]
            elec_full[1] += tt
        except:
            pass
    
   
    open('data/time_stamps','w').write(str(elec_full[0][1:]))
    return(elec_full[1][1:])


def get_stats_15hz(data):
    '''
    Applies a fourier tranform to data in a 10 sec sliding window, then appends to 'data/psd_15hz_data'
    '''

    sec_10 = int(20*10*12)
    out_psd = []    
    
    if len(data) > sec_10:
        for i in range(int((len(data)-sec_10)/12)):
            jj = psdthresh.getstats15hz(np.array(data[12*i:sec_10+(i+1)*12]))
            out_psd += [jj]
            print(jj)

    open('data/psd_15hz_data','w').write(str(out_psd))
    print("\n15Hz data writen to 'data/psd_15hz_data'\n\n")

