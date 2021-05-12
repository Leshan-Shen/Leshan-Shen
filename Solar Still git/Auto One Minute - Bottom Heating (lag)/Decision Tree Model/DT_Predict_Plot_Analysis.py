# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 15:47:05 2021

@author: SLS
"""

#%%Import Needed Packages
import pandas as pd
import datetime
from plotly.offline import plot
import plotly.graph_objects as go
#%%Program Start time
starttime = datetime.datetime.now()
#long running
#%%Read csv files
Net_Water_Production = pd.read_csv('Net_Water_Production-2021-03-29-2021-04-25.csv',index_col = 0) 
#Read Net_Water_Production.csv file
Auto_Daily_Water_Production = pd.read_csv('Auto_Daily_Water_Production.csv',index_col = 0) 
#Read Auto_Daily_Water_Production.csv file
DT_Predict_Water_Production = pd.read_csv('DT_Predict_Water_Production.csv',index_col = 0) 
#Read Net_Water_Production.csv file
DT_Predict_Daily_Water_Production = pd.read_csv('DT_Predict_Daily_Water_Production.csv',index_col = 0) 
#Read Auto_Daily_Water_Production.csv file
#%%Types to datetime
Net_Water_Production['TIMESTAMP'] = pd.to_datetime(Net_Water_Production['TIMESTAMP'])
#types to datetime
Auto_Daily_Water_Production['TIMESTAMP'] = pd.to_datetime(Auto_Daily_Water_Production['TIMESTAMP'])
#types to datetime
DT_Predict_Water_Production['TIMESTAMP'] = pd.to_datetime(DT_Predict_Water_Production['TIMESTAMP'])
#types to datetime
DT_Predict_Daily_Water_Production['TIMESTAMP'] = pd.to_datetime(DT_Predict_Daily_Water_Production['TIMESTAMP'])
#types to datetime
#%%
ID0_Net_Water_Production = Net_Water_Production[Net_Water_Production['ID'] == 0]
ID2_Net_Water_Production = Net_Water_Production[Net_Water_Production['ID'] == 2]
ID0_Net_Water_Production.index = range(0,len(ID0_Net_Water_Production))
ID2_Net_Water_Production.index = range(0,len(ID2_Net_Water_Production))
#%%
ID0_Auto_Daily_Water_Production = Auto_Daily_Water_Production[Auto_Daily_Water_Production['ID'] == 0]
ID2_Auto_Daily_Water_Production = Auto_Daily_Water_Production[Auto_Daily_Water_Production['ID'] == 2]
ID0_Auto_Daily_Water_Production.index = range(0,len(ID0_Auto_Daily_Water_Production))
ID2_Auto_Daily_Water_Production.index = range(0,len(ID2_Auto_Daily_Water_Production))
#%%
ID0_DT_Predict_Water_Production = DT_Predict_Water_Production[DT_Predict_Water_Production['ID'] == 0]
ID2_DT_Predict_Water_Production = DT_Predict_Water_Production[DT_Predict_Water_Production['ID'] == 2]
ID0_DT_Predict_Water_Production.index = range(0,len(ID0_DT_Predict_Water_Production))
ID2_DT_Predict_Water_Production.index = range(0,len(ID2_DT_Predict_Water_Production))
#%%
ID0_DT_Predict_Daily_Water_Production = DT_Predict_Daily_Water_Production[DT_Predict_Daily_Water_Production['ID'] == 0]
ID2_DT_Predict_Daily_Water_Production = DT_Predict_Daily_Water_Production[DT_Predict_Daily_Water_Production['ID'] == 2]
ID0_DT_Predict_Daily_Water_Production.index = range(0,len(ID0_DT_Predict_Daily_Water_Production))
ID2_DT_Predict_Daily_Water_Production.index = range(0,len(ID2_DT_Predict_Daily_Water_Production))
#%%
fig = go.Figure(data = [go.Scatter(x= ID0_Net_Water_Production['TIMESTAMP'], 
                                   y= ID0_Net_Water_Production['Net_Weight'],
                                   name = 'ID0_Net_Water_Production', mode = 'markers'),
                        go.Scatter(x= ID0_DT_Predict_Water_Production['TIMESTAMP'], 
                                   y= ID0_DT_Predict_Water_Production['Predict_Net_Weight'],
                                   name = 'ID0_DT_Predict_Water_Production', mode = 'markers')])
plot(fig, filename = 'ID0 Real versus Predict dotted.html')
#%%
fig = go.Figure(data = [go.Scatter(x= ID2_Net_Water_Production['TIMESTAMP'], 
                                   y= ID2_Net_Water_Production['Net_Weight'],
                                   name = 'ID2_Net_Water_Production', mode = 'markers'),
                        go.Scatter(x= ID2_DT_Predict_Water_Production['TIMESTAMP'], 
                                   y= ID2_DT_Predict_Water_Production['Predict_Net_Weight'],
                                   name = 'ID2_DT_Predict_Water_Production', mode = 'markers')])
plot(fig, filename = 'ID2 Real versus Predict dotted.html')
#%%
fig = go.Figure(data = [go.Bar(x= ID0_Auto_Daily_Water_Production['TIMESTAMP'], 
                                   y= ID0_Auto_Daily_Water_Production['Water_Production'],
                                   name = 'ID0_Net_Water_Production'),
                        go.Bar(x= ID0_DT_Predict_Daily_Water_Production['TIMESTAMP'], 
                                   y= ID0_DT_Predict_Daily_Water_Production['Water_Production'],
                                   name = 'ID0_DT_Predict_Water_Production')])
fig.update_layout(barmode= 'group')
plot(fig, filename = 'ID0 Daily Real versus Predict Bar.html')
#%%
fig = go.Figure(data = [go.Bar(x= ID2_Auto_Daily_Water_Production['TIMESTAMP'], 
                                   y= ID2_Auto_Daily_Water_Production['Water_Production'],
                                   name = 'ID2_Net_Water_Production'),
                        go.Bar(x= ID2_DT_Predict_Daily_Water_Production['TIMESTAMP'], 
                                   y= ID2_DT_Predict_Daily_Water_Production['Water_Production'],
                                   name = 'ID2_DT_Predict_Water_Production')])
fig.update_layout(barmode= 'group')
plot(fig, filename = 'ID2 Daily Real versus Predict Bar.html')
#%%Program endding time
endtime = datetime.datetime.now()
print("该程序运行完成需要时间:", endtime-starttime)