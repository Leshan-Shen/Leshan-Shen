# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 10:23:29 2021

@author: SLS
"""
import pandas as pd
import datetime
import joblib
#%%Program Start time
starttime = datetime.datetime.now()
#long running
#%%Import RF Model
model0 = joblib.load('ID0 RF Model-2021-03-29-2021-04-22')
model2 = joblib.load('ID2 RF Model-2021-03-29-2021-04-22')
#%%Get solar environment minute data
SolarEnv_Day = pd.read_csv('20210426-CR1000_BSRN1000_Min.csv', skiprows=[0]) #Read csv file, skip first line
SolarEnvUnit_Day = SolarEnv_Day.loc[[0],:] #Get solarEnv_Day unit row
SolarEnv_Day = SolarEnv_Day.drop(index = [0,1]) #Drop unneeded data rows, Delete two rows of unit
SolarEnv_Day['TIMESTAMP'] = pd.to_datetime(SolarEnv_Day['TIMESTAMP']) #Change types to datetime
SolarEnv_Day[SolarEnv_Day.columns[2:50]] = SolarEnv_Day[SolarEnv_Day.columns[2:50]].apply(pd.to_numeric,errors = 'coerce')
#Types to float
#%%Column Selection
SolarData_Day = SolarEnv_Day[["TIMESTAMP", "Global_Avg", "Direct_Avg", 
                              "Diffuse_Avg",'AirTemp_C_Avg','WS_ms_Avg','RH_Avg',
                              'Press_Avg']] #Column selection
SolarData_Day = SolarData_Day.dropna(axis=0,how='any') #Drop nan
#%%Read Net Water Production
Clean_Data = pd.read_csv('Net_Water_Production-2021-03-29-2021-04-25.csv',index_col= 0) #Read csv file
Clean_Data['TIMESTAMP'] = pd.to_datetime(Clean_Data['TIMESTAMP'])
#%%Seperate data according different Solar Still Types
ID0_Clean_Data = Clean_Data[Clean_Data['ID'] == 0]
ID2_Clean_Data = Clean_Data[Clean_Data['ID'] == 2]
ID0_Clean_Data.index = range(0,len(ID0_Clean_Data))
ID2_Clean_Data.index = range(0,len(ID2_Clean_Data))
#%%Manipulate TIMESTAMP, Bottom heating having a lag in terms of solar env data and net water production
###
SolarEnv_Day['TIMESTAMP'] = SolarEnv_Day['TIMESTAMP'] + datetime.timedelta(hours=-1) 
###
#%%Merge Net Water Production and Solar Env Data
SolarData_Day_ID0 = pd.merge(SolarData_Day, ID0_Clean_Data, how='right', on='TIMESTAMP',
left_index=False, right_index=False, sort=None)
#Merge based on right "TIMESTAMP"
SolarData_Day_ID2 = pd.merge(SolarData_Day, ID2_Clean_Data, how='right', on='TIMESTAMP',
left_index=False, right_index=False, sort=None)
#Merge based on right "TIMESTAMP
#%%
Model_SolarData_ID0 = SolarData_Day_ID0.drop(columns ='Net_Weight')
X = SolarData_Day_ID0[['Global_Avg','AirTemp_C_Avg','WS_ms_Avg','RH_Avg',
                              'Press_Avg']]
ID0_Predictions = model0.predict(X)/100
Model_SolarData_ID0['Predict_Net_Weight'] = ID0_Predictions
Model_SolarData_ID0.drop(columns = ['Global_Avg','AirTemp_C_Avg','WS_ms_Avg','RH_Avg','Press_Avg','Direct_Avg','Diffuse_Avg'],
                                       inplace = True)

#%%
Model_SolarData_ID2 = SolarData_Day_ID2.drop(columns ='Net_Weight')
X2 = SolarData_Day_ID2[['Global_Avg','AirTemp_C_Avg','WS_ms_Avg','RH_Avg',
                              'Press_Avg']]
ID2_Predictions = model2.predict(X2)/100
Model_SolarData_ID2['Predict_Net_Weight'] = ID2_Predictions
Model_SolarData_ID2.drop(columns = ['Global_Avg','AirTemp_C_Avg','WS_ms_Avg','RH_Avg','Press_Avg','Direct_Avg','Diffuse_Avg'],
                                       inplace = True)
#%%
Predict_Water_Production = pd.concat([Model_SolarData_ID0,Model_SolarData_ID2]).reset_index(drop=True)
#%%
Predict_Water_Production.to_csv('RF_Predict_Water_Production.csv')
#%%Program endding time
endtime = datetime.datetime.now()
print("该程序运行完成需要时间:", endtime-starttime)