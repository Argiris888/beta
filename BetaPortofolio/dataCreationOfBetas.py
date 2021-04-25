from pandas_datareader import data
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.stats.stats import pearsonr
import time



################# synarthsh upologismou beta mias periodou mias metoxhs, apo times kleisimatos ana mhna ########################


def estimateStockBeta(period,symbol,index):
    t1=time.time()
    stocksDataFromYahoo=data.DataReader([symbol],'yahoo',start=period[0],end=period[1])
    stocksMonthly=stocksDataFromYahoo.resample('M').last() 
    stocksMonthly=stocksMonthly['Adj Close']
    logReturnsMonthly=stocksMonthly.pct_change().apply(lambda x:np.log(1+x))
    marketIndex=data.DataReader(index,'yahoo',start=period[0],end=period[1])
    marketIndexMonthly=marketIndex.resample('M').last()
    marketIndexMonthly=marketIndexMonthly['Adj Close']
    logReturnsIndexMonthly=marketIndexMonthly.pct_change().apply(lambda x:np.log(1+x))
    t2=time.time()
    print(f'prwto meros {t2-t1}')
    t1=time.time()
    myRegressionDataFrame=pd.DataFrame({'R':logReturnsMonthly[symbol],'RM':logReturnsIndexMonthly})
    y=myRegressionDataFrame['R']
    x=myRegressionDataFrame['RM']
    x=sm.add_constant(x)
    model=sm.OLS(y,x,missing='drop')
    results=model.fit()
    t2=time.time()
    print('2o meros einai',t2-t1)
    return [symbol,results.params['RM'],logReturnsMonthly,logReturnsIndexMonthly]




###########################################################################################################################################################


################### ftiaxnontas dataframe kai to apothikeuoume se excel me ta betas olwn town metoxwn olwn twn periodwn ###################################
#%%
#### ta dedomena mou
#nan=['LUMN','CA']
sample=[ 'LUMN','T','DIS','HAS','GPC','BBY','F','NKE','HD','CA',\
         'SYY','PEP','APA','XOM','UNM','CINF','ALL','AON','MMC',\
         'AXP','JPM','PKI','BAX','BDX','BMY','ABT','JNJ','SNA',\
         'SWK','PH','EMR','LMT','DE','BA','NTAP','XLNX','ADSK',\
         'ADP','IBM','CSCO','MSFT','APPL','AVY','IFF','SHW',\
         'LIN','AES','EIX','EXC','NEE']
index='^GSPC'
period1=['2000/01/01','2005/01/01']
period2=['2005/01/01','2010/01/01']
period3=['2010/01/01','2015/01/01']
period4=['2018/01/01','2020/01/01']
listOfPeriods=[period1,period2,period3,period4]

# gia na ftiaksw enwmenes periodous 
titlePeriod=[]
for periods in listOfPeriods:
    period='-'.join(periods)
    titlePeriod.append(period)
listOfTickers=sample
sizePortofolio=2
stockBetaVector=np.zeros((len(listOfTickers),len(listOfPeriods)))
for row in range(len(listOfTickers)):

    for column in range(len(listOfPeriods)):
        t1=time.time()
        stocksBeta=estimateStockBeta(listOfPeriods[column],listOfTickers[row],index)[1]
        stockBetaVector[row][column]=stocksBeta
        t2=time.time()
        print(t2-t1)
        break
    break
print(stockBetaVector)
###### ftiaxnoume ta onomata stis sthles
titlePeriod=[]
for periods in listOfPeriods:
    period='-'.join(periods)
    titlePeriod.append(period)


stocksBetaDataFrame=pd.DataFrame(stockBetaVector,columns=titlePeriod,index=listOfTickers)        
print(stocksBetaDataFrame)
#stocksBetaDataFrame.to_excel('individualsStocksBeta.xlsx')

#stocksBetaDataFrame=pd.read_excel('individualsStocksBeta.xlsx',index_col=0)
###################################################################################################################################

#print(estimateStockBeta(period2,'SNA',index)[2])
#print(estimateStockBeta(period2,'SNA',index)[3])

#for i in range(len(sample)):
#    print(sample[i],estimateStockBeta(period4,sample[i],index)[2])
