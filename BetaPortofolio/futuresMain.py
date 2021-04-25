from pandas_datareader import data
import numpy as np
import pandas as pd
import statsmodels.api as sm
import time
import matplotlib.pyplot as plt



######################################## Data Used ####################################################################
period=['2019/04/01','2021/04/01']
listOfTickers=[	'BAC','NVDA','JNJ','AAPL']
weightsVector=[0.15,0.15,0.35,0.35]
weightsVector=np.array(weightsVector)
indexBasedFuture='ES=F'


stocksBetaDataFrame=pd.read_excel('my_Stocks_Beta.xlsx',index_col=0)
indexReturns=pd.read_excel('index_returns.xlsx',index_col=0)
stockPrices=pd.read_excel('my_Stocks_Prices.xlsx',index_col=0)
stocksReturns=pd.read_excel('my_Data_Returns.xlsx',index_col=0)
#print(stocksBetaDataFrame.head(),indexReturns.head(),stockPrices.head(),stocksReturns.head())

#########################################################################################################################



####################################### calculating Portfolio's returns ##################################################
arrayReturns=stocksReturns.to_numpy()
weightsArray=np.tile(weightsVector,(arrayReturns.shape[0],1))
weightedReturns=np.multiply(weightsArray,arrayReturns)
portfolioReturns=np.sum(weightedReturns,axis=1)
portfolioReturnsDF=pd.DataFrame(portfolioReturns,columns=['Portofolio'],index=stocksReturns.index)


###################################### Plots ##############################################################################

stockPrices.plot()
plt.legend(loc='best')

portfolioReturnsDF.plot()
plt.show()

###########################################################################################################################



###################################### Descriptive Statistics of Portofolio Returns #######################################
describe=portfolioReturnsDF.describe()
print(describe)

skew=portfolioReturnsDF.skew()
kurt=portfolioReturnsDF.kurt()
print(f'\n\n\nThe skewness of the portofolio returnss is {list(skew)}, and the kurtosis is {list(kurt)}\n\n\n')
############################################################################################################################



##################################### Calculating Portfolio's Beta #########################################################
arrayBeta=stocksBetaDataFrame.to_numpy()
weightedBetaVector=np.multiply(weightsVector.reshape(-1,1),arrayBeta)
portfolioBeta=np.sum(weightedBetaVector)
print(f'The beta of our portofolio during the period {list(stocksBetaDataFrame.columns)} is b: {portfolioBeta}\n\n\n')
#############################################################################################################################



###################################### Calculating the Νumber of  E-Mini S&P 500 Jun 2021 Futures needed ######################

capital=2*10**6
StocksPrice=data.DataReader(listOfTickers,'yahoo',start='2021/04/05',end='2021/04/05') 
StocksPrice=np.transpose(StocksPrice['Adj Close'].to_numpy())
print(f'The adjusted closed prices of the stocks in portfolio are \n{StocksPrice}\n\n\n')
capitalPerStock=weightsVector.reshape(-1,1)*capital
print(f'The capital we are going to use in each stock is \n{capitalPerStock}\n\n\n')
numberOfStocks=np.trunc(np.divide(capitalPerStock,StocksPrice))
print(f'The number of shares we are going to purchase in each stock is \n{numberOfStocks}\n\n\n')
totalUsed=np.sum(np.multiply(numberOfStocks,StocksPrice))
notInUse=capital-totalUsed
print(f'From the initial capital of {capital} euros, we use {totalUsed:15.5f} euros and we still have {notInUse:15.5f} euros available,'\
      f'so the difference is very small and we continue with the initial amount and the same weights\n\n\n\n')

indexFuture=data.DataReader(indexBasedFuture,'yahoo',start='2021/04/06',end='2021/04/06')
indexFuture=indexFuture['Adj Close'].to_numpy()
print(f'\n\n The adjusted closed price of the future is {indexFuture}\n\n')
#print(StocksPrice)
multiplier=50
N=portfolioBeta*(capital/(indexFuture*multiplier))
print(f'The number of futures we are going to buy for the long hedging of the portfolio, is N:{int(np.round(N))},\n the float number of futures needed is {N}'\
      f'so there is over-hedged\n\n\n')

####################################################################################################################################



