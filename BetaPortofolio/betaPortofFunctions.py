
from pandas_datareader import data
import numpy as np
import pandas as pd
import statsmodels.api as sm
from itertools import combinations
import itertools
from scipy.stats.stats import pearsonr 


stocksBetaDataFrame=pd.read_excel('IndividualsStocksBeta.xlsx',index_col=0)

def estimateStockBeta(period,symbol,index):

    stocksDataFromYahoo=data.DataReader(listOfTickers,'yahoo',start=period[0],end=period[1])
    stocksMonthly=stocksDataFromYahoo.resample('M').last() 
    stocksMonthly=stocksMonthly['Adj Close']
    logReturnsMonthly=stocksMonthly.pct_change().apply(lambda x:np.log(1+x))
    #pd.DataFrame(stocksMonthly).to_csv('tickers_Close.csv')
    #print(stocksMonthly)
    marketIndex=data.DataReader(index,'yahoo',start=period[0],end=period[1])
    marketIndexMonthly=marketIndex.resample('M').last()
    marketIndexMonthly=marketIndex['Adj Close']
    logReturnsIndexMonthly=marketIndexMonthly.pct_change().apply(lambda x:np.log(1+x))
    myRegressionDataFrame=pd.DataFrame({'R':logReturnsMonthly[symbol],'RM':logReturnsIndexMonthly})
    y=myRegressionDataFrame['R']
    x=myRegressionDataFrame['RM']
    x=sm.add_constant(x)
    model=sm.OLS(y,x,missing='drop')
    results=model.fit()
    #print(results.summary())
    return [symbol,results.params['RM']]

def estimatePortofolioBeta1(period,listOfTickers,index):

   
    betas_list=[]
    for name in listOfTickers:

         betas_list.append(estimateStockBeta(period,name,index))

    portofolio_beta=np.mean(betas_list)
    return portofolio_beta

def estimatePortofolioBeta(stocksBetaDataFrame,period,listOfTickers):

   
    betas_list=[]
    for name in listOfTickers:

         betas_list.append(stocksBetaDataFrame.loc[listOfTickers,period])

    portofolio_beta=np.mean(betas_list)
    return portofolio_beta



#def combinationsOfPortofolios(period,listOfTickers,index,sizePortofolio):

#    combinations = list(itertools.combinations(listOfTickers, sizePortofolio))
#    uniqueCombinations = set(combinations)
#    uniqueCombinations = [list(elem) for elem in uniqueCombinations]
#    nStocksPortofolioBeta=[]
#    for portofolio in uniqueCombinations:
    
#          nStocksPortofolioBeta.append(estimatePortofolioBeta(period,portofolio,index))


#    meanOfnStocksPortofolioBeta=np.mean(nStocksPortofolioBeta)
#    return [meanOfnStocksPortofolioBeta,nStocksPortofolioBeta]



period1=['2005/01/01','2010/01/01']
period2=['2010/01/01','2015/01/01']
period3=['2015/01/01','2020/01/01']
listOfPeriods=[period1,period2,period3]
titlePeriod=[]
for periods in listOfPeriods:
    period='-'.join(periods)
    titlePeriod.append(period)
listOfTickers=['MO','AEP','BA','BMY']
index='^GSPC'
sizePortofolio=2

#print(estimatePortofolioBeta(period2,listOfTickers,index))
#print(estimatePortofolioBeta(['2015/08/01','2018/01/01'],['MO','AEP','BA','BMY']))
#t=combinationsOfPortofolios(period,listOfTickers,index,sizePortofolio)
#print(t)
def combinationsOfPortofolios(stocksBetaDataFrame,period,listOfTickers,sizePortofolio):
    i=sizePortofolio
    portofoliosList=[]
    while i<=len(listOfTickers):
        portofoliosList.append(listOfTickers[(i-sizePortofolio):i])
        i=i+sizePortofolio
        
    nStocksPortofolioBeta=[]
    for portofolio in portofoliosList:
    
          nStocksPortofolioBeta.append(estimatePortofolioBeta(stocksBetaDataFrame,period,portofolio))


    meanOfnStocksPortofolioBeta=np.mean(nStocksPortofolioBeta)
    return [meanOfnStocksPortofolioBeta,nStocksPortofolioBeta]
#print(combinationsOfPortofolios(stocksBetaDataFrame,titlePeriod[0],listOfTickers,2))

