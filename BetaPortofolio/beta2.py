from pandas_datareader import data
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.stats.stats import pearsonr
import time

def estimateStockBeta(period,symbol,index):
    stocksDataFromYahoo=data.DataReader([symbol],'yahoo',start=period[0],end=period[1]) 
    stocksDaily=stocksDataFromYahoo['Adj Close']
    logReturnsDaily=stocksDaily.pct_change().apply(lambda x:np.log(1+x))
    indexFuture=data.DataReader(index,'yahoo',start=period[0],end=period[1])
    indexDaily=indexFuture['Adj Close']
    logReturnsIndexDaily=indexDaily.pct_change().apply(lambda x:np.log(1+x))
    myRegressionDataFrame=pd.DataFrame({'R':logReturnsDaily[symbol],'RI':logReturnsIndexDaily})
    y=myRegressionDataFrame['R']
    x=myRegressionDataFrame['RI']
    x=sm.add_constant(x)
    model=sm.OLS(y,x,missing='drop')
    results=model.fit()
    return [symbol,results.params['RI'],stocksDaily,indexDaily,logReturnsDaily,logReturnsIndexDaily]



listOfTickers=['BMY','ABT','JNJ','SNA']
indexBasedFuture='ES=F'
period=['2019/04/01','2021/04/01']
betaVector=[]
for i in range(len(listOfTickers)):
    betaVector.append(estimateStockBeta(period,listOfTickers[i],indexBasedFuture)[1])


print(betaVector)
titlePeriod='-'.join(period)
stocksBetaDataFrame=pd.DataFrame(betaVector,columns=[titlePeriod],index=listOfTickers)        
print(stocksBetaDataFrame)
#stocksBetaDataFrame.to_excel('stocksBeta.xlsx')