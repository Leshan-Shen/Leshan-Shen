# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 15:02:16 2021

@author: SLS
"""

import pandas as pd
import numpy as np
import datetime
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import calendar
#import packages

#Get solar still water daily production data---------------------------------#
date_record = datetime.datetime(2020, 6, 5)
date_record = date_record.strftime('%Y-%m-%d')
#record date
SolarWater = pd.read_csv(r'D:\R\Solar Still\Bottom Interfacial Solar Still Water Production.csv',
                         header = None)
#read csv file
SolarWater_Day = [SolarWater.iat[0,0],SolarWater.iat[0,1]]
SolarWater_Day = np.mat(SolarWater_Day)
#change datatype from list to matrix

for i in range(1,int(SolarWater.shape[1]/2)):
    daydata = [SolarWater.iat[0, 2*i],SolarWater.iat[0, 2*i+1]]  
    daydata = np.mat(daydata)
    SolarWater_Day = np.row_stack((SolarWater_Day,daydata))

SolarWater_Day = pd.DataFrame(SolarWater_Day)
SolarWater_Day.columns = ['Date', 'Water_Production']
SolarWater_Day['Date'] = pd.to_datetime(SolarWater_Day['Date'])
SolarWater_Day['Date'] = SolarWater_Day['Date'].dt.strftime('%Y-%m-%d')
#get datetime format

SolarWater_Day['Date'] = SolarWater_Day['Date'][SolarWater_Day['Date'] >= date_record]
SolarWater_Day = SolarWater_Day.dropna(axis=0,how='any')
#dropna in dataframe

SolarWater_Day['Water_Production'] = pd.to_numeric(SolarWater_Day['Water_Production'])
SolarWater_Day['Water_Production'] = (SolarWater_Day['Water_Production']*4./1000)
SolarWater_Day['Water_Energy'] = SolarWater_Day['Water_Production']/1.5
#----------------------------------------------------------------------------#
#Get solar environment daily data--------------------------------------------#

SolarEnv_Day = pd.read_csv(r'C:\Users\JYB3\Desktop\浙江省能源集团有限公司技术研究院\能源化工研究所\新能源：太阳能海水淡化\实验原始数据\气象数据\CR1000_BSRN1000_Day201022.csv',
                           skiprows=[0])
SolarEnvUnit_Day = SolarEnv_Day.loc[[0],:]
SolarEnv_Day = SolarEnv_Day.drop(index = [0,1]) 
#Delete two rows of unit
SolarEnv_Day['TIMESTAMP'] = pd.to_datetime(SolarEnv_Day['TIMESTAMP'])
SolarEnv_Day['TIMESTAMP'] = SolarEnv_Day['TIMESTAMP'] + datetime.timedelta(days=-1)
SolarEnv_Day['TIMESTAMP'] = SolarEnv_Day['TIMESTAMP'].dt.strftime('%Y-%m-%d')

#SolarEnv_Day[SolarEnv_Day.columns[2:39]] = SolarEnv_Day[SolarEnv_Day.columns[2:39]].apply(pd.to_numeric)
#CANNOT RETURN NAN to Numeric Value
#----------------------------------------------------------------------------#
#Select data column and analysis---------------------------------------------#

SolarData_Day = SolarEnv_Day[["TIMESTAMP", "Global_Energy_Tot", "Direct_Energy_Tot", "Diffuse_Energy_Tot"]]
SolarData_Day['TIMESTAMP'] = SolarData_Day['TIMESTAMP'][SolarData_Day['TIMESTAMP'] >= date_record]
SolarData_Day = SolarData_Day.dropna(axis=0,how='any')
SolarDataUnit_Day = SolarEnvUnit_Day[["TIMESTAMP", "Global_Energy_Tot", "Direct_Energy_Tot", "Diffuse_Energy_Tot"]]
SolarWater_Day.rename(columns={'Date': 'TIMESTAMP'}, inplace=True)
SolarData_Day = pd.merge(SolarData_Day, SolarWater_Day[['TIMESTAMP','Water_Energy']], how='left', on='TIMESTAMP',
left_index=False, right_index=False, sort=None)
SolarEnergy_Day = pd.melt(SolarData_Day, id_vars =['TIMESTAMP'], value_vars =['Global_Energy_Tot'])


SolarData_Day[SolarData_Day.columns[1:4]] = SolarData_Day[SolarData_Day.columns[1:4]].apply(pd.to_numeric)
SolarData_Day['Global_Efficiency'] = SolarData_Day['Water_Energy']/SolarData_Day['Global_Energy_Tot']
SolarData_Day['DirDiffRatio'] = SolarData_Day['Direct_Energy_Tot']/SolarData_Day['Diffuse_Energy_Tot']
SolarData_Day['DirDiff'] = pd.cut(x=SolarData_Day['DirDiffRatio'],bins=[min(SolarData_Day['DirDiffRatio'])-0.01,0.1,1,max(SolarData_Day['DirDiffRatio'])], labels=['Cloudy', 'Between','Clear'])
#----------------------------------------------------------------------------#
SolarData_Day_full = SolarData_Day
SolarData_Day = SolarData_Day.dropna()
SolarData_Day.drop(index = [45,64,65],inplace = True)
Solar_feature_set_Dataframe = SolarData_Day[['Direct_Energy_Tot','Diffuse_Energy_Tot']]
Solar_feature_set = []

for values in Solar_feature_set_Dataframe:
    Solar_feature_set = Solar_feature_set_Dataframe.values.tolist()
    Solar_feature_set.append(Solar_feature_set)

Solar_feature_set.pop()
Solar_target_set = SolarData_Day['Global_Efficiency'].values.tolist()


model = LinearRegression()
model.fit(Solar_feature_set, Solar_target_set)

SolarData_Day = SolarData_Day_full
SolarData_Day['fit_Efficiency'] = model.intercept_ + model.coef_[0]*SolarData_Day['Direct_Energy_Tot'] + model.coef_[1]*SolarData_Day['Diffuse_Energy_Tot']

plt.figure()
plt.plot(SolarData_Day['Global_Energy_Tot'], SolarData_Day['Global_Efficiency'],'ro', label = 'Global_Efficiency')
plt.plot(SolarData_Day['Global_Energy_Tot'], SolarData_Day['fit_Efficiency'],'bo',label = 'fit Efficiency')
plt.legend()
plt.title('Global Energy Total vs Energy Use Efficiency')
plt.xlabel('Global Energy Total (KhW/m^2)')
plt.ylabel('Efficiency')
plt.show()

SolarData_Day.to_csv('D:\Python\Solar Still git\Bottom Interfacial Solar Still Daily Water Production.csv')

SolarData_Day['TIMESTAMP'] = pd.to_datetime(SolarData_Day['TIMESTAMP'],format="%Y/%m/%d").dt.date

plt.figure()
plt.plot(SolarData_Day['TIMESTAMP'], SolarData_Day['Global_Efficiency'],'ko', label = 'Global Efficiency')
plt.legend()
plt.title('Timestamp vs Global Efficiency')
plt.xlabel('TIMESTAMP')
plt.xticks(rotation=45)
plt.ylabel('Global Efficiency')
plt.show()


