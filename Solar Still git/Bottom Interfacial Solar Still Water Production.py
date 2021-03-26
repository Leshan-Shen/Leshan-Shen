# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 15:02:16 2021

@author: SLS
"""
#%%Import packages
import pandas as pd
import numpy as np
import datetime
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import sys
sys.path.append('D:\Python\Self-defined Modules')
import linear_plot
#%%Get solar still water daily production data
#date_record = datetime.datetime(int(input('请输入年份（xxxx）: ')), int(input('请输入月份（xx）: ')), 
                                #int(input('请输入日期（xx）: ')))
#user input if needed
date_record = datetime.datetime(2020, 6, 5)
date_record = date_record.strftime('%Y-%m-%d') #Record date
SolarWater = pd.read_csv('Bottom Interfacial Solar Still Water Production.csv', header = None) #Read csv file
SolarWater_Day = [SolarWater.iat[0,0],SolarWater.iat[0,1]] 
SolarWater_Day = np.mat(SolarWater_Day) #Change datatype from list to matrix
for i in range(1,int(SolarWater.shape[1]/2)):
    daydata = [SolarWater.iat[0, 2*i],SolarWater.iat[0, 2*i+1]]  
    daydata = np.mat(daydata)
    SolarWater_Day = np.row_stack((SolarWater_Day,daydata))
SolarWater_Day = pd.DataFrame(SolarWater_Day) #Types to dataframe
SolarWater_Day.columns = ['Date', 'Water_Production'] #Columns header names
SolarWater_Day['Date'] = pd.to_datetime(SolarWater_Day['Date']) #Types to datetime
SolarWater_Day['Date'] = SolarWater_Day['Date'].dt.strftime('%Y-%m-%d') #Get datetime format
SolarWater_Day['Date'] = SolarWater_Day['Date'][SolarWater_Day['Date'] >= date_record] #Select needed data
SolarWater_Day = SolarWater_Day.dropna(axis=0,how='any') #Drop nan in dataframe
SolarWater_Day['Water_Production'] = pd.to_numeric(SolarWater_Day['Water_Production']) #Types to float 
SolarWater_Day['Water_Production'] = (SolarWater_Day['Water_Production']*4./1000)
#Manipulate water production column
SolarWater_Day['Water_Energy'] = SolarWater_Day['Water_Production']/1.5 #Get water energy column
#%%Get solar environment daily data
SolarEnv_Day = pd.read_csv('CR1000_BSRN1000_Day210322.csv', skiprows=[0]) #Read csv file, skip first line
SolarEnvUnit_Day = SolarEnv_Day.loc[[0],:] #Get solarEnv_Day unit row
SolarEnv_Day = SolarEnv_Day.drop(index = [0,1]) #Drop unneeded data rows, Delete two rows of unit
SolarEnv_Day['TIMESTAMP'] = pd.to_datetime(SolarEnv_Day['TIMESTAMP']) #Change types to datetime
SolarEnv_Day['TIMESTAMP'] = SolarEnv_Day['TIMESTAMP'] + datetime.timedelta(days=-1) #Manipulate TIMESTAMP, env_data is the integral of the previous day
SolarEnv_Day['TIMESTAMP'] = SolarEnv_Day['TIMESTAMP'].dt.strftime('%Y-%m-%d') #Get datetime format
SolarEnv_Day[SolarEnv_Day.columns[2:50]] = SolarEnv_Day[SolarEnv_Day.columns[2:50]].apply(pd.to_numeric,errors = 'coerce')
#Types to float
#%%Select data column and merge to form data for analysis
SolarData_Day = SolarEnv_Day[["TIMESTAMP", "Global_Energy_Tot", "Direct_Energy_Tot", 
                              "Diffuse_Energy_Tot"]] #Column selection
SolarData_Day['TIMESTAMP'] = SolarData_Day['TIMESTAMP'][SolarData_Day['TIMESTAMP'] >= date_record] #Select needed data
SolarData_Day = SolarData_Day.dropna(axis=0,how='any') #Drop nan
SolarDataUnit_Day = SolarEnvUnit_Day[["TIMESTAMP", "Global_Energy_Tot", "Direct_Energy_Tot", 
                                      "Diffuse_Energy_Tot"]] #Get solardata_day unit
SolarWater_Day.rename(columns={'Date': 'TIMESTAMP'}, inplace=True) #Rename date to timestamp for merge later
SolarData_Day = pd.merge(SolarData_Day, SolarWater_Day[['TIMESTAMP','Water_Energy']], how='left', on='TIMESTAMP',
left_index=False, right_index=False, sort=None)
#Merge based on left "TIMESTAMP"
#%%Data analysis
SolarEnergy_Day = pd.melt(SolarData_Day, id_vars =['TIMESTAMP'], value_vars =['Global_Energy_Tot']) 
#Melt to get SolarEnergy_Day
SolarData_Day['Global_Efficiency'] = SolarData_Day['Water_Energy']/SolarData_Day['Global_Energy_Tot']
#Get Global_Efficiency column
SolarData_Day['DirDiffRatio'] = SolarData_Day['Direct_Energy_Tot']/SolarData_Day['Diffuse_Energy_Tot']
#Get DirDiffRatio column
SolarData_Day['DirDiff'] = pd.cut(x=SolarData_Day['DirDiffRatio'],
                                  bins=[min(SolarData_Day['DirDiffRatio'])-0.01,0.1,1,
                                        max(SolarData_Day['DirDiffRatio'])], 
                                  labels=['Cloudy', 'Between','Clear']) 
#Categorize DirDiffRatio in Dirdiff
#%%Linear Regression Machine Learning of Direct Energy Total, Diffuse Energy Total, and Global Efficiency
SolarData_Day_full = SolarData_Day #Save SolarData_Day_full for future use
SolarData_Day = SolarData_Day.dropna() #Drop nan
SolarData_Day.drop(index = [45,64,65],inplace = True) #Drop manually selected inaccurate data
Solar_feature_set_Dataframe = SolarData_Day[['Direct_Energy_Tot','Diffuse_Energy_Tot']]
Solar_feature_set = [] #Set list

for values in Solar_feature_set_Dataframe:
    Solar_feature_set = Solar_feature_set_Dataframe.values.tolist()
    Solar_feature_set.append(Solar_feature_set) #Dataframe to list

Solar_feature_set.pop() #Delete the last element of a list
Solar_target_set = SolarData_Day['Global_Efficiency'].values.tolist() #Dataframe to list

model = LinearRegression()
model.fit(Solar_feature_set, Solar_target_set) #Set model for linear regression fit

SolarData_Day = SolarData_Day_full #Recover dataframe including undeleted "nan"
SolarData_Day['fit_Efficiency'] = model.intercept_ + model.coef_[0]*SolarData_Day['Direct_Energy_Tot'] + model.coef_[1]*SolarData_Day['Diffuse_Energy_Tot']
#Get fit_Efficiency from linear regression learning
#%%Plot Global Energy Total vs Energy Use Efficiency (including linear fit efficiency)
plt.figure()
plt.plot(SolarData_Day['Global_Energy_Tot'], SolarData_Day['Global_Efficiency'],'ro', label = 'Global_Efficiency')
plt.plot(SolarData_Day['Global_Energy_Tot'], SolarData_Day['fit_Efficiency'],'bo',label = 'fit Efficiency')
plt.legend()
plt.title('Global Energy Total vs Energy Use Efficiency')
plt.xlabel('Global Energy Total (KhW/m^2)')
plt.ylabel('Efficiency')
plt.show()
#%%Save processed dataframe to a new csv file
SolarData_Day.to_csv('D:\Python\Solar Still git\Manipulated Data Set\Bottom Interfacial Solar Still Daily Water Production.csv')
#%%Plot Global Energy Total vs Water Energy
SolarData_Day_nona = SolarData_Day.dropna() #Drop nan
fig, ax = plt.subplots() #name plot
linear_plot.linear_plot(SolarData_Day_nona['Global_Energy_Tot'].values.tolist(),SolarData_Day_nona['Water_Energy'].values.tolist())
#Linear_plot program from self-defined linear_plot module
plt.title('Global Energy Total vs Water Energy')
plt.xlabel('Global Energy Total (KhW/m^2)')
plt.ylabel('Water Energy (KhW/m^2)')

for i, txt in enumerate(SolarData_Day_nona['TIMESTAMP'].values.tolist()):
    if i % 2 == 0:
        ax.text(SolarData_Day_nona['Global_Energy_Tot'].values.tolist()[i], SolarData_Day_nona['Water_Energy'].values.tolist()[i],txt,
            position = (SolarData_Day_nona['Global_Energy_Tot'].values.tolist()[i], SolarData_Day_nona['Water_Energy'].values.tolist()[i]+0.1),
            horizontalalignment = 'center', size = 'xx-small')
    else:
        ax.text(SolarData_Day_nona['Global_Energy_Tot'].values.tolist()[i], SolarData_Day_nona['Water_Energy'].values.tolist()[i],txt,
            position = (SolarData_Day_nona['Global_Energy_Tot'].values.tolist()[i], SolarData_Day_nona['Water_Energy'].values.tolist()[i]-0.1),
            horizontalalignment = 'center', size = 'xx-small')
#Try to avoid overlapping of labels, not very successful
#%%Plot Timestamp vs Global Efficiency
SolarData_Day['TIMESTAMP'] = pd.to_datetime(SolarData_Day['TIMESTAMP'],format="%Y/%m/%d").dt.date
plt.figure()
plt.plot(SolarData_Day['TIMESTAMP'], SolarData_Day['Global_Efficiency'],'ko', label = 'Global Efficiency')
plt.legend()
plt.title('Timestamp vs Global Efficiency')
plt.xlabel('TIMESTAMP')
plt.ylabel('Global Efficiency')
plt.show()  
#%%Plot Global Energy Total vs Global Efficiency
plt.figure()
iCloudy, iBetween, iClear = [], [], []
for i, status in enumerate(SolarData_Day['DirDiff'].values.tolist()):
        if status == 'Cloudy':
            plt.plot(SolarData_Day['Global_Energy_Tot'][i], SolarData_Day['Global_Efficiency'][i], 'ro')
            iCloudy.append(i)
        elif status == 'Between':
            plt.plot(SolarData_Day['Global_Energy_Tot'][i], SolarData_Day['Global_Efficiency'][i], 'go')
            iBetween.append(i)
        elif status == 'Clear':
            plt.plot(SolarData_Day['Global_Energy_Tot'][i], SolarData_Day['Global_Efficiency'][i], 'bo')
            iClear.append(i)
        else:
            plt.plot(SolarData_Day['Global_Energy_Tot'][i], SolarData_Day['Global_Efficiency'][i], 'ko')
#Plot different color plot distinguished by category in 'DirDiff'
p1 = linear_plot.plot_reg(SolarData_Day['Global_Energy_Tot'][iCloudy].values.tolist(),SolarData_Day['Global_Efficiency'][iCloudy].values.tolist(),
                     'r-', 'Cloundy')
p2 = linear_plot.plot_reg(SolarData_Day['Global_Energy_Tot'][iBetween].values.tolist(),SolarData_Day['Global_Efficiency'][iBetween].values.tolist(),
                     'g-', 'Between')
p3 = linear_plot.plot_reg(SolarData_Day['Global_Energy_Tot'][iClear].values.tolist(),SolarData_Day['Global_Efficiency'][iClear].values.tolist(),
                     'b-', 'Clear')
#plot_reg program from self-defined linear_plot module
plt.legend(loc='lower right',title = 'Category',frameon = False)
plt.title('Global Energy Total vs Global Efficiency')
plt.xlabel('Global Energy Total (KhW/m^2)')
plt.ylabel('Global Efficiency')
#%%Plot Energy Distribution Summary vs Timestamp bar diagram
plt.figure()
plt.bar(x=SolarData_Day['TIMESTAMP'], height=SolarData_Day['Global_Energy_Tot'], 
        label='Global Energy Total', color='red', alpha=0.8)
plt.bar(x=SolarData_Day['TIMESTAMP'], height=SolarData_Day['Direct_Energy_Tot'], 
        label='Direct Energy Total', color='green', alpha=0.8)
plt.bar(x=SolarData_Day['TIMESTAMP'], height=SolarData_Day['Diffuse_Energy_Tot'], 
        label='Diffuse Energy Total', color='blue', alpha=0.8)
plt.bar(x=SolarData_Day['TIMESTAMP'], height=SolarData_Day['Water_Energy'], 
        label='Water Energy', color='purple', alpha=0.8)
plt.legend(loc = 'upper right', title = 'Different Energy Category',frameon = False)
plt.title('Energy Distribution Summary vs Timestamp')
plt.xlabel('TIMESTAMP')
plt.ylabel('Energy (KhW/m^2)')