# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 15:02:16 2021

@author: SLS
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import packages

data = pd.read_csv('D:\R\CO2\CO2-1.csv', names = ['Time','P_out'])
#read csv file

data['c_CO2'] = (15-data['P_out'])/100*4*1000/22.4/3600/30
data['Conv'] = 2*np.cumsum(data['c_CO2'])/2
#manipulate dataframe from csv

plt.figure()
x = data['Time']
y = data['Conv']
plt.plot(x, y, label ='Conv', color='purple')
plt.legend()
plt.title('Time vs Conv')
plt.xlabel('Time')
plt.ylabel('Conv')
plt.show()

plt.figure()
x = data['P_out']
y = data['Conv']
plt.plot(x, y, label ='Conv', color='green')
plt.legend()
plt.title('P_out vs Conv')
plt.xlabel('P_out')
plt.ylabel('Conv')
plt.show()
#plotting
