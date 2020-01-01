#!/usr/bin/env python
# coding: utf-8

# In[2]:


from os import path

if path.exists("data/live_packets"):
    open("data/live_packets","w").write('')

if path.exists("data/xy_coordinates"):
    open("data/xy_coordinates","w").write('')   

if path.exists("data/time_stamps"):
    open("data/time_stamps","w").write('')       

if path.exists("data/psd_15hz_data"):
    open("data/psd_15hz_data","w").write('')     

