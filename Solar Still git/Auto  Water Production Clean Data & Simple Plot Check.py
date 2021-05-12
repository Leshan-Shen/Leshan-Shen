# -*- coding: utf-8 -*-
"""
Created on Fri May  7 13:34:06 2021

@author: 94749
"""

#%%Import needed packages
import pandas as pd
import numpy as np
import datetime
from dfply import *
from plotly.offline import plot
import plotly.graph_objects as go
#%%Record Start TIME for timing purpose
startTIME = datetime.datetime.now()
#long running
#%%Define multiple_dat_read function
def multiple_dat_read(*filenames):
    import pandas as pd
    df = pd.DataFrame()
    for items in filenames:
        df1 = pd.read_table(items,header=None)
        df = df.append(df1,ignore_index = True)
    return df
#%%Define Net_Weight_Swap function
def Net_Weight_Swap(weight):
    x = weight - weight[0]
    threshold = 50
    for a in range(1,len(weight)):
        if abs(weight[a]-weight[a-1]) >= threshold:
            x[a:len(weight)] = x[a:len(weight)] - weight[a] + weight[a-1]
    return x
#%%Transfer original data to cleaned data, ID0, Stepwise Bottom Heating SS 
Balance0 = multiple_dat_read('COM4-2021-03290850-04120940.DAT',
                             'COM4-2021-04140911-04251158.DAT'
                             ) #Read dat files
Balance_data0 = [Balance0.iat[0,0], Balance0.iat[1,0], Balance0.iat[2,0], 
                 Balance0.iat[3,0], Balance0.iat[4,0]] #Make a series of 5 elements
Balance_data0 = np.mat(Balance_data0) #Transfer series to matrix
for i in range(1,int(len(Balance0[0])/5)):
    Balance_data0_1 = [Balance0.iat[5*(i),0], Balance0.iat[5*(i)+1,0], Balance0.iat[5*(i)+2,0], 
                       Balance0.iat[5*(i)+3,0], Balance0.iat[5*(i)+4,0]]
    Balance_data0_1 = np.mat(Balance_data0_1)                         
    Balance_data0 = np.row_stack((Balance_data0, Balance_data0_1)) #Append matrix
Balance_data0 = pd.DataFrame(Balance_data0, columns=(['ID','DATE','TIME','TEMP','WT']),dtype=np.str)
#Make a dataframe from a matrix, define types as string
Balance_data0 = Balance_data0.dropna() #Drop nan values
Balance_data0['ID'] = Balance_data0.ID.str.extract('(\d+)')
Balance_data0['DATE'] = Balance_data0.DATE.str.extract('(\d+\-\d+\-\d+)')
Balance_data0['TIME'] = Balance_data0.TIME.str.extract('(\d+\-\d+\-\d+)')
Balance_data0['TEMP'] = Balance_data0.TEMP.str.extract('(\d+\.\d+)')
Balance_data0['WT'] = Balance_data0.WT.str.extract('(\-{0,1}\d+\.\d+)')
Balance_data0['WT'] = pd.to_numeric(Balance_data0['WT'])
Balance_data0 = Balance_data0.dropna() #Drop nan values
Balance_data0.index = range(0,len(Balance_data0)) #Recount the index after dropna
Balance_data0['DATE'] = pd.to_datetime(str('20') + Balance_data0['DATE']) #Change Balance_data0['DATE'] type to datetime
Balance_data0['WT'] = Net_Weight_Swap(Balance_data0['WT']) #Apply Net_Weight_Swap function
#%%Transfer original data to cleaned data, ID2, InvertPyramid Bottom Heating SS
Balance2 = multiple_dat_read('COM5-2021-03290851-04120941.DAT',
                             'COM5-2021-04140912-04251158.DAT'
                             ) #Read dat files
Balance_data2 = [Balance2.iat[0,0], Balance2.iat[1,0], Balance2.iat[2,0], 
                 Balance2.iat[3,0], Balance2.iat[4,0]] #Make a series of 5 elements
