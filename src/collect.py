#!/usr/bin/env python
# coding: utf-8

# In[129]:


import time
from muse2 import Muse
import csv
import os, os.path
import muse_MACs
import multiprocessing
import config_data



def write_data(x, y):
    '''
    This function appends data packets (12 mV points per packet) from the muse to 'data/live_packets'
    '''

    name_time='data/live_packets'
    tim = str(time.time())
    fields = [[tim+"|"+str(x[4])],'']
    
    with open(r'{}'.format(name_time), 'a') as f:
        writer = csv.writer(f)
        writer.writerow(fields)
        
myMuse = Muse(callback=write_data,address=muse_MACs.myaddress,iface=0)
myMuse.runListener()

