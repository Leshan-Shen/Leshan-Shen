# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 14:13:06 2021

@author: SLS
"""
#%%
import pandas as pd
import datetime
#%%Get solar still water daily production data
#date_record = datetime.datetime(int(input('请输入年份（xxxx）: ')), int(input('请输入月份（xx）: ')), 
                                #int(input('请输入日期（xx）: ')))
date_record = datetime.datetime(2020,12,2)
date_record = date_record.strftime('%Y-%m-%d') #Record date
SolarWater = pd.read_csv('Desalination Production.csv') #Read csv file
SolarWater = SolarWater[SolarWater['Time'].notnull() == False]
SolarWater = SolarWater.drop(columns = ['Time'])
SolarWater['Date'] = pd.to_datetime(SolarWater['Date'],format = ('%Y%m%d')) #Types to datetime
SolarWater['Date'] = SolarWater['Date'].dt.strftime('%Y-%m-%d') #Get datetime format
SolarWater['Date'] = SolarWater['Date'][SolarWater['Date'] >= date_record] #Select needed data
SolarWater = SolarWater[SolarWater['Date'].notnull() == True]
SolarWater['Stepwise_Bottom_Heating_Energy_Production'] = SolarWater['Stepwise_Bottom_Heating']/1000/1.5/0.6/0.6
SolarWater['InvertPyramid_Bottom_Heating_Energy_Production'] = SolarWater['InvertPyramid_Bottom_Heating']/1000/1.5/0.6/0.6
SolarWater['Sidewall_Interfacial_Energy_Production'] = SolarWater['Sidewall_Interfacial']/1000/1.5/0.5/0.5
SolarWater['Bottom_Heating_Energy_Production'] = SolarWater['Bottom_Heating']/1000/1.5/0.5/0.5
SolarWater['Foam_Bottom_Interfacial_Energy_Production'] = SolarWater['Foam_Bottom_Interfacial']/1000/1.5/0.5/0.45
SolarWater_Day = SolarWater.drop(columns=['Stepwise_Bottom_Heating','InvertPyramid_Bottom_Heating',
                                          'Sidewall_Interfacial','Bottom_Heating','Foam_Bottom_Interfacial'])
#%%Get solar environment daily data
SolarEnv_Day = pd.read_csv('CR1000_BSRN1000_Day210322.csv', skiprows=[0]) #Read csv file, skip first line
SolarEnvUnit_Day = SolarEnv_Day.loc[[0],:] #Get solarEnv_Day unit row
SolarEnv_Day = SolarEnv_Day.drop(index = [0,1]) #Drop unneeded data rows, Delete two rows of unit
SolarEnv_Day['TIMESTAMP'] = pd.to_datetime(SolarEnv_Day['TIMESTAMP']) #Change types to datetime
SolarEnv_Day['TIMESTAMP'] = SolarEnv_Day['TIMESTAMP'] + datetime.timedelta(days=-1) #Manipulate TIMESTAMP, env_data is the integral of the previous day
SolarEnv_Day['TIMESTAMP'] = SolarEnv_Day['TIMESTAMP'].dt.strftime('%Y-%m-%d') #Get datetime format
SolarEnv_Day[SolarEnv_Day.columns[2:50]] = SolarEnv_Day[SolarEnv_Day.columns[2:50]].apply(pd.to_numeric,errors = 'coerce')
#Types to float
SolarData_Day = SolarEnv_Day.drop(columns = ['RECORD']) #Column selection
SolarData_Day['TIMESTAMP'] = SolarData_Day['TIMESTAMP'][SolarData_Day['TIMESTAMP'] >= date_record] #Select needed data
SolarData_Day = SolarData_Day[SolarData_Day['TIMESTAMP'].notnull() == True] #Drop nan
SolarDataUnit_Day = SolarEnvUnit_Day.drop(columns = ['RECORD']) #Get solardata_day unit
SolarWater_Day.rename(columns={'Date': 'TIMESTAMP'}, inplace=True) #Rename date to timestamp for merge later
SolarData_Day = pd.merge(SolarWater_Day, SolarData_Day, how='left', on='TIMESTAMP',
left_index=False, right_index=False, sort=None)
#Merge based on left "TIMESTAMP"
#%%Save processed dataframe to a new csv file
SolarData_Day.to_csv('D:\Python\Solar Still git\Manipulated Data Set\Daily Water Production Summary with Env_Data.csv',
                     na_rep = 'nan')
#blank to nan