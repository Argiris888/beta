from pandas_datareader import data
import numpy as np
import pandas as pd
import statsmodels.api as sm
import time
import matplotlib.pyplot as plt
import datetime

listOfTickers=['BAC','NVDA','JNJ','AAPL']
indexBasedFuture='ES=F'
period=['2019/04/01','2021/04/01']
weightsVector=[0.15,0.15,0.35,0.35]
weightsVector=np.array(weightsVector)



stocksBetaDataFrame=pd.read_excel('my_Stocks_Beta.xlsx',index_col=0)
indexReturns=pd.read_excel('index_returns.xlsx',index_col=0)
stockPrices=pd.read_excel('my_Stocks_Prices.xlsx',index_col=0)
stocksReturns=pd.read_excel('my_Data_Returns.xlsx',index_col=0)
#print(stocksBetaDataFrame.head(),indexReturns.head(),stockPrices.head(),stocksReturns.head())


arrayReturns=stocksReturns.to_numpy()
weightsArray=np.tile(weightsVector,(arrayReturns.shape[0],1))
weightedReturns=np.multiply(weightsArray,arrayReturns)
portfolioReturns=np.sum(weightedReturns,axis=1)
portfolioReturnsDF=pd.DataFrame(portfolioReturns,columns=['Portofolio'],index=stocksReturns.index)



plt.figure()
stockPrices.plot()
plt.legend(loc='best')
#plt.show()


portfolioReturnsDF.plot()
plt.show()
#plt.show()

describe=portfolioReturnsDF.describe()
print(describe)

skew=portfolioReturnsDF.skew()
kurt=portfolioReturnsDF.kurt()
print(f'\n\n\nThe skewness of the portofolio returnss is {kew}, and the kurtosis is {kurt}\n\n\n')


