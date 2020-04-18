# -*- coding: utf-8 -*-
"""
Updated 4/17/20

Once the data from each pegasor is imported, this file can be run in order to 
generate several plots to visualized the N concentrations. Each variable can be plotted
by changing 'n' variable to that desired. 
@author: wagne216
"""
# change to pycode directory

import numpy as np
import pandas as pd
import os, os.path
import matplotlib.pyplot as m
import time
import win32com.client as wincl
import time
from matplotlib import gridspec
import seaborn as sns # for the KDE plot

# change to folder where code is stored:
os.chdir(r'C:\Users\D\OneDrive - purdue.edu\ABE\PIAQ Analysis\PyCode')
# create function that tells you when tasks are done (audio + visual)
def sayandprint(string):
    speak = wincl.Dispatch("SAPI.SpVoice")
    speak.Speak(string)
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print(string +" "+ current_time)

## LOAD DATAFRAMES (if necessary) from saved HDF5 files
#store1 = pd.HDFStore('store1.h5')
#store2 = pd.HDFStore('store2.h5')
#store3 = pd.HDFStore('store3.h5')
#store4 = pd.HDFStore('store4.h5')
#
## store1.keys() # to view variable possibilities
## load relevant variables from HDF5 files as arrays (to save space)
#n1 = store1['sn1'].to_numpy()
#a1 = store1['sa1'].to_numpy()
#time1 = store1['stime1'].to_numpy()
#n2 = store2['sn2'].to_numpy()
#a2 = store2['sa2'].to_numpy()
#time2 = store2['stime2'].to_numpy()
#n3 = store3['sn3'].to_numpy()
#a3 = store3['sA3'].to_numpy()
#time3 = store3['stime3'].to_numpy()
#n4 = store4['sn4'].to_numpy()
#a4 = store4['sa4'].to_numpy()
#time4 = store4['stime4'].to_numpy()

# %% TIME-SERIES- check for data gaps and obvious wrong things that may need manually corrected
fgr = m.figure(figsize =(11,8)) 
fgr.add_axes()
fgr.suptitle('PIAQ Number Concentration Time Series Plots')

# %
# PIAQ 1
ax1 = fgr.add_subplot(221)
ax1 = m.plot(time1b,n1b,color='red')
m.title('a.) PIAQ 1')
m.ylabel('N ($cm^{-3}$)')
m.xlabel('Time')

# PIAQ 2
ax2 = fgr.add_subplot(222)
ax2 = m.plot(time2,n2,color='orange')
m.title('b.) PIAQ 2')
m.ylabel('N ($cm^{-3}$)')
m.xlabel('Time')

# PIAQ 3
ax3 = fgr.add_subplot(223)
ax3 = m.plot(time3,n3,color='green')
m.title('c.) PIAQ 3')
m.ylabel('N ($cm^{-3}$)')
m.xlabel('Time')

# PIAQ 4
ax4 = fgr.add_subplot(224)
ax4 = m.plot(time4,n4,color='blue')
m.title('d.) PIAQ 4')
m.ylabel('N ($cm^{-3}$)')
m.xlabel('Time')

fgr.subplots_adjust(wspace=0.4,hspace=0.3,left=0.125,right=0.9,top=0.9,bottom=0.1)

m.show()

# %% BOXPLOTS: 
# without outliers

fgr = m.figure(figsize =(11,8)) 

# 1
ax1 = fgr.add_subplot(141)
ax1=m.boxplot(n1,0,'')
m.title('PIAQ 1: Office Air')
m.ylabel('N ($cm^{-3}$)')

# 2
ax2 = fgr.add_subplot(142)
ax2=m.boxplot(n2,1,'')
m.title('PIAQ 2: Outdoor Air')

# 3
ax3 = fgr.add_subplot(143)
ax3=m.boxplot(n3,1,'')
m.title('PIAQ 3: Supply Air')

# 4
ax4 = fgr.add_subplot(144)
ax4=m.boxplot(n4,1,'')
m.title('PIAQ 4: Pre-filter Supply')
fgr.subplots_adjust(wspace=0.4,hspace=0.3,left=0.125,right=0.9,top=0.9,bottom=0.1)

