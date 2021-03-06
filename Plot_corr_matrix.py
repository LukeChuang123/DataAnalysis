import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from sklearn import preprocessing

# def find_low_corr_col(corr_matrix):

def plot_corr_matrix(df):
    dfData = df.corr()
    print(dfData)
    plt.subplots(figsize=(50, 50)) # 設定畫面大小
    sns.heatmap(dfData, annot=False, vmax=1, square=True, cmap="Blues")
    plt.savefig('相關係數矩陣.png')
    plt.show()

#讀進分析資料
analysis_data = pd.read_excel("時間序列分析資料.xlsx")
analysis_data.drop("Unnamed: 0",axis=1,inplace=True)

#找相關係數
x = analysis_data.iloc[:,3:]
y = analysis_data["BOX_OFFICE"] 

# num_corr_matrix = x.corr()#x變數間的相關
# plot_corr_matrix(x)

corr_list = []
col_list = x.columns
x_list = []
for i in range(x.shape[1]):
    corr = x.iloc[:,i].corr(y)
    #如果相關係數等於nan不要記錄起來
    if (np.isnan(corr)):
        print("this is nan:")
        print(x.columns[i])
        analysis_data.drop(x.columns[i],axis=1,inplace=True)
        continue
    if(corr > 0.2 or corr < -0.2):
        print(col_list[i]+':',corr)
        x_list.append(col_list[i])   
        corr_list.append(corr)
    else:
        continue
# print(corr_list)

#畫出描述各變數與票房關係的長條圖
# plot_x = list(analysis_data.iloc[:,3:].columns)
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False
plt.bar(x_list,corr_list,width=0.5)
plt.grid(axis='y')
plt.savefig('重要變數與票房相關係數.png')
plt.axhline(y=0,color="black")
plt.show()


#將刪掉與y相關係數為nan的變數欄位後的新資料表格存起來
analysis_data.to_excel("時間序列分析資料.xlsx")
# print(num_corr_matrix)
print("畫好相關係數矩陣了!")