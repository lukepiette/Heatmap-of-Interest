#!/usr/bin/env python
# coding: utf-8

# In[155]:


import assemble_exodia
import time
import cv2

full = open('data/live_packets','r').read()
tmp_data = assemble_exodia.clean_data(full)
assemble_exodia.get_stats_15hz(tmp_data)


def get_data():
    '''
    Parses data from 'data/psd_15hz_data'
    '''
    full = open('data/psd_15hz_data','r').read()
    full = full.replace('[','')
    full = full.replace(']','')
    elec_full = full.replace(',','').split(' ')
    return(elec_full)

def get_time():
    '''
    Parses data from 'data/time_stamps'
    '''
    full = open('data/time_stamps','r').read()
    full = full.replace('[','')
    full = full.replace(']','')
    full = full.replace(' ','')
    full = full.replace("'",'')
    data = full.split(',')
    for i in range(len(data)):
        data[i] = data[i].split('.')[0]
    return(data[20*10:])

def assembler(x,y):
    x = x[0:len(y)]
    out = []
    for i in range(len(x)):
        out += [[x[i],y[i]]]
 
    return(out)

def parse_coordinates():
    '''
    Parses data from 'data/xy_coordinates'
    '''
    data_coor = open('data/xy_coordinates','r').read().replace('(','').split(')')
    out = []
    for i in data_coor:
        try:
            dd = i.replace(' ','').split(',')
            jj = dd[0].split('.')[0]
            out += [[jj,dd[1],dd[2]]]
        except:
            pass
    return(out)


def track_dat(tcc,dis2):
    liser = [0 for i in range(dis2)]
    bij = tcc[0][0]
    track = 0
    cot = 0

    for i in tcc:
        jj = i[0]
        if bij == jj:
            cot += 1
        else:
            liser[track] = cot
            cot = 0
            track += 1
            bij = jj

    ff = []
    for i in liser:
        if i != 0:
            ff += [i]	

    return(ff)


def assemble_all():
    x = get_time()
    y = get_data()

    ass = assembler(x,y)
    tcc = parse_coordinates()

    dico = int(tcc[0][0])-int(ass[0][0])+10
    endo = int(ass[-1][0])-int(tcc[-1][0])

    if dico < 0:
        print("The distance between collection and start of pygame window were too large. \nPlease restart.")
        return

    dis1 = -int(ass[0][0])+int(ass[-1][0])+10
    dis2 = -int(tcc[0][0])+int(tcc[-1][0])

    print('start time dif:',dico,'| end time dif:',endo,'\n')
    print('Sec total: ',dis1)
    print('Sec run: ',dis2)

    liser_ass = track_dat(ass,dis2)[1:-endo-1]
    liser_tcc = track_dat(tcc,dis2)[11-dico:-1]

    tcc_new = []
    ass_new = []
    c_tcc = 0
    c_ass = 0 
    
    print(len(liser_ass),len(liser_tcc))

    for i in range(len(liser_tcc)):
        num = liser_tcc[i] // liser_ass[i]
        num2 = liser_tcc[i]-(liser_ass[i]*num)
        
        for w in ass[c_ass:c_ass+liser_ass[i]]:
            ass_new += num*[w]

        if num2 > 0:
            ass_new += num2*[ass[c_ass+liser_ass[i]]]
        tcc_new += tcc[c_tcc:c_tcc+liser_tcc[i]]
        c_tcc += liser_tcc[i]
        c_ass += liser_ass[i]

    print(len(ass_new),len(tcc_new))
    outed = []
    for i in range(len(ass_new)):
        outed += [[tcc_new[i][0],ass_new[i][1],tcc_new[i][1],tcc_new[i][2]]]

    return(outed)
    

def heat_map():
    '''
    For each SSVEP point, map that value to 'null.jpg' to create a heatmap of interest
    '''

    jj = cv2.imread('null.jpg')
    data = assemble_all()
    
    for i in range(len(data)):
        sd = 0
        if float(data[i][1]) < 80: 
            pix = float(data[i][1])//2
            sd = 1
        else:
            pix = float(data[i][1])**3

        if pix > 255:
            pix = 255
        
        x_cor = int(float(data[i][2]))
        y_cor = int(float(data[i][3]))

        try:
            jj[y_cor][x_cor][0] = 0
            jj[y_cor][x_cor][1] = 0
            jj[y_cor][x_cor][2] = 0
            if sd == 0:
                jj[y_cor][x_cor][2] = int(pix)
            else:
                jj[y_cor][x_cor][0] = int(pix)
        except:
            if x_cor > 1800:
                x_cor = 1800
            elif x_cor < 0:
                x_cor = 0

            if y_cor > 1000:
                y_cor = 1000
            elif y_cor < 0:
                y_cor = 0
        
    cv2.imwrite('data/result.jpg', jj)
    

heat_map()
import oneD_array

