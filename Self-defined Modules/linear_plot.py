# -*- coding: utf-8 -*-
"""
Created on Wed Mar 24 10:20:28 2021

@author: SLS
"""
import matplotlib.pyplot as plt

def linear_plot(A,B):
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    
    ### TODO: 线性拟合计算参数 ###
    df = pd.DataFrame({'A': A, 'B': B})
    df = df.dropna()
    A = df['A'].values.tolist()
    B = df['B'].values.tolist()
    SumXiYi = 0
    SumXi = 0
    SumYi = 0
    SumXi2 = 0
    PointX = []
    PointY = []
    for item in range(len(A)):
        XiYi = A[item] * B[item]
        SumXiYi += XiYi
        SumXi += A[item]
        SumYi += B[item]
        SumXi2 += A[item] * A[item]
        PointX.append(A[item])
        PointY.append(B[item])
    
    
    w = (len(A) * SumXiYi - SumXi * SumYi) / (len(A) * SumXi2 - SumXi * SumXi)
    b = (SumXi2 * SumYi - SumXiYi * SumXi) / (len(A) * SumXi2 - SumXi * SumXi)
    w = round(w,2)
    b = round(b,2)
    
    X = np.array(A)
    Y = w * X + b

    plt.plot(X, Y, color='red')
    plt.scatter(PointX, PointY, color='blue') # 散点图
     # 务必保留此行，设置绘图对象
    
    return # 务必按此顺序返回

def plot_reg(A,B,Description,d):
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np
    
    ### TODO: 线性拟合计算参数 ###
    df = pd.DataFrame({'A': A, 'B': B})
    df = df.dropna()
    A = df['A'].values.tolist()
    B = df['B'].values.tolist()
    SumXiYi = 0
    SumXi = 0
    SumYi = 0
    SumXi2 = 0
    PointX = []
    PointY = []
    for item in range(len(A)):
        XiYi = A[item] * B[item]
        SumXiYi += XiYi
        SumXi += A[item]
        SumYi += B[item]
        SumXi2 += A[item] * A[item]
        PointX.append(A[item])
        PointY.append(B[item])
    
    
    w = (len(A) * SumXiYi - SumXi * SumYi) / (len(A) * SumXi2 - SumXi * SumXi)
    b = (SumXi2 * SumYi - SumXiYi * SumXi) / (len(A) * SumXi2 - SumXi * SumXi)
    w = round(w,2)
    b = round(b,2)
    
    X = np.array(A)
    Y = w * X + b

    plt.plot(X, Y, Description, label = d)
    plt.show()
     # 务必保留此行，设置绘图对象
    
    return # 务必按此顺序返回

if __name__=="__main__":
    
    A = [2,4,6,7,8]
    B = [3,7,6,7,8]
    
    plt.figure()
    linear_plot(A,B)
    
    plt.figure()
    plot_reg(A,B,'r-','test')
    plt.legend()
    
    