def correlationCoefficient(stocksBetaDataFrame,period1,period2,listOfTickers,sizePortofolio):
    a=combinationsOfPortofolios(stocksBetaDataFrame,period1,listOfTickers,sizePortofolio)[1]
    b=combinationsOfPortofolios(stocksBetaDataFrame,period2,listOfTickers,sizePortofolio)[1]
    corcoef=pearsonr(a,b)
    #corcoef2=np.corrcoef(a,b)
    return corcoef,corcoef2,a,b


t=correlationCoefficient(stocksBetaDataFrame,titlePeriod[2],titlePeriod[1],listOfTickers,sizePortofolio)
print(t)
print(titlePeriod[1])

#def createSortedListOfPeriodsSamplesBetas(period,listOfTickers,index):
 #   sortedList=[]







#logReturnsData=estimateStockBeta

def adjustmentPerPeriod(stocksBetaDataFrame,period1,period2,listOfTickers):

    #stockPeriod1Beta=[]
    #stockPeriod2Beta=[]
    #for symbol in listOfTickers:

    #    stockPeriod1Beta.append(estimateStockBeta(period1,symbol,index))
    #    stockPeriod2Beta.append(estimateStockBeta(period2,symbol,index))

    #myRegressionDataFrame=pd.DataFrame({'beta1':stockPeriod1Beta,'beta2':stockPeriod2Beta})
    y=stocksBetaDataFrame[period2]
    x=stocksBetaDataFrame[period1]
    x=sm.add_constant(x)
    model=sm.OLS(y,x,missing='drop')
    results=model.fit()
    return results.params


#print(adjustmentPerPeriod(stocksBetaDataFrame,titlePeriod[0],titlePeriod[1],listOfTickers))
#print()

def meanSquareErrors(stocksBetaDataFrame,period0,period1,period2,listOfTickers,sizePortofolio):

    estimatedPortofoliosBetaWithoutAdj=combinationsOfPortofolios(stocksBetaDataFrame,period1,listOfTickers,sizePortofolio)[1]

    adjustment=adjustmentPerPeriod(stocksBetaDataFrame,period0,period1,listOfTickers)
    estimatedPortofoliosBetaWithAdj=adjustment[0] +adjustment[1]*np.array(estimatedPortofoliosBetaWithoutAdj)

    realizedPortofoliosBeta=combinationsOfPortofolios(stocksBetaDataFrame,period2,listOfTickers,sizePortofolio)[1]
    A=estimatedPortofoliosBetaWithoutAdj
    B=estimatedPortofoliosBetaWithAdj
    C=realizedPortofoliosBeta

    meanSquareErrorWithoutAdjustment=np.square(np.subtract(A, C)).mean()
    meanSquareErrorWithAdjustment=np.square(np.subtract(B, C)).mean()

    #information_array=np.array([])

    return [meanSquareErrorWithoutAdjustment,meanSquareErrorWithAdjustment,estimatedPortofoliosBetaWithoutAdj,estimatedPortofoliosBetaWithAdj,realizedPortofoliosBeta,adjustment]

#print(meanSquareErrors(stocksBetaDataFrame,titlePeriod[0],titlePeriod[1],titlePeriod[2],listOfTickers,sizePortofolio))
#print(estimateStockBeta(period1,'MO',index))


# ftiaxnontas dataframe me ta betas olwn town metoxwn olwn twn periodwn

#stockBetaVector=np.zeros((len(listOfTickers),len(listOfPeriods)))
#for raw in range(len(listOfTickers)):


#    for column in range(len(listOfPeriods)):
#        stocksBeta=estimateStockBeta(listOfPeriods[column],listOfTickers[raw],index)[1]
#        stockBetaVector[raw][column]=stocksBeta

# ftiaxnoum ta onomata stis sthles
#titlePeriod=[]
#for periods in listOfPeriods:
#    period='-'.join(periods)
#    titlePeriod.append(period)




#stocksBetaDataFrame=pd.DataFrame(stockBetaVector,columns=titlePeriod,index=listOfTickers)        
#print(stocksBetaDataFrame)
#stocksBetaDataFrame.to_excel('IndividualsStocksBeta.xlsx')


#stocksBetaDataFrame=pd.read_excel('IndividualsStocksBeta.xlsx',index_col=0)
#print(estimatePortofolioBeta(stocksBetaDataFrame,titlePeriod[0],listOfTickers))
#print(stocksBetaDataFrame.loc['MO',:])