Balance_data2 = np.mat(Balance_data2) #Transfer series to matrix
for i in range(1,int(len(Balance2[0])/5)):
    Balance_data2_1 = [Balance2.iat[5*(i),0], Balance2.iat[5*(i)+1,0], Balance2.iat[5*(i)+2,0],
                       Balance2.iat[5*(i)+3,0], Balance2.iat[5*(i)+4,0]]
    Balance_data2_1 = np.mat(Balance_data2_1)                         
    Balance_data2 = np.row_stack((Balance_data2, Balance_data2_1)) #Append matrix
Balance_data2 = pd.DataFrame(Balance_data2, columns=(['ID','DATE','TIME','TEMP','WT']),dtype=np.str)
#Make a dataframe from a matrix, define types as string
Balance_data2 = Balance_data2.dropna() #Drop nan values
Balance_data2['ID'] = Balance_data2.ID.str.extract('(\d+)')
Balance_data2['DATE'] = Balance_data2.DATE.str.extract('(\d+\-\d+\-\d+)')
Balance_data2['TIME'] = Balance_data2.TIME.str.extract('(\d+\-\d+\-\d+)')
Balance_data2['TEMP'] = Balance_data2.TEMP.str.extract('(\d+\.\d+)')
Balance_data2['WT'] = Balance_data2.WT.str.extract('(\-{0,1}\d+\.\d+)')
Balance_data2['WT'] = pd.to_numeric(Balance_data2['WT'])
Balance_data2 = Balance_data2.dropna() #Drop nan values
Balance_data2.index = range(0,len(Balance_data2)) #Recount the index after dropna
Balance_data2['DATE'] = pd.to_datetime(str('20') + Balance_data2['DATE']) #Change Balance_data2['DATE'] type to datetime
Balance_data2['WT'] = Net_Weight_Swap(Balance_data2['WT']) #Apply Net_Weight_Swap function
#%%Combine all SS data together and manipulate
Balance_data = Balance_data0.append(Balance_data2,ignore_index = True)
Balance_data['DATE'] = Balance_data['DATE'].dt.strftime('%Y-%m-%d')
Balance_data['TIMESTAMP'] = Balance_data['DATE'] + str('-') + Balance_data['TIME'] 
Balance_data['TIMESTAMP'] = pd.to_datetime(Balance_data['TIMESTAMP'],format = ('%Y-%m-%d-%H-%M-%S'))
Balance_data >>= group_by(X.ID,X.DATE) >> mutate(Weight = X.WT-X.WT[0]) >> ungroup()
#Use group by to start weight count as 0 every day
#%%Save dataframe to csv file
filename = Balance_data['TIMESTAMP'].iat[0].strftime('Python Auto Water Production Clean Data-%Y-%m-%d') + Balance_data['TIMESTAMP'].iat[-1].strftime('-%Y-%m-%d.csv')
#define filename
Balance_data.to_csv(filename)
#%%Manipulate dataframe for a simple analysis plot
Balance_data['ID'] = pd.to_numeric(Balance_data['ID'])
ID0_Clean_Data = Balance_data[Balance_data['ID'] == 0]
ID2_Clean_Data = Balance_data[Balance_data['ID'] == 2]
ID0_Clean_Data.index = range(0,len(ID0_Clean_Data))
ID2_Clean_Data.index = range(0,len(ID2_Clean_Data))
#Seperate ID0 & ID2
#%%Plot 'Simple Plot of Water Production
fig = go.Figure(data = [go.Scatter(x = ID0_Clean_Data['TIMESTAMP'],
                                   y = ID0_Clean_Data['Weight'],
                                   name = 'SBH'),
                        go.Scatter(x = ID2_Clean_Data['TIMESTAMP'],
                                   y = ID2_Clean_Data['Weight'],
                                   name = 'IPBH')])
plot(fig, filename = 'Simple Plot of Water Production.html')
#%%Collect program running TIME
endTIME = datetime.datetime.now()
print("该程序运行完成需要时间:", endTIME-startTIME)