# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 16:23:43 2021

@author: SLS
"""
#%%
import pandas as pd
import datetime
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import sys
sys.path.append('D:\Python\Self-defined Modules')
import linear_plot
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
SolarEnv_Day[SolarEnv_Day.columns[2:39]] = SolarEnv_Day[SolarEnv_Day.columns[2:39]].apply(pd.to_numeric,errors = 'coerce')
#Types to float
#%%Select data column and merge to form data for analysis
SolarData_Day = SolarEnv_Day[["TIMESTAMP", "Global_Energy_Tot", "Direct_Energy_Tot", 
                              "Diffuse_Energy_Tot"]] #Column selection
SolarData_Day['TIMESTAMP'] = SolarData_Day['TIMESTAMP'][SolarData_Day['TIMESTAMP'] >= date_record] #Select needed data
SolarData_Day = SolarData_Day.dropna(axis=0,how='any') #Drop nan
SolarDataUnit_Day = SolarEnvUnit_Day[["TIMESTAMP", "Global_Energy_Tot", "Direct_Energy_Tot", 
                                      "Diffuse_Energy_Tot"]] #Get solardata_day unit
SolarWater_Day.rename(columns={'Date': 'TIMESTAMP'}, inplace=True) #Rename date to timestamp for merge later
SolarData_Day = pd.merge(SolarData_Day, SolarWater_Day, how='left', on='TIMESTAMP',
left_index=False, right_index=False, sort=None)
#%%Data analysis
SolarEnergy_Day = pd.melt(SolarData_Day, id_vars =['TIMESTAMP'], value_vars =['Global_Energy_Tot']) 
#Melt to get SolarEnergy_Day
SolarData_Day['Stepwise_Bottom_Heating_Global_Efficiency'] = SolarData_Day['Stepwise_Bottom_Heating_Energy_Production']/SolarData_Day['Global_Energy_Tot']
#Get Stepwise_Bottom_Heating_Global_Efficiency column
SolarData_Day['InvertPyramid_Bottom_Heating_Global_Efficiency'] = SolarData_Day['InvertPyramid_Bottom_Heating_Energy_Production']/SolarData_Day['Global_Energy_Tot']
#Get InvertPyramid_Bottom_Heating_Global_Efficiency column
SolarData_Day['Sidewall_Interfacial_Global_Efficiency'] = SolarData_Day['Sidewall_Interfacial_Energy_Production']/SolarData_Day['Global_Energy_Tot']
#Get Sidewall_Interfacial_Global_Efficiency column
SolarData_Day['Bottom_Heating_Global_Efficiency'] = SolarData_Day['Bottom_Heating_Energy_Production']/SolarData_Day['Global_Energy_Tot']
#Get Bottom_Heating_Global_Efficiency column
SolarData_Day['Foam_Bottom_Interfacial_Global_Efficiency'] = SolarData_Day['Foam_Bottom_Interfacial_Energy_Production']/SolarData_Day['Global_Energy_Tot']
#Get Foam_Bottom_Interfacial_Efficiency column
SolarData_Day['DirDiffRatio'] = SolarData_Day['Direct_Energy_Tot']/SolarData_Day['Diffuse_Energy_Tot']
#Get DirDiffRatio column
SolarData_Day['DirDiff'] = pd.cut(x=SolarData_Day['DirDiffRatio'],
                                  bins=[min(SolarData_Day['DirDiffRatio'])-0.01,0.1,1,
                                        max(SolarData_Day['DirDiffRatio'])], 
                                  labels=['Cloudy', 'Between','Clear']) 
#Categorize DirDiffRatio in Dirdiff
#%%Linear Regression Machine Learning of Direct Energy Total, Diffuse Energy Total, and Stepwise_Bottom_Heating Global Efficiency
SolarData_Day_full = SolarData_Day #Save SolarData_Day_full for future use
SolarData_Day = SolarData_Day.dropna() #Drop nan
Solar_feature_set_Dataframe = SolarData_Day[['Direct_Energy_Tot','Diffuse_Energy_Tot']]
Solar_feature_set = [] #Set list

for values in Solar_feature_set_Dataframe:
    Solar_feature_set = Solar_feature_set_Dataframe.values.tolist()
    Solar_feature_set.append(Solar_feature_set) #Dataframe to list

Solar_feature_set.pop() #Delete the last element of a list
Solar_target_set = SolarData_Day['Stepwise_Bottom_Heating_Global_Efficiency'].values.tolist() #Dataframe to list

model = LinearRegression()
model.fit(Solar_feature_set, Solar_target_set) #Set model for linear regression fit

SolarData_Day = SolarData_Day_full #Recover dataframe including undeleted "nan"
SolarData_Day['Stepwise_Bottom_Heating_fit_Efficiency'] = model.intercept_ + model.coef_[0]*SolarData_Day['Direct_Energy_Tot'] + model.coef_[1]*SolarData_Day['Diffuse_Energy_Tot']
#Get Stepwise_Bottom_Heating_fit_Efficiency from linear regression learning
#%%Linear Regression Machine Learning of Direct Energy Total, Diffuse Energy Total, and InvertPyramid_Bottom_Heating Global Efficiency
SolarData_Day_full = SolarData_Day #Save SolarData_Day_full for future use
SolarData_Day = SolarData_Day.dropna() #Drop nan
Solar_feature_set_Dataframe = SolarData_Day[['Direct_Energy_Tot','Diffuse_Energy_Tot']]
Solar_feature_set = [] #Set list

for values in Solar_feature_set_Dataframe:
    Solar_feature_set = Solar_feature_set_Dataframe.values.tolist()
    Solar_feature_set.append(Solar_feature_set) #Dataframe to list

Solar_feature_set.pop() #Delete the last element of a list
Solar_target_set = SolarData_Day['InvertPyramid_Bottom_Heating_Global_Efficiency'].values.tolist() #Dataframe to list

model = LinearRegression()
model.fit(Solar_feature_set, Solar_target_set) #Set model for linear regression fit

SolarData_Day = SolarData_Day_full #Recover dataframe including undeleted "nan"
SolarData_Day['InvertPyramid_Bottom_Heating_fit_Efficiency'] = model.intercept_ + model.coef_[0]*SolarData_Day['Direct_Energy_Tot'] + model.coef_[1]*SolarData_Day['Diffuse_Energy_Tot']
#Get Stepwise_Bottom_Heating_fit_Efficiency from linear regression learning
#%%Linear Regression Machine Learning of Direct Energy Total, Diffuse Energy Total, and Sidewall_Interfacial Global Efficiency
SolarData_Day_full = SolarData_Day #Save SolarData_Day_full for future use
SolarData_Day = SolarData_Day.dropna() #Drop nan
Solar_feature_set_Dataframe = SolarData_Day[['Direct_Energy_Tot','Diffuse_Energy_Tot']]
Solar_feature_set = [] #Set list

for values in Solar_feature_set_Dataframe:
    Solar_feature_set = Solar_feature_set_Dataframe.values.tolist()
    Solar_feature_set.append(Solar_feature_set) #Dataframe to list

Solar_feature_set.pop() #Delete the last element of a list
Solar_target_set = SolarData_Day['Sidewall_Interfacial_Global_Efficiency'].values.tolist() #Dataframe to list

model = LinearRegression()
model.fit(Solar_feature_set, Solar_target_set) #Set model for linear regression fit

SolarData_Day = SolarData_Day_full #Recover dataframe including undeleted "nan"
SolarData_Day['Sidewall_Interfacial_fit_Efficiency'] = model.intercept_ + model.coef_[0]*SolarData_Day['Direct_Energy_Tot'] + model.coef_[1]*SolarData_Day['Diffuse_Energy_Tot']
#Get Sidewall_Interfacial_fit_Efficiency from linear regression learning
#%%Linear Regression Machine Learning of Direct Energy Total, Diffuse Energy Total, and Bottom_Heating Global Efficiency
SolarData_Day_full = SolarData_Day #Save SolarData_Day_full for future use
SolarData_Day = SolarData_Day.dropna() #Drop nan
Solar_feature_set_Dataframe = SolarData_Day[['Direct_Energy_Tot','Diffuse_Energy_Tot']]
Solar_feature_set = [] #Set list

for values in Solar_feature_set_Dataframe:
    Solar_feature_set = Solar_feature_set_Dataframe.values.tolist()
    Solar_feature_set.append(Solar_feature_set) #Dataframe to list

Solar_feature_set.pop() #Delete the last element of a list
Solar_target_set = SolarData_Day['Bottom_Heating_Global_Efficiency'].values.tolist() #Dataframe to list

model = LinearRegression()
model.fit(Solar_feature_set, Solar_target_set) #Set model for linear regression fit

SolarData_Day = SolarData_Day_full #Recover dataframe including undeleted "nan"
SolarData_Day['Bottom_Heating_fit_Efficiency'] = model.intercept_ + model.coef_[0]*SolarData_Day['Direct_Energy_Tot'] + model.coef_[1]*SolarData_Day['Diffuse_Energy_Tot']
#Get Sidewall_Interfacial_fit_Efficiency from linear regression learning
#%%Linear Regression Machine Learning of Direct Energy Total, Diffuse Energy Total, and Foam_Bottom_Interfacial Global Efficiency
SolarData_Day_full = SolarData_Day #Save SolarData_Day_full for future use
SolarData_Day = SolarData_Day.dropna() #Drop nan
Solar_feature_set_Dataframe = SolarData_Day[['Direct_Energy_Tot','Diffuse_Energy_Tot']]
Solar_feature_set = [] #Set list

for values in Solar_feature_set_Dataframe:
    Solar_feature_set = Solar_feature_set_Dataframe.values.tolist()
    Solar_feature_set.append(Solar_feature_set) #Dataframe to list

Solar_feature_set.pop() #Delete the last element of a list
Solar_target_set = SolarData_Day['Foam_Bottom_Interfacial_Global_Efficiency'].values.tolist() #Dataframe to list

model = LinearRegression()
model.fit(Solar_feature_set, Solar_target_set) #Set model for linear regression fit

SolarData_Day = SolarData_Day_full #Recover dataframe including undeleted "nan"
SolarData_Day['Foam_Bottom_Interfacial_fit_Efficiency'] = model.intercept_ + model.coef_[0]*SolarData_Day['Direct_Energy_Tot'] + model.coef_[1]*SolarData_Day['Diffuse_Energy_Tot']
#Get Sidewall_Interfacial_fit_Efficiency from linear regression learning
#%%Plot Global Energy Total vs Energy Use Efficiency (including linear fit efficiency)
plt.figure()
plt.plot(SolarData_Day['Global_Energy_Tot'], SolarData_Day['Stepwise_Bottom_Heating_Global_Efficiency'],'rD', 
         label = 'Stepwise_Bottom_Heating_Global_Efficiency')
plt.plot(SolarData_Day['Global_Energy_Tot'], SolarData_Day['Stepwise_Bottom_Heating_fit_Efficiency'],'r*',
         label = 'Stepwise_Bottom_Heating_fit_Efficiency')
plt.plot(SolarData_Day['Global_Energy_Tot'], SolarData_Day['InvertPyramid_Bottom_Heating_Global_Efficiency'],'bD', 
         label = 'InvertPyramid_Bottom_Heating_Global_Efficiency')
plt.plot(SolarData_Day['Global_Energy_Tot'], SolarData_Day['InvertPyramid_Bottom_Heating_fit_Efficiency'],'b*',
         label = 'InvertPyramid_Bottom_Heating_fit_Efficiency')
plt.plot(SolarData_Day['Global_Energy_Tot'], SolarData_Day['Sidewall_Interfacial_Global_Efficiency'],'cD', 
         label = 'Sidewall_Interfacial_Global_Efficiency')
plt.plot(SolarData_Day['Global_Energy_Tot'], SolarData_Day['Sidewall_Interfacial_fit_Efficiency'],'c*',
         label = 'Sidewall_Interfacial_fit_Efficiency')
plt.plot(SolarData_Day['Global_Energy_Tot'], SolarData_Day['Bottom_Heating_Global_Efficiency'],'gD', 
         label = 'Bottom_Heating_Global_Efficiency')
plt.plot(SolarData_Day['Global_Energy_Tot'], SolarData_Day['Bottom_Heating_fit_Efficiency'],'g*',
         label = 'Bottom_Heatingl_fit_Efficiency')
plt.plot(SolarData_Day['Global_Energy_Tot'], SolarData_Day['Foam_Bottom_Interfacial_Global_Efficiency'],'kD', 
         label = 'Foam_Bottom_Interfacial_Global_Efficiency')
plt.plot(SolarData_Day['Global_Energy_Tot'], SolarData_Day['Foam_Bottom_Interfacial_fit_Efficiency'],'k*',
         label = 'Foam_Bottom_Interfacial_fit_Efficiency')
plt.legend()
plt.title('Global Energy Total vs Energy Use Efficiency')
plt.xlabel('Global Energy Total (KhW/m^2)')
plt.ylabel('Efficiency')
plt.ylim(0,0.7)
plt.show()
#%%
SolarData_Day_Managed = SolarData_Day[SolarData_Day['Global_Energy_Tot'] >= 1]
plt.figure()
plt.plot(SolarData_Day_Managed['Global_Energy_Tot'], SolarData_Day_Managed['Stepwise_Bottom_Heating_Global_Efficiency'],'rD', 
         label = 'Stepwise_Bottom_Heating_Global_Efficiency')
linear_plot.plot_reg(SolarData_Day_Managed['Global_Energy_Tot'].values.tolist(),SolarData_Day_Managed['Stepwise_Bottom_Heating_Global_Efficiency'].values.tolist(),
                     'r-', 'Stepwise_Bottom_Heating_Global_Efficiency')
plt.plot(SolarData_Day_Managed['Global_Energy_Tot'], SolarData_Day_Managed['InvertPyramid_Bottom_Heating_Global_Efficiency'],'bD', 
         label = 'InvertPyramid_Bottom_Heating_Global_Efficiency')
linear_plot.plot_reg(SolarData_Day_Managed['Global_Energy_Tot'].values.tolist(),SolarData_Day_Managed['InvertPyramid_Bottom_Heating_Global_Efficiency'].values.tolist(),
                     'b-', 'InvertPyramid_Bottom_Heating_Global_Efficiency')
plt.plot(SolarData_Day_Managed['Global_Energy_Tot'], SolarData_Day_Managed['Sidewall_Interfacial_Global_Efficiency'],'cD', 
         label = 'Sidewall_Interfacial_Global_Efficiency')
linear_plot.plot_reg(SolarData_Day_Managed['Global_Energy_Tot'].values.tolist(),SolarData_Day_Managed['Sidewall_Interfacial_Global_Efficiency'].values.tolist(),
                     'c-', 'Sidewall_Interfacial_Global_Efficiency')
plt.plot(SolarData_Day_Managed['Global_Energy_Tot'], SolarData_Day_Managed['Bottom_Heating_Global_Efficiency'],'gD', 
         label = 'Bottom_Heating_Global_Efficiency')
linear_plot.plot_reg(SolarData_Day_Managed['Global_Energy_Tot'].values.tolist(),SolarData_Day_Managed['Bottom_Heating_Global_Efficiency'].values.tolist(),
                     'g-', 'Bottom_Heating_Global_Efficiency')
plt.plot(SolarData_Day_Managed['Global_Energy_Tot'], SolarData_Day_Managed['Foam_Bottom_Interfacial_Global_Efficiency'],'kD', 
         label = 'Foam_Bottom_Interfacial_Global_Efficiency')
linear_plot.plot_reg(SolarData_Day_Managed['Global_Energy_Tot'].values.tolist(),SolarData_Day_Managed['Foam_Bottom_Interfacial_Global_Efficiency'].values.tolist(),
                     'k-', 'Foam_Bottom_Interfacial_Global_Efficiency')
plt.legend()
plt.title('Global Energy Total vs Energy Use Efficiency')
plt.xlabel('Global Energy Total (KhW/m^2)')
plt.ylabel('Efficiency')
plt.ylim(0,0.7)
plt.show()
#%%Use plotly to get group bar chart
from plotly.offline import plot
import plotly.graph_objects as go
go.Figure()
fig = go.Figure(data = [go.Bar(name = 'Global Energy Total', x= SolarData_Day['TIMESTAMP'], y= SolarData_Day['Global_Energy_Tot'], marker_color = 'purple'),
                        go.Bar(name = 'Stepwise_Bottom_Heating_Water_Energy', x= SolarWater_Day['TIMESTAMP'], y= SolarWater_Day['Stepwise_Bottom_Heating_Energy_Production'], marker_color = 'red'),
                        go.Bar(name = 'InvertPyramid_Bottom_Heating_Water_Energy', x= SolarWater_Day['TIMESTAMP'], y = SolarWater_Day['InvertPyramid_Bottom_Heating_Energy_Production'], marker_color = 'blue'),
                        go.Bar(name = 'Sidewall_Interfacial_Water_Energy', x= SolarWater_Day['TIMESTAMP'], y= SolarWater_Day['Sidewall_Interfacial_Energy_Production'], marker_color = 'cyan'), 
                        go.Bar(name = 'Bottom_Heating_Water_Energy', x= SolarWater_Day['TIMESTAMP'], y= SolarWater_Day['Bottom_Heating_Energy_Production'], marker_color = 'green'), 
                        go.Bar(name = 'Foam_Bottom_Interfacial_Water_Energy', x= SolarWater_Day['TIMESTAMP'], y= SolarWater_Day['Foam_Bottom_Interfacial_Energy_Production'], marker_color = 'black')])
#Change the bar mode
fig.update_layout(title_text = 'Energy Distribution Summary vs Timestamp', 
                  xaxis_title= 'TIMESTAMP', yaxis_title= 'Energy (KhW/m^2)',
                  barmode= 'group')
plot(fig)