m.show()
# %% with outliers

fgr = m.figure(figsize =(11,8)) 

# 1
ax1 = fgr.add_subplot(141)
ax1=m.boxplot(n1)
m.title('PIAQ 1: Office Air')
m.ylabel('N ($cm^{-3}$)')

# 2
ax2 = fgr.add_subplot(142)
ax2=m.boxplot(n2)
m.title('PIAQ 2: Outdoor Air')

# 3
ax3 = fgr.add_subplot(143)
ax3=m.boxplot(n3)
m.title('PIAQ 3: Supply Air')

# 4
ax4 = fgr.add_subplot(144)
ax4=m.boxplot(n4)
m.title('PIAQ 4: Pre-filter Supply')
fgr.subplots_adjust(wspace=0.4,hspace=0.3,left=0.125,right=0.9,top=0.9,bottom=0.1)
m.show()
# %% NORMALZIED CDFS

fgr = m.figure(figsize =(11,8)) 
fgr.suptitle('Number Concentration Normalized CDFs')

# PIAQ 1
ax1 = fgr.add_subplot(221)
cs1 = np.cumsum(n1)
ax1 = m.plot(cs1/cs1[-1],color='red')
m.title('a.) PIAQ 1: Office Air')
m.ylabel('CDF')
m.xlabel('N ($cm^{-3}$)')

# PIAQ 2
ax2 = fgr.add_subplot(222)
cs2 = np.cumsum(n2)
ax2 = m.plot(cs2/cs2[-1],color='orange')
m.title('b.) PIAQ 2: Outdoor Air')
m.ylabel('CDF')
m.xlabel('N ($cm^{-3}$)')

# PIAQ 3
ax3 = fgr.add_subplot(223)
cs3 = np.cumsum(n3)
ax3 = m.plot(cs3/cs3[-1],color='green')
m.title('c.) PIAQ 3: Supply Air')
m.ylabel('CDF')
m.xlabel('N ($cm^{-3}$)')

# PIAQ 4
ax4 = fgr.add_subplot(224)
cs4 = np.cumsum(n4)
ax4 = m.plot(cs4/cs4[-1],color='blue')
m.title('d. PIAQ 4: Pre-filter Supply')
m.ylabel('CDF')
m.xlabel('N ($cm^{-3}$)')

fgr.subplots_adjust(wspace=0.4,hspace=0.3,left=0.125,right=0.9,top=0.9,bottom=0.1)

m.show()

# %% KDE PLOTS- look at distributions for each dataset
fgr = m.figure(figsize =(11,8)) 
fgr.add_axes()
fgr.suptitle('Kernel Density Estimates')

# PIAQ 1
ax1 = fgr.add_subplot(221)
ax1 = sns.distplot(n1, kde = True, hist=False, rug=False,color='red')
m.ylabel('Density')
m.xlabel('N ($cm^{-3}$)')
m.title('a.) PIAQ 1: Office Air')

# PIAQ 2
ax2 = fgr.add_subplot(222)
ax2 = sns.distplot(n2, kde = True, hist=False, rug=False,color='orange')
m.ylabel('Density')
m.xlabel('N ($cm^{-3}$)')
m.title('b.) PIAQ 2: Outdoor Air')

# PIAQ 3
ax3 = fgr.add_subplot(223)
ax3 = sns.distplot(n3, kde = True, hist=False, rug=False,color='green')
m.ylabel('Density')
m.xlabel('N ($cm^{-3}$)')
m.title('c.) PIAQ 3: Supply Air')

# PIAQ 4
ax4 = fgr.add_subplot(224)
ax4 = sns.distplot(n4, kde = True, hist=False, rug=False,color='blue')
m.ylabel('Density')
m.xlabel('N ($cm^{-3}$)')
m.title('d. PIAQ 4: Pre-filter Supply')

fgr.subplots_adjust(wspace=0.4,hspace=0.4,left=0.125,right=0.9,top=0.8,bottom=0.1)

m.show()

