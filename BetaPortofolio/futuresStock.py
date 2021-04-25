from pandas_datareader import data
import numpy as np
import pandas as pd
import statsmodels.api as sm
import time
import matplotlib.pyplot as plt

def estimateStockBeta(period,symbol,index):
    stocksDataFromYahoo=data.DataReader(symbol,'yahoo',start=period[0],end=period[1]) 
    stocksDaily=stocksDataFromYahoo['Adj Close']
    logReturnsDaily=stocksDaily.pct_change().apply(lambda x:np.log(1+x))
    indexFuture=data.DataReader(index,'yahoo',start=period[0],end=period[1])
    indexDaily=indexFuture['Adj Close']
    logReturnsIndexDaily=indexDaily.pct_change().apply(lambda x:np.log(1+x))
    ############################# Regresion ######################################################
    betaVector=[]
    for stock in symbol:
        myRegressionDataFrame=pd.DataFrame({'R':logReturnsDaily[stock],'RI':logReturnsIndexDaily})
        y=myRegressionDataFrame['R']
        x=myRegressionDataFrame['RI']
        x=sm.add_constant(x)
        model=sm.OLS(y,x,missing='drop')
        results=model.fit()
        betaVector.append(results.params['RI'])    ### list with the betas of the stocks

    ################################## creating excel for time saving ###########################################
    #logReturnsDaily['portfolioReturns']=logReturnsDaily[list(logReturnsDaily.columns.values)].mean(axis=1)  # an xrhsimopoiousa isa varh
    indexDaily.to_excel('index_Prices.xlsx')
    logReturnsIndexDaily.rename('indexReturns')
    logReturnsIndexDaily.to_excel('index_Returns.xlsx')
    logReturnsDaily.to_excel('my_Data_Returns.xlsx')
    stocksDaily.to_excel('my_Stocks_Prices.xlsx')

    titlePeriod='-'.join(period)
    stocksBetaDataFrame=pd.DataFrame(betaVector,columns=[titlePeriod],index=listOfTickers)
    stocksBetaDataFrame.to_excel('my_Stocks_Beta.xlsx')
    ###############################################################################################################
    return [symbol,betaVector,stocksDaily,indexDaily,logReturnsDaily,logReturnsIndexDaily]



listOfTickers=['BAC','NVDA','JNJ','AAPL']
indexBasedFuture='ES=F'
period=['2019/04/01','2021/04/01']


myData=estimateStockBeta(period,listOfTickers,indexBasedFuture)
