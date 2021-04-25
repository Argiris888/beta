from pandas_datareader import data
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.stats.stats import pearsonr




################# synarthsh upologismou beta mias periodou mias metoxhs, apo times kleisimatos ana mhna ########################


def estimateStockBeta(period,symbol,index):

    stocksDataFromYahoo=data.DataReader(symbol,'yahoo',start=period[0],end=period[1])
    stocksMonthly=stocksDataFromYahoo.resample('M').last() 
    stocksMonthly=stocksMonthly['Adj Close']
    logReturnsMonthly=stocksMonthly.pct_change().apply(lambda x:np.log(1+x))
    logReturnsMonthly=logReturnsMonthly.to_list()
    marketIndex=data.DataReader(index,'yahoo',start=period[0],end=period[1])
    marketIndexMonthly=marketIndex.resample('M').last()
    marketIndexMonthly=marketIndexMonthly['Adj Close']
    logReturnsIndexMonthly=marketIndexMonthly.pct_change().apply(lambda x:np.log(1+x)).to_list()
    #myRegressionDataFrame=pd.DataFrame({'R':logReturnsMonthly[symbol],'RM':logReturnsIndexMonthly})
    #y,x=logReturnsMonthly,logReturnsIndexMonthly
    #x=sm.add_constant(x)
    #model=sm.OLS(y,x,missing='drop')
    #results=model.fit()
    return [symbol, logReturnsMonthly,logReturnsIndexMonthly]#results.params[1]]#,stocksMonthly,logReturnsMonthly,stocksMonthly.pct_change()]




###########################################################################################################################################################


################### ftiaxnontas dataframe kai to apothikeuoume se excel me ta betas olwn town metoxwn olwn twn periodwn ###################################

#### ta dedomena mou
#nan=['LUMN','CA']
sample=['LUMN','CA','T','DIS','HAS','GPC','BBY','F','NKE','HD',\
         'SYY','PEP','APA','XOM','UNM','CINF','ALL','AON','MMC',\
         'AXP','JPM','PKI','BAX','BDX','BMY','ABT','JNJ','SNA',\
         'SWK','PH','EMR','LMT','DE','BA','NTAP','XLNX','ADSK',\
         'ADP','IBM','CSCO','MSFT','AAPL','AVY','IFF','SHW',\
         'LIN','AES','EIX','EXC','NEE']
index='^GSPC'
#period1=['2000/01/01','2005/01/01']
#period2=['2005/01/01','2010/01/01']
#period3=['2010/01/01','2015/01/01']
period4=['2015/01/01','2020/01/01']
#listOfPeriods=[period1,period2,period3,period4]

# gia na ftiaksw enwmenes periodous 
#titlePeriod=[]
#for periods in listOfPeriods:
#    period='-'.join(periods)
#    titlePeriod.append(period)
#listOfTickers=sample
#sizePortofolio=2
#stockBetaVector=np.zeros((len(listOfTickers),len(listOfPeriods)))
#for row in range(len(listOfTickers)):

#    for column in range(len(listOfPeriods)):
#        stocksBeta=estimateStockBeta(listOfPeriods[column],listOfTickers[row],index)[3]
#        stockBetaVector[row][column]=stocksBeta
#print(stockBetaVector)
###### ftiaxnoume ta onomata stis sthles
#titlePeriod=[]
#for periods in listOfPeriods:
#    period='-'.join(periods)
#    titlePeriod.append(period)


#stocksBetaDataFrame=pd.DataFrame(stockBetaVector,columns=titlePeriod,index=listOfTickers)        
#print(stocksBetaDataFrame)
#stocksBetaDataFrame.to_excel('individualsStocksBeta.xlsx')

#stocksBetaDataFrame=pd.read_excel('individualsStocksBeta.xlsx',index_col=0)
###################################################################################################################################

#print(type(estimateStockBeta(period1,'LUMN',index)[2]))
#print(estimateStockBeta(period2,'SNA',index))
#print(estimateStockBeta(period1,'LUMN',index))
#b=estimateStockBeta(period2,'SNA',index)[1]
#print(b)
stocksReturns=[]
for i in range(len(sample)):
    stocksReturns.append(estimateStockBeta(period4,sample[i],index)[1])
    stocksReturns[i]=pd.DataFrame(stocksReturns[i])
    #print(estimateStockBeta(period4,sample[i],index)[1])
print(stocksReturns)


