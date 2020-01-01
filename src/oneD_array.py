#!/usr/bin/env python
# coding: utf-8

# In[100]:


import numpy as np
import cv2


def D2_to_D1():
    '''
    This function parses the 3D 'data/result.jpg' image and squishes it down to a 1D sequence of integers for the plotter.
    The plotter LED colors are either blue or red on a gradient scale from 1 (blue) - 250 (red).
    Where the subject looked but didn't get a large response, the LED turns blue. Where they did get a high response, the LED tirns red.
    '''

    data = cv2.imread('data/result.jpg')
    total = []
    
    for i in data:
        tmp = []
        cc = 1

        for o in i:
            if sum(o) > 400:
                tmp += [0]
            else:
                if o[1] == 0:
                    if o[0] > 0:
                        tmp += [o[0]]
                        cc += 1
                    elif o[2] > 0:
                        j = 100+o[2]
                        if j > 250:
                            j = 250
                        
                        tmp += [j,j]
                        cc += 1

        hh = sum(tmp)//cc
        if hh > 250:
            hh = 250
        total += [hh]
        
    tt = np.array(total)
    np.save('data/RGB_data', tt)

D2_to_D1()

