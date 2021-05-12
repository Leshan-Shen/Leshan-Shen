# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 16:36:45 2021

@author: SLS
"""
#%%Import needed packages
import pandas as pd
import datetime
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
#%%Program Start time
starttime = datetime.datetime.now()
#long running
#%%Read Net Water Production
Clean_Data = pd.read_csv('Net_Water_Production-2021-03-29-2021-04-22.csv',index_col= 0) #Read csv file
Clean_Data['TIMESTAMP'] = pd.to_datetime(Clean_Data['TIMESTAMP'])
#%%Seperate data according different Solar Still Types
ID0_Clean_Data = Clean_Data[Clean_Data['ID'] == 0]
ID2_Clean_Data = Clean_Data[Clean_Data['ID'] == 2]
ID0_Clean_Data.index = range(0,len(ID0_Clean_Data))
ID2_Clean_Data.index = range(0,len(ID2_Clean_Data))
#%%Get solar environment minute data
SolarEnv_Day = pd.read_csv('20210426-CR1000_BSRN1000_Min.csv', skiprows=[0]) #Read csv file, skip first line
SolarEnvUnit_Day = SolarEnv_Day.loc[[0],:] #Get solarEnv_Day unit row
SolarEnv_Day = SolarEnv_Day.drop(index = [0,1]) #Drop unneeded data rows, Delete two rows of unit
SolarEnv_Day['TIMESTAMP'] = pd.to_datetime(SolarEnv_Day['TIMESTAMP']) #Change types to datetime
SolarEnv_Day[SolarEnv_Day.columns[2:50]] = SolarEnv_Day[SolarEnv_Day.columns[2:50]].apply(pd.to_numeric,errors = 'coerce')
#Types to float
#%%Select data column and merge to form data for analysis
SolarData_Day = SolarEnv_Day[["TIMESTAMP", "Global_Avg", "Direct_Avg", 
                              "Diffuse_Avg",'AirTemp_C_Avg','WS_ms_Avg','RH_Avg',
                              'Press_Avg']] #Column selection
SolarData_Day = SolarData_Day.dropna(axis=0,how='any') #Drop nan
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
#%% Model based on only global
X = SolarData_Day_ID0[['Global_Avg','AirTemp_C_Avg','WS_ms_Avg','RH_Avg',
                              'Press_Avg']]
y = SolarData_Day_ID0['Net_Weight']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)
#Spilt test and train data sets by ratio 2:8
y_train = y_train*100
y_test = y_test*100
#Need Integers for Model Fitting,*100 to maintain all the values
model0 = DecisionTreeClassifier()
#Create a DT Classifier
model0.fit(X_train, y_train.astype(int))
#Need Integers for Model Fitting
#%%Save Model in seperate files
filename = ID0_Clean_Data['TIMESTAMP'].iat[1].strftime('ID0 DT Model-%Y-%m-%d') + ID0_Clean_Data['TIMESTAMP'].iat[-1].strftime('-%Y-%m-%d')
joblib.dump(model0,filename)
#%%Model Accurate Estimation
predictions0 = model0.predict(X_test)
score = accuracy_score(y_test.astype(int), predictions0)
print(score)
#%% Model based on only global
X2 = SolarData_Day_ID2[['Global_Avg','AirTemp_C_Avg','WS_ms_Avg','RH_Avg',
                              'Press_Avg']]
y2 = SolarData_Day_ID2['Net_Weight']
X2_train, X2_test, y2_train, y2_test = train_test_split(X2, y2, test_size = 0.2)
#Spilt test and train data sets by ratio 2:8
y2_train = y2_train*100
y2_test = y2_test*100
#Need Integer for Model Fitting,*100 to maintain all the values
model2 = DecisionTreeClassifier()
model2.fit(X2_train, y2_train.astype(int))
#Need Integers for Model Fitting
#%%Save Model in seperate files
filename = ID2_Clean_Data['TIMESTAMP'].iat[1].strftime('ID2 DT Model-%Y-%m-%d') + ID2_Clean_Data['TIMESTAMP'].iat[-1].strftime('-%Y-%m-%d')
joblib.dump(model2,filename)
#%%Model Accurate Estimation
predictions2 = model2.predict(X2_test)
score = accuracy_score(y2_test.astype(int), predictions2)
print(score)
#%%Program endding time
endtime = datetime.datetime.now()
print("该程序运行完成需要时间:", endtime-starttime)