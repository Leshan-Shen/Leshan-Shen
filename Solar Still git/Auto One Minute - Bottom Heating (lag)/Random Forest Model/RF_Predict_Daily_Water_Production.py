# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 15:34:14 2021

@author: SLS
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 11:56:02 2021

@author: SLS
"""
#%%Import Needed Packages
import pandas as pd
import datetime
import numpy as np
#%%Program Start time
starttime = datetime.datetime.now()
#long running
#%% Read RF_Predict_Water_Production.csv
RF_Predict_Water_Production = pd.read_csv('RF_Predict_Water_Production.csv',index_col = 0) #Read csv file
#%%
RF_Predict_Water_Production['TIMESTAMP'] = pd.to_datetime(RF_Predict_Water_Production['TIMESTAMP'])
ID0_Clean_Data = RF_Predict_Water_Production[RF_Predict_Water_Production['ID'] == 0]
ID2_Clean_Data = RF_Predict_Water_Production[RF_Predict_Water_Production['ID'] == 2]
ID0_Clean_Data.index = range(0,len(ID0_Clean_Data))
ID2_Clean_Data.index = range(0,len(ID2_Clean_Data))
#Compare = pd.merge(ID0_Clean_Data, ID2_Clean_Data, on = 'TIMESTAMP')
#%%
ID0Mar_Daily_Water_Production = []
ID0March_Date = []
for i in range(1,32):
    ID0March_Data = []
    record_date = datetime.datetime(2021,3,i)
    record_date_plus_one = record_date + datetime.timedelta(days=+1) #Manipulate TIMESTAMP
    for value in ID0_Clean_Data['TIMESTAMP']:
        if value >= record_date:
            if value <= record_date_plus_one:
                RF_Predict_Weight_Values = ID0_Clean_Data['Predict_Net_Weight'][ID0_Clean_Data['TIMESTAMP'] == value].values[0]
                ID0March_Data.append(RF_Predict_Weight_Values)
    ID0March_Date.append(record_date)
    ID0Mar_Daily_Water_Production.append(round(sum(ID0March_Data),2))
ID0Mar_Daily_Water_Production = np.column_stack((ID0March_Date,ID0Mar_Daily_Water_Production))
#%%
ID0Apr_Daily_Water_Production = []
ID0April_Date = []
for i in range(1,31):
    ID0April_Data = []
    record_date = datetime.datetime(2021,4,i)
    record_date_plus_one = record_date + datetime.timedelta(days=+1) #Manipulate TIMESTAMP
    for value in ID0_Clean_Data['TIMESTAMP']:
        if value >= record_date:
            if value <= record_date_plus_one:
                RF_Predict_Weight_Values = ID0_Clean_Data['Predict_Net_Weight'][ID0_Clean_Data['TIMESTAMP'] == value].values[0]
                ID0April_Data.append(RF_Predict_Weight_Values)
    ID0April_Date.append(record_date)
    ID0Apr_Daily_Water_Production.append(round(sum(ID0April_Data),2))
ID0Apr_Daily_Water_Production = np.column_stack((ID0April_Date,ID0Apr_Daily_Water_Production))
#%%
ID2Mar_Daily_Water_Production = []
ID2March_Date = []
for i in range(1,32):
    ID2March_Data = []
    record_date = datetime.datetime(2021,3,i)
    record_date_plus_one = record_date + datetime.timedelta(days=+1) #Manipulate TIMESTAMP
    for value in ID2_Clean_Data['TIMESTAMP']:
        if value >= record_date:
            if value <= record_date_plus_one:
                RF_Predict_Weight_Values = ID2_Clean_Data['Predict_Net_Weight'][ID2_Clean_Data['TIMESTAMP'] == value].values[0]
                ID2March_Data.append(RF_Predict_Weight_Values)
    ID2March_Date.append(record_date)
    ID2Mar_Daily_Water_Production.append(round(sum(ID2March_Data),2))
ID2Mar_Daily_Water_Production = np.column_stack((ID2March_Date,ID2Mar_Daily_Water_Production))
#%%
ID2Apr_Daily_Water_Production = []
ID2April_Date = []
for i in range(1,31):
    ID2April_Data = []
    record_date = datetime.datetime(2021,4,i)
    record_date_plus_one = record_date + datetime.timedelta(days=+1) #Manipulate TIMESTAMP
    for value in ID2_Clean_Data['TIMESTAMP']:
        if value >= record_date:
            if value <= record_date_plus_one:
                RF_Predict_Weight_Values = ID2_Clean_Data['Predict_Net_Weight'][ID2_Clean_Data['TIMESTAMP'] == value].values[0]
                ID2April_Data.append(RF_Predict_Weight_Values)
    ID2April_Date.append(record_date)
    ID2Apr_Daily_Water_Production.append(round(sum(ID2April_Data),2))
ID2Apr_Daily_Water_Production = np.column_stack((ID2April_Date,ID2Apr_Daily_Water_Production))
#%%
ID0_RF_Predict_Daily_Water_Production = np.row_stack((ID0Mar_Daily_Water_Production,
                                               ID0Apr_Daily_Water_Production
                                               ))
ID2_RF_Predict_Daily_Water_Production = np.row_stack((ID2Mar_Daily_Water_Production,
                                               ID2Apr_Daily_Water_Production
                                               ))
ID0_RF_Predict_Daily_Water_Production = pd.DataFrame(ID0_RF_Predict_Daily_Water_Production,
                                           columns = ['TIMESTAMP','Water_Production'])
ID0_RF_Predict_Daily_Water_Production.insert(0,'ID',0)
ID2_RF_Predict_Daily_Water_Production = pd.DataFrame(ID2_RF_Predict_Daily_Water_Production,
                                           columns = ['TIMESTAMP','Water_Production'])
ID2_RF_Predict_Daily_Water_Production.insert(0,'ID',2)

RF_Predict_Daily_Water_Production = pd.concat([ID0_RF_Predict_Daily_Water_Production,ID2_RF_Predict_Daily_Water_Production],sort=True).reset_index(drop=True)

#%%
RF_Predict_Daily_Water_Production.to_csv('RF_Predict_Daily_Water_Production.csv')
#%%Program endding time
endtime = datetime.datetime.now()
print("该程序运行完成需要时间:", endtime-starttime)