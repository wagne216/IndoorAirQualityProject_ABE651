# -*- coding: utf-8 -*-
"""
Updated 4/17/20
~ 7 minutes to completion
Use this to eliminate and track unwanted values from PIAQ data. 
Finds values outside of desired ranges, logs times. 
@author: wagne216
"""

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

# LOAD DATAFRAMES (if necessary) from saved HDF5 files
store1 = pd.HDFStore('store1.h5')
store2 = pd.HDFStore('store2.h5')
store3 = pd.HDFStore('store3.h5')
store4 = pd.HDFStore('store4.h5')

# store1.keys() # to view variable possibilities
# load relevant variables from HDF5 files as arrays (to save space)
n1 = store1['sn1'].to_numpy()
a1 = store1['sa1'].to_numpy()
time1 = store1['stime1'].to_numpy()
n2 = store2['sn2'].to_numpy()
a2 = store2['sa2'].to_numpy()
time2 = store2['stime2'].to_numpy()
n3 = store3['sn3'].to_numpy()
a3 = store3['sA3'].to_numpy()
time3 = store3['stime3'].to_numpy()
n4 = store4['sn4'].to_numpy()
a4 = store4['sa4'].to_numpy()
time4 = store4['stime4'].to_numpy()

# %% Filter data:
# Find indices in each data set where  0>= N > 10^5 and remove
# 1. Negative vals not reasonable; 
# 2. val's higher than 20000 1/cm^3 likely from instrument shutdown
# 3. Where N = 0 exaclty, likely also from instrument warming up
sayandprint('starting filters')

# PIAQ1:
idx_below1 = [idx_sub for idx_sub, val in enumerate(n1) if val < 0]
idx_above1 = [idx_sup for idx_sup, val in enumerate(n1) if val > 2*10**5]
idx_zer1 = [idx_zer for idx_zer, val in enumerate(n1) if val ==0]
n1=np.delete(n1,idx_below1)
n1=np.delete(n1,idx_above1)
n1=np.delete(n1,idx_zer1)
time1=np.delete(time1,idx_below1)
time1=np.delete(time1,idx_above1)
time1=np.delete(time1,idx_zer1)
a1nan = np.argwhere(np.isnan(a1)) # fina A NaN index
timea1 =np.delete(time1,a1nan)

# PIAQ 2:
idx_below2 = [idx_sub for idx_sub, val in enumerate(n2) if val < 0]
idx_above2 = [idx_sup for idx_sup, val in enumerate(n2) if val > 2*10**5]
idx_zer2 = [idx_zer for idx_zer, val in enumerate(n2) if val ==0]
n2=np.delete(n2,idx_below2)
n2=np.delete(n2,idx_above2)
n2=np.delete(n1,idx_zer2)
a2nan = np.argwhere(np.isnan(a2)) # fina A NaN index
time2=np.delete(time2,idx_below2)
time2=np.delete(time2,idx_above2)
time2=np.delete(time2,idx_zer2)
timea2 =np.delete(time2,a2nan)

# PIAQ 3:
idx_below3 = [idx_sub for idx_sub, val in enumerate(n3) if val < 0]
idx_above3 = [idx_sup for idx_sup, val in enumerate(n3) if val > 2*10**5]
idx_zer3 = [idx_zer for idx_zer, val in enumerate(n3) if val ==0]
n3=np.delete(n3,idx_below3)
n3=np.delete(n3,idx_above3)
n3=np.delete(n3,idx_zer3)
idxnan3 = np.array([])
# loop to find NaN indices:
for line in np.arange(1,len(a3)):
    if isinstance(a3[line], str): # returns True if cell is string (would be a "NaN")
        idxnan3 = np.append(idxnan3,line)
time3=np.delete(time3,idx_below3)
time3=np.delete(time3,idx_above3)
time3=np.delete(time3,idx_zer3)
timea3 =np.delete(time3,idxnan3)
a3 =np.delete(a3,idxnan3)

# PIAQ4:
idx_below4 = [idx_sub for idx_sub, val in enumerate(n4) if val < 0]
idx_above4 = [idx_sup for idx_sup, val in enumerate(n4) if val > 2*10**5]
idx_zer4 = [idx_zer for idx_zer, val in enumerate(n4) if val ==0]
n4=np.delete(n4,idx_below4)
n4=np.delete(n4,idx_above4)
n4=np.delete(n4,idx_zer4)
idxnan4 = np.array([])
# loop to find NaN indices:
for line in np.arange(1,len(a4)):
    if isinstance(a4[line], str): # returns True if cell is string (would be a "NaN")
        idxnan4 = np.append(idxnan4,line)
time4=np.delete(time4,idx_below4)
time4=np.delete(time4,idx_above4)
time4=np.delete(time4,idx_zer4)
timea4 =np.delete(time4,idxnan4)
a4 =np.delete(a4,idxnan4)

sayandprint('filters applied')
 # %%
        
        
    
