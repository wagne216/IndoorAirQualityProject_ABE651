# -*- coding: utf-8 -*-
"""
Updated: 4-4-20

Run this script to 
1. import PIAQ 1 data 
     - check that data is in right PIAQ # category based on # in data sheet
2. eliminate irrelevant data
3. save as HDF5 under variable 'store.py'

"""

# modules:
import numpy as np
import pandas as pd
import os, os.path
import time
import win32com.client as wincl

# change to pycode directory
os.chdir(r'C:\Users\D\OneDrive - purdue.edu\ABE\PIAQ Analysis\PyCode')

# create function that tells you when tasks are done (audio + visual)
def sayandprint(string):
    speak = wincl.Dispatch("SAPI.SpVoice")
    speak.Speak(string)
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print(string +" "+ current_time)

# define data locations relative to path of this script: 
p1files = os.listdir(r"..\Data\PIAQ 1 - LL2")

# 1. IMPORT DATAS

# %% PIAQ 1
sayandprint("Importing PIAQ 1 variables")

# initialize each data array (keep same var's as heading):
p1_time = []
p1_sootA = []
p1_sootLDSA = []
#p1_sootM = []
p1_sootN = []
p1_Temp = []
p1_Hum = []
p1_CO2 = []
#p1_BaromP = []

# cycle through each file and save data as proper var based on column headers (defined manually)

for file_no in range(np.size(p1files)):
#for file_no in range(3):
    # define data filepath relative to this script
    filepath = "..\Data\PIAQ 1 - LL2\\"+p1files[file_no]
    # must first see which filetype in order to properly treat it 
    firstcheck = pd.read_table(filepath,header=2)
    col_size = np.size(firstcheck.columns)
    data = [] # clear each time so there's no accidental adding of previous datas
    
    if col_size == 1: # becaues it's a continuous string due to '\t' delim
        # TREAT AS ABNORMAL 
        data = pd.read_csv(filepath, sep = r'\t', header = 2,index_col=False, lineterminator = "")
        # fix the time column into a time stamp
        fixtime = data['"time'].str.replace("T"," ") # remove T from date
        fixtime = fixtime.str.strip('"') # remove extra quptes
        fixtime = pd.to_datetime(fixtime[:-1]) # convert time string to time stamp
        # add time back in to data
        data['time']= fixtime
        data = data[:-1] # remove last line
        data = data.rename(columns={'Barom.P",':'Barom.P'})
    else: # col_size ~ 9, but is not 1
        # TREAT AS NORMAL 
    #    data = pd.read_table(filepath,header =2,index_col=False,names=["time","sootA","sootLDSA","sootM","sootN","Temp","Hum","CO2","Barom.P"],skiprows=-1)
        data = pd.read_table(filepath,header =2,index_col=False,skiprows=-1) # names not prespecified in case they change in diff files
        # fix the time column into a time stamp
        fixtime = data['time'].str.replace("T"," ") # remove T from date
        fixtime = pd.to_datetime(fixtime[:-1]) # convert time string to time stamp
        # add time back in to data
        data['time'] = fixtime
        data = data[:-1] # remove last line
        
    
    # concatenate lists by OLD_LIST+NEW_LIST (converted from dataframe)
    p1_time = p1_time + pd.Series.to_list(data['time'])
    p1_sootA = p1_sootA + pd.Series.to_list(data['sootA'])
    p1_sootLDSA = p1_sootLDSA + pd.Series.to_list(data['sootLDSA'])
#    p1_sootM = p1_sootM + pd.Series.to_list(data['sootM'])
    p1_sootN = p1_sootN + pd.Series.to_list(data['sootN'])
    p1_Temp = p1_Temp + pd.Series.to_list(data['Temp'])
    p1_Hum = p1_Hum + pd.Series.to_list(data['Hum'])
    p1_CO2 = p1_CO2 + pd.Series.to_list(data['CO2'])
#    p1_BaromP = p1_BaromP+ pd.Series.to_list(data['Barom.P'])

    
    
#visual and audio notification when import is finished so i don't have to wait: 
sayandprint("PIAQ 1 variables saved")

# %% convert separate lists back into 1 data frame

p1_df = pd.DataFrame({'time':p1_time,'A':p1_sootA,'LDSA':p1_sootLDSA,\
                      'N':p1_sootN,'T':p1_Temp,'H':p1_Hum,\
                      'CO2':p1_CO2})

#%% make rows unique then reorder
p1_df = p1_df.drop_duplicates(keep='first')
p1_df = p1_df.sort_values('time',axis=0,ascending=True,na_position='last')
# does sample length make sense?
no_sec = 60*14*3600 # for sample length of about 300 days (Feb- Dec)

# %% HDF5store because the file is so large - only if needed to avoid running this script again
sayandprint("PIAQ 1 variables saving")

# does sample length make sense?
time1 = p1_df['time']
a1 = p1_df['A']
ldsa1 = p1_df['LDSA']
#m1 = p1_df['M'] # didn't include in dataframe matrix
n1 = p1_df['N']
h1 = p1_df['H']
T1 = p1_df['T']
co21 = p1_df['CO2']

# create storage file 1
store1 = pd.HDFStore('store1.h5')

#store the vars ( missing = __)
store1['stime1'] =time1
#store1['sm1'] = m1
store1['sn1'] = n1
store1['sh1'] = h1
store1['sco21'] = co21
store1['sT1'] = T1
store1['sa1'] = a1
store1['sldsa1'] = ldsa1

# check access by reloding a variable
c1= store1['sn1']

sayandprint("PIAQ 1 variables saved")

# %% check data
# use list comprehension to get values outside of acceptable range:
idx_below = [idx_sub for idx_sub, val in enumerate(n1) if val < 0]
idx_above = [idx_sup for idx_sup, val in enumerate(n1) if val > 10**5]
