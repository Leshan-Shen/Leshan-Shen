# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 09:18:05 2021

@author: SLS
"""

#%%Import Needed Packages
import pandas as pd
import datetime
import numpy as np
#%%Program Start time
starttime = datetime.datetime.now()
#long running
#%%Read Clean_Data
Clean_Data = pd.read_csv('Selected water production data-2021-03-29-2021-04-22.csv') #Read csv file
Clean_Data['TIMESTAMP'] = pd.to_datetime(Clean_Data['TIMESTAMP']).dt.strftime('%Y-%m-%d-%H:%M:00')
Clean_Data['TIMESTAMP'] = pd.to_datetime(Clean_Data['TIMESTAMP'])
Clean_Data = Clean_Data.drop(columns=['Unnamed: 0','DATE','WT','TIME','TEMP'])
#%%Seperate ID0 & ID2
ID0_CleanData = Clean_Data[Clean_Data['ID'] == 0]
ID2_CleanData = Clean_Data[Clean_Data['ID'] == 2]
ID0_CleanData.index = range(0,len(ID0_CleanData))
ID2_CleanData.index = range(0,len(ID2_CleanData))
#Compare = pd.merge(ID0_Clean_Data, ID2_Clean_Data, on = 'TIMESTAMP')
#%%Get net weight water production
ID0_CleanData['Net_Weight'] = ID0_CleanData['Weight']
for i in range(1,len(ID0_CleanData['Weight'])):
    if ID0_CleanData['Weight'][i] != 0:
        ID0_CleanData['Net_Weight'][i] = ID0_CleanData['Weight'][i] - ID0_CleanData['Weight'][i-1]
    else:
        ID0_CleanData['Net_Weight'][i] = ID0_CleanData['Net_Weight'][i-1]   
ID0_CleanData.index = range(0,len(ID0_CleanData))
#%%Get net weight water production
ID2_CleanData['Net_Weight'] = ID2_CleanData['Weight']
for i in range(1,len(ID2_CleanData['Weight'])):
    if ID2_CleanData['Weight'][i] != 0:
        ID2_CleanData['Net_Weight'][i] = ID2_CleanData['Weight'][i] - ID2_CleanData['Weight'][i-1]
    else:
        ID2_CleanData['Net_Weight'][i] = ID2_CleanData['Net_Weight'][i-1]   
ID2_CleanData.index = range(0,len(ID2_CleanData))
#%%Define average function
def average(*args):
    sum = 0
    if len(args) == 0:
        return sum
    for item in args:
        sum += item
    avg = sum/len(args)
    return avg
#%%
ID0_Clean_Data = [ID0_CleanData.iat[0,0],ID0_CleanData.iat[0,1], ID0_CleanData.iat[0,2]]
for i in range(1,int(len(ID0_CleanData)/5)):
    ID0_Clean_Data1 = [average(ID0_CleanData.iat[5*i-4,0], ID0_CleanData.iat[5*i-3,0], ID0_CleanData.iat[5*i-2,0], 
                                ID0_CleanData.iat[5*i-1,0], ID0_CleanData.iat[5*i-0,0]),
                        ID0_CleanData.iat[5*i-2,1],
                        average(ID0_CleanData.iat[5*i-4,3], ID0_CleanData.iat[5*i-3,3], ID0_CleanData.iat[5*i-2,3], 
                                ID0_CleanData.iat[5*i-1,3], ID0_CleanData.iat[5*i-0,3])]                       
    ID0_Clean_Data = np.row_stack((ID0_Clean_Data, ID0_Clean_Data1))
ID0_Clean_Data = pd.DataFrame(ID0_Clean_Data,columns=(['ID','TIMESTAMP','Net_Weight']))

#%%
ID2_Clean_Data = [ID2_CleanData.iat[0,0],ID2_CleanData.iat[0,1], ID2_CleanData.iat[0,2]]
for i in range(1,int(len(ID2_CleanData)/5)):
    ID2_Clean_Data1 = [average(ID2_CleanData.iat[5*i-4,0], ID2_CleanData.iat[5*i-3,0], ID2_CleanData.iat[5*i-2,0], 
                                ID2_CleanData.iat[5*i-1,0], ID2_CleanData.iat[5*i-0,0]),
                        ID2_CleanData.iat[5*i-2,1],
                        average(ID2_CleanData.iat[5*i-4,3], ID2_CleanData.iat[5*i-3,3], ID2_CleanData.iat[5*i-2,3], 
                                ID2_CleanData.iat[5*i-1,3], ID2_CleanData.iat[5*i-0,3])]                       
    ID2_Clean_Data = np.row_stack((ID2_Clean_Data, ID2_Clean_Data1))
ID2_Clean_Data = pd.DataFrame(ID2_Clean_Data,columns=(['ID','TIMESTAMP','Net_Weight']))
#%%
Net_Water_Production = pd.concat([ID0_Clean_Data[['ID','TIMESTAMP','Net_Weight']],
                                  ID2_Clean_Data[['ID','TIMESTAMP','Net_Weight']]]).reset_index(drop=True)
#%%
filename = ID0_Clean_Data['TIMESTAMP'].iat[1].strftime('Net_Water_Production-%Y-%m-%d') + ID0_Clean_Data['TIMESTAMP'].iat[-1].strftime('-%Y-%m-%d.csv')
Net_Water_Production.to_csv(filename)
#%%Program endding time
endtime = datetime.datetime.now()
print("该程序运行完成需要时间:", endtime-starttime)