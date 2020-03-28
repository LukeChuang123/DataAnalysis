# from sklearn.cross_validation import cross_val_score
import pandas as pd
from sklearn import datasets
from sklearn.linear_model import LinearRegression
# from sklearn.cross_validation import train_test_split
from sklearn import metrics
import numpy as np
import math

import datetime

from  Regression import Regression
   
analysis_data = pd.read_excel("時間序列分析資料.xlsx")
analysis_data.drop("Unnamed: 0",axis=1,inplace=True)
# analysis_data.set_index("DATE",drop=False,inplace=True)
print(analysis_data)

#設定x,y
x = analysis_data.iloc[:,3:]
y = analysis_data["BOX_OFFICE"]

#設定train,test data
split_date = datetime.datetime.strptime("2019-03-23", "%Y-%m-%d")
split_index = analysis_data[analysis_data.DATE == split_date].index.tolist()[0]
print("split_index:",split_index)

x_train = x.iloc[0:split_index,:] 
x_test = x.iloc[split_index:,:]
y_train = y.iloc[0:split_index]
y_test = y.iloc[split_index:]

x_num = x.shape[1]

#------------------------------------------------
reg = Regression(x_train,y_train,x_test,y_test)
reg.lasso_reg(47,10e3)
print()
reg.raw_reg()
input("continue")

#---------------------------------------------
#一次式
reg = LinearRegression().fit(x_train, y_train)

print("Intercept:",reg.intercept_)
print("Coffient:",reg.coef_,"\n")
for var,coef in zip(x_train,reg.coef_): 
    print(var+":",coef)

y_pred = reg.predict(x_test)

mean_squared_error = metrics.mean_squared_error(y_test,y_pred)

print("Result:")
print("R^2 for train data:",reg.score(x_train, y_train))
print("R^2 for test data:",reg.score(x_test, y_test))
print("Mean squared error:",mean_squared_error)
print("Average error:",math.sqrt(mean_squared_error))
print("Average box-office:",y_test.mean())
input("continue")

#----------------------------------------------------------
#Gradient Descent
#initialize parameters
paras = np.random.randint( low = -100,high = 100, size = 1+x_num) #1個bias+x_num個變數
lr = 0.001 #learning-rate
iteration = 10

#store values of parameters 
paras_history = [paras]

#iterations
for i in range(iteration):

    para_grads = np.zeros(1+x_num,dtype=float) #1個bias+x_num個變數
    for n in range(x_train.shape[0]):
        x_vector = np.append([1],x_train.iloc[n,:].to_numpy())
        # input("continue")
        #算bias的偏微分
        para_grads[0] = para_grads[0]+2.0*(y_train[n]-paras.dot(x_vector))*(-1.0)
        print("bias_grad",para_grads[0])
        #算各變數係數的偏微分
        for var in range(x_num):
            para_grads[var+1] = para_grads[var+1]+2.0*(y_train[n]-paras.dot(x_vector))*(-x_train.iloc[n,var])
            print("weight"+str(var+1)+"_grad:",para_grads[var+1])

    #更新參數
    paras = paras - lr*para_grads

    #將更新後參數存到paras_history
    paras_history.append(paras)
    
    print("finish an iteration",str(i)+"/"+str(iteration))
    # input("continue")

#最終的參數
final_paras = paras_history[-1]
bias = final_paras[0]
coefs = final_paras[1:] 
for var,coef in zip(x_train,coefs):
    print(var+":",coef)

#算出預測的y
y_pred = []
for n in range(x_test.shape[0]):
    print(n + split_index)
    x_vector = np.append([1],x_test.iloc[n + split_index,:].to_numpy())
    y = final_paras.dot(x)
    y_pred.append(y)

mean_squared_error = metrics.mean_squared_error(y_test,y_pred)

print("Result:")
# print("R^2 for train data:",reg.score(x_train, y_train))
# print("R^2 for test data:",reg.score(x_test, y_test))
print("Mean squared error:",mean_squared_error)
print("Average error:",math.sqrt(mean_squared_error))
print("Average box-office:",y_test.mean())
input("continue")






