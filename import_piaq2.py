# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 12:32:54 2020

Import all PIAQ2 files. Everything is based off of the PIAQ1 process. 
Files missing- need to 1. Go back to PIAQ 2 and try to see if I can purge and 
    2. Check the Dell from the lab to see if any were uploaded
@author: D
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
p2files = os.listdir(r"..\Data\PIAQ 2 - Outdoor air")

# 1. IMPORT DATAS

# %% PIAQ 2- should have similar formats as PIAQ 1 because download format same (from USB)
# PIAQ 2 likely running different softwares and may be diff var's

# initialize each data array (keep same var's as heading):
p2_time = []
p2_sootA = []
p2_sootM = []
p2_sootN = []
p2_Temp = []
p2_Hum = []
p2_CO2 = []
p2_CMD = []

# cycle through each file and save data as proper var based on column headers (defined manually)

for file_no in range(np.size(p2files)):
#file_no = 65 # for troubleshooting
    # define data filepath relative to this script
    filepath = "..\Data\PIAQ 2 - Outdoor air\\"+p2files[file_no]
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
        data = pd.read_table(filepath,header =2,index_col=False,skiprows=-1) # names not prespecified in case they change in diff files
        # fix the time column into a time stamp
        fixtime = data['time'].str.replace("T"," ") # remove T from date
        fixtime = pd.to_datetime(fixtime[:-1]) # convert time string to time stamp
        # add time back in to data
        data['time'] = fixtime
        data = data[:-1] # remove last line
        
    
    # concatenate lists by OLD_LIST+NEW_LIST (converted from dataframe)
    p2_time = p2_time + pd.Series.to_list(data['time'])
    p2_sootA = p2_sootA + pd.Series.to_list(data['sootA'])
#    p2_sootM = p2_sootM + pd.Series.to_list(data['sootM'])
    p2_sootN = p2_sootN + pd.Series.to_list(data['sootN'])
    p2_Temp = p2_Temp + pd.Series.to_list(data['Temp'])
    p2_Hum = p2_Hum + pd.Series.to_list(data['Hum'])
    p2_CO2 = p2_CO2 + pd.Series.to_list(data['CO2'])
    p2_CMD = p2_CMD + pd.Series.to_list(data['CMD'])

    
    
#visual and audio notification when import is finished so i don't have to wait: 
sayandprint("PIAQ 2 variables saved")

# %% convert separate lists back into 1 data frame

p2_df = pd.DataFrame({'time':p2_time,'A':p2_sootA,\
                      'N':p2_sootN,'T':p2_Temp,'H':p2_Hum,\
                      'CO2':p2_CO2,'CMD':p2_CMD})


#%% make rows unique then reorder
p2_df = p2_df.drop_duplicates(keep='first')
p2_df = p2_df.sort_values('time',axis=0,ascending=True,na_position='last')
# does sample length make sense?
no_sec = 60*24*3600 # for sample length of about 300 days (Feb- Dec)

# %% HDF5store because the file is so large - only if needed to avoid running this script again
sayandprint("PIAQ 2 variables saving")

# does sample length make sense?
time2 = p2_df['time']
a2 = p2_df['A']
#m2 = p2_df['M'] # didn't include in dataframe matrix
n2 = p2_df['N']
h2 = p2_df['H']
T2 = p2_df['T']
co22 = p2_df['CO2']
cmd2 = p2_df['CMD']

# create storage file 2
store2 = pd.HDFStore('store2.h5')

#store the vars ( missing = __)
store2['stime2'] =time2
#store2['sm2'] = m2
store2['sn2'] = n2
store2['sh2'] = h2
store2['sco22'] = co22
store2['sT2'] = T2
store2['sa2'] = a2
store2['scmd2'] = cmd2

# check access by reloding a variable
c2= store2['sn2']

sayandprint("PIAQ 2 variables saved")
