# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 03:00:15 2020

Use to import PIAQ files. Will like have to divide the data into chunks when importing and saving,
beacuse each file is way too large. Avoid this by saving smaller files in the future;
when using PPS plotter, restart data logging with each save. 

@author: D
"""

# use this to figure out the .txt. import thing# modules:
import numpy as np
import pandas as pd
import os, os.path
import time
import win32com.client as wincl
from datetime import datetime

# change to pycode directory
os.chdir(r'C:\Users\D\OneDrive - purdue.edu\ABE\PIAQ Analysis\PyCode')

# create function that tells you when tasks are done (audio + visual)
def sayandprint(string):
    speak = wincl.Dispatch("SAPI.SpVoice")
    speak.Speak(string)
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print(string +" "+ current_time)

# define data location relative to path of this script: 
p3files = os.listdir(r"..\Data\PIAQ 3 - After supply fan")

# %% start here when restarting data 

#$ initialize the final lists that data from each file will be concatenated to: 
p3_time = []
p3_N = []
p3_A = []
p3_M = []
p3_CMD = []
p3_H = [] 
p3_T = []
p3_CO2 = []

# IMPORT 
sayandprint("Importing PIAQ 3 variables")

#for file in np.arange(86,97):
for file in np.arange(97,np.size(p3files)):
    
    filepath = "..\Data\PIAQ 3 - After supply fan\\"+p3files[file]
    frac = open(filepath, 'r') # raccoon file
    # read file and save all data as 1 var
    fullset = frac.readlines() # 
    # close file 
    frac.close()
    # create list of 0's equal to file width; initializes variable to be faster
    Data = [0]*len(fullset)

    # split data for first row as strings, based on commas
    for header_labels in range(10):       
        header = fullset[0].split('\t') # and divides list into sep header titles
        header = header[:-1] # remove 'comments' column
        if 'Piaq122_Flow1 [l/min]' in header: # these cause issues
            header.remove('Piaq122_Flow1 [l/min]')
        if 'Piaq122_Flow2 [l/min]' in header:
            header.remove('Piaq122_Flow2 [l/min]')
            
        # for each file: 
        df = pd.DataFrame([],index=None)
        
        # reset empty columns
        c0 = []
        c1 = []
        c2 = []
        c3 = []
        c4 = []
        c5 = []
        c6 = []
        c7 = []
        c8 = []
        
        sh = np.size(header) # will determine how many columns
        
        # CREATE UNNAMED LISTS - to account for diff files with diff downloaded datas and order
            # because working with floats this time instead of series, must append in loops
        for line in range(1,len(fullset)-1): # goes through each line
            Data[line] = fullset[line].strip().split('\t') # and divides into list row by row
#            Data[line][1:8] = fullset[line][1:8].strip("'") # and divides into list row by row
            if r'' in Data[line]: # data is missing some pieces and woudl complicate import even more, then ignore
                break # break this particular for loop
            if np.size(Data[line]) < np.size(header): # if line has less than full data
                line = line+1 # go to next line
                Data[line] = fullset[line].strip().split('\t') # and divides into list row by row

            if np.size(Data[line]) - np.size(header)==0: # carry on with business as usual
                # time (always first) reported in no. seconds past 1/1/1970:
                c0.append(datetime.timestamp(datetime.strptime(Data[line][0], '%Y-%m-%d %H:%M:%S.%f')) ) # datetime then timestamp
                # CREATE UNNAMED LISTS based on columns - to account for diff files with diff downloaded datas and order
                if sh > 1: # (then at least a 2nd col, etc.)
                    c1.append(float(Data[line][1])) # floating point field
                if sh > 2:
                    c2.append(float(Data[line][2])) # floating point field
                if sh > 3:
                    c3.append(float(Data[line][3])) # floating point field
                if sh > 4:
                    c4.append(float(Data[line][4])) # floating point field
                if sh > 5:
                    c5.append(float(Data[line][5])) # floating point field
                if sh > 6:
                    c6.append(float(Data[line][6])) # floating point field
                if sh > 7:
                    c7.append(float(Data[line][7])) # floating point field
                if sh > 8:
                    c8.append(float(Data[line][8])) # floating point field
        
        # CREATE NAMED DATAFRAME SERIES- based on named column headers
        df[header[0]] = c0
        if sh > 1:
            df[header[1]] = c1
        if sh > 2:
            df[header[2]] = c2
        if sh > 3:
            df[header[3]] = c3
        if sh > 4:
            df[header[4]] = c4
        if sh > 5:
            df[header[5]] = c5
        if sh > 6:
            df[header[6]] = c6
        if sh > 7:
            df[header[7]] = c7
        if sh > 8:
            df[header[8]] = c8
        
        # APPEND NAMED DATA FROM DATAFRAMES INTO P3 LISTS (Nan if doesn't exist to preserve time-data links)
        # always a time column:    
        p3_time = p3_time + df['time'].to_list() 
        if r'Piaq122_N [x1000/cm3]' in df:
            p3_N = p3_N + df['Piaq122_N [x1000/cm3]'].to_list() 
        else:
            p3_N = p3_N +  ['NaN'] * len(c0) 
        if r'Piaq122_A [um2/cm3]' in df:
            p3_A = p3_A + df['Piaq122_A [um2/cm3]'].to_list()  
        else:
            p3_A = p3_A +  ['NaN'] * len(c0) 
        if r'Piaq122_M [ug/m3]' in df:
            p3_M = p3_M + df['Piaq122_M [ug/m3]'].to_list()  
        else:
            p3_M = p3_M +  ['NaN'] * len(c0) 
        if r'Piaq122_CMD []' in df:
            p3_CMD = p3_CMD + df['Piaq122_CMD []'].to_list()  
        else:
            p3_CMD = p3_CMD +  ['NaN'] * len(c0) 
        if 'Piaq122_H [%]' in df: 
            p3_H = p3_H + df['Piaq122_H [%]'].to_list()  
        else:
            p3_H = p3_H +  ['NaN'] * len(c0) 
        if r'Piaq122_T [°C]' in df:
            p3_T = p3_T + df['Piaq122_T [°C]'].to_list()  
        else:
            p3_T = p3_T +  ['NaN'] * len(c0) 
        if r'Piaq122_CO2 [ppm]' in df: 
            p3_CO2 = p3_CO2 + df['Piaq122_CO2 [ppm]'].to_list()  
        else:
            p3_CO2 = p3_CO2 +  ['NaN'] * len(c0) 

#Data[0] = header
sayandprint('PIAQ 3 files imported at')
# %% turn lists BACK into dataframe to be consistent with others 

p3_df = pd.DataFrame({'PIAQ3_time':p3_time,'PIAQ3_A [um2/cm3]':p3_A,\
                      'PIAQ3_sootM':p3_M,'PIAQ3_sootN':p3_N,'PIAQ3_T':p3_T,'PIAQ3_H':p3_H,\
                      'PIAQ3_CO2':p3_CO2,'PIAQ3_CMD':p3_CMD})
    
# %% make rows unique then reorder
p3_df = p3_df.drop_duplicates(keep='first')
p3_df = p3_df.sort_values('PIAQ3_time',axis=0,ascending=True,na_position='last')
# does sample length make sense?
no_sec = 60*24*3600 # for sample length of about 300 days (Feb- Dec)

# %% SAVE
# HDF5store because the file is so large - only if needed to avoid running this script again
sayandprint("PIAQ 3 variables saving")

store = pd.HDFStore('store.h5')
store['p3_df_97to102'] = p3_df

sayandprint("PIAQ 3 variables stored")

# %%
df = df.drop('Piaq122_T [°C]',axis=1)
