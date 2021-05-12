# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 16:32:18 2021

@author: SLS
"""
#%%Import Needed Packages
import pandas as pd
import datetime
#%%Select Needed Time Frame
df = pd.read_csv('Python Auto Water Production Clean Data-2021-03-29-2021-04-25.csv')
df = df.drop(columns=['Unnamed: 0'])
start_date = datetime.datetime(int(input('please enter the year for start_date: ')),
                               int(input('please enter the month for start_date: ')),
                               int(input('please enter the date for start_date: ')))

end_date = datetime.datetime(int(input('please enter the year for end_date: ')),
                               int(input('please enter the month for end_date: ')),
                               int(input('please enter the date for end_date: ')))
df['DATE'] = pd.to_datetime(df['DATE'])
df = df[(df['DATE'] >= start_date) & (df['DATE'] <= end_date)]
#%%Create csv file
filename = df['DATE'].iat[1].strftime('Selected water production data-%Y-%m-%d') + df['DATE'].iat[-1].strftime('-%Y-%m-%d.csv')
#Define filename
df.to_csv(filename)