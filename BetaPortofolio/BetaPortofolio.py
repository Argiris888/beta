from pandas_datareader import data
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.stats.stats import pearsonr 
from sklearn.metrics import median_absolute_error



#################################### testing set ####################################
sample=[ 'LUMN','T','DIS','HAS','GPC','BBY','F','NKE','HD','CA',\
         'SYY','PEP','APA','XOM','UNM','CINF','ALL','AON','MMC',\
         'AXP','JPM','PKI','BAX','BDX','BMY','ABT','JNJ','SNA',\
         'SWK','PH','EMR','LMT','DE','BA','NTAP','XLNX','ADSK',\
         'ADP','IBM','CSCO','MSFT','APPL','AVY','IFF','SHW',\
         'LIN','AES','EIX','EXC','NEE']
period1=['2000/01/01','2005/01/01']
period2=['2005/01/01','2010/01/01']
period3=['2010/01/01','2015/01/01']
period4=['2015/01/01','2020/01/01']
listOfPeriods=[period1,period2,period3,period4]
titlePeriod=[]
for periods in listOfPeriods:
    period='-'.join(periods)
    titlePeriod.append(period)
index='^GSPC'
sizePortofolio=2
#######################################################################################




stocksBetaDataFrame=pd.read_excel('IndividualsStocksBeta.xlsx',index_col=0)

    
def estimatePortofolioBeta(stocksBetaDataFrame,period,listOfTickers):

   
    betas_list=[]
    for name in listOfTickers:

         betas_list.append(stocksBetaDataFrame.loc[listOfTickers,period])

    portofolio_beta=np.mean(betas_list)
    return portofolio_beta


def combinationsOfPortofolios(stocksBetaDataFrame,period,sizePortofolio):

    sortedBeta=stocksBetaDataFrame[period].sort_values()
    sortedBeta=list(sortedBeta.index)
    i=sizePortofolio
    portofoliosList=[]

    while i<=len(sortedBeta):
        portofoliosList.append(sortedBeta[(i-sizePortofolio):i])
        i=i+sizePortofolio
        
    nStocksPortofolioBeta=[]
    for portofolio in portofoliosList:
    
          nStocksPortofolioBeta.append(estimatePortofolioBeta(stocksBetaDataFrame,period,portofolio))


    meanOfnStocksPortofolioBeta=np.mean(nStocksPortofolioBeta)
    return [meanOfnStocksPortofolioBeta,nStocksPortofolioBeta,sortedBeta]
#print(combinationsOfPortofolios(stocksBetaDataFrame,titlePeriod[0],2))


def correlationCoefficient(stocksBetaDataFrame,period1,period2,sizePortofolio):
    a=combinationsOfPortofolios(stocksBetaDataFrame,period1,sizePortofolio)[1]
    b=combinationsOfPortofolios(stocksBetaDataFrame,period2,sizePortofolio)[1]
    corcoef=pearsonr(a,b)
    return corcoef[0]

#t=correlationCoefficient(stocksBetaDataFrame,titlePeriod[2],titlePeriod[1],sizePortofolio)
#print(t)


def adjustmentPerPeriod(stocksBetaDataFrame,period1,period2):

   
    y=stocksBetaDataFrame[period2]
    x=stocksBetaDataFrame[period1]
    x=sm.add_constant(x)
    model=sm.OLS(y,x,missing='drop')
    results=model.fit()
    return results.params


#print(adjustmentPerPeriod(stocksBetaDataFrame,titlePeriod[0],titlePeriod[1]))


def meanSquareErrors(stocksBetaDataFrame,period0,period1,period2,sizePortofolio):

    estimatedPortofoliosBetaWithoutAdj=combinationsOfPortofolios(stocksBetaDataFrame,period1,sizePortofolio)[1]

    adjustment=adjustmentPerPeriod(stocksBetaDataFrame,period0,period1)
    estimatedPortofoliosBetaWithAdj=adjustment[0] +adjustment[1]*np.array(estimatedPortofoliosBetaWithoutAdj)

    realizedPortofoliosBeta=combinationsOfPortofolios(stocksBetaDataFrame,period2,sizePortofolio)[1]
    A=estimatedPortofoliosBetaWithoutAdj
    B=estimatedPortofoliosBetaWithAdj
    C=realizedPortofoliosBeta

    meanSquareErrorWithoutAdjustment=np.square(np.subtract(A, C)).mean()
    meanSquareErrorWithAdjustment=np.square(np.subtract(B, C)).mean()

    

    return [meanSquareErrorWithoutAdjustment,meanSquareErrorWithAdjustment,estimatedPortofoliosBetaWithoutAdj,estimatedPortofoliosBetaWithAdj,realizedPortofoliosBeta,adjustment]

#print(meanSquareErrors(stocksBetaDataFrame,titlePeriod[0],titlePeriod[1],titlePeriod[2],sizePortofolio))



########################################## Descriptive Statistics Block #######################################################

def descriptiveStatisticsSample(stocksBetaDataFrame):
    meanOfPeriod=[]
    stdvOfPeriod=[]
    percentilesOfPeriod=[]
    for col in stocksBetaDataFrame:
        meanOfPeriod.append(np.mean(stocksBetaDataFrame[col]))
        stdvOfPeriod.append(np.std(stocksBetaDataFrame[col]))
        percentilesOfPeriod.append(np.percentile(stocksBetaDataFrame[col], [10, 25, 50, 75, 90]).tolist())
    return meanOfPeriod,stdvOfPeriod, percentilesOfPeriod

print(f'Οι μέσες τιμές των περιόδων\n {stocksBetaDataFrame.columns.to_list()} είναι\n {descriptiveStatisticsSample(stocksBetaDataFrame)[0]}\n'\
      f'Οι τυπικές αποκλίσεις των περιόδων\n {stocksBetaDataFrame.columns.to_list()} είναι\n {descriptiveStatisticsSample(stocksBetaDataFrame)[1]}\n'\
      f'Τα ποσοστιαία σημεία 10,25,50,75,90 για τις περιόδους\n {stocksBetaDataFrame.columns.to_list()} είναι\n {descriptiveStatisticsSample(stocksBetaDataFrame)[2]}\n\\n\n\n\n' )

####################################################################################################################################


######################################## Correlation Coefficient Data Frame ########################################################

portofolioSizeVector=[1,2,4,7,10,15,20,25]
#correlationArray=np.zeros((len(portofolioSizeVector),len(titlePeriod)-1))

#for row in range(len(portofolioSizeVector)):

#    for column in range(len(titlePeriod)-1):
#        correlation=correlationCoefficient(stocksBetaDataFrame,titlePeriod[column],titlePeriod[column+1],portofolioSizeVector[row])
#        correlationArray[row][column]=correlation
##print(correlationArray)

##### ftiaxnoum ta onomata stis sthles gia to DF
#titlePeriod2=[]
#for i in range(len(titlePeriod)-1):
#    period=' : '.join([titlePeriod[i],titlePeriod[i+1]])
#    titlePeriod2.append(period)

#correlationDataFrame=pd.DataFrame(correlationArray,columns=titlePeriod2,index=portofolioSizeVector)        
#print(f'Ο πίνακας συσχετίσεων μεταξύ των περιόδων είναι\n {correlationDataFrame}\n\n\n')
#correlationDataFrame.to_excel('correlationDataFrame.xlsx')

###############################################################################################################################################



########################################## Adjustment Models OLS between periods ##############################################################
 
for i in range(len(titlePeriod)-2):

      params=adjustmentPerPeriod(stocksBetaDataFrame,titlePeriod[i],titlePeriod[i+1])
      print('THE REGRESSION TENDENCY OF ESTIMATED BETA COEFFICIENTS FOR INDIVUAL SECURITIES BETWEEN '\
      f'{titlePeriod[i]} and {titlePeriod[i+1]} is : \n a={params[0]:4.3f} \n b={params[1]:4.3f}\n\n\n')

################################################################################################################################################

 


##################################################### MeanSquareError DataFrame ################################################################

#portofolioSizeVector=[1,2,3]
meanSquareErrorArray=np.zeros((len(portofolioSizeVector),(len(titlePeriod)-2)*2))
for row in range(len(portofolioSizeVector)):
    column=0
    for i in range(len(titlePeriod)-2):
        meanSquare=meanSquareErrors(stocksBetaDataFrame,titlePeriod[i],titlePeriod[i+1],titlePeriod[i+2],portofolioSizeVector[row])
        meanSquareErrorArray[row][column]=meanSquare[0]
        meanSquareErrorArray[row][column+1]=meanSquare[1]
        column+=2


### ftixnoume dataframe gia meansquare errors ana megethos portofoliou kai ana periodo
  

meanSquareDataFrame=pd.DataFrame( meanSquareErrorArray,columns=2*(titlePeriod[2:]),index=portofolioSizeVector)        
print(f'The mean Square Errors of our estimations are\n {meanSquareDataFrame}\n\n\n')
#meanSquareDataFrame.to_excel('meanSquareError.xlsx')      

##################################################################################################################################################   
 
 


####################### estimated Beta Coefficients DataFrame for portofolios of N securities for each Period ####################################
#sizePortofolio=25
numberOfPortofolios=int(len(stocksBetaDataFrame.index)/sizePortofolio)

portofoliosOfnSecuritiesBetasArray=np.zeros((numberOfPortofolios,len(titlePeriod)))
for i in range(numberOfPortofolios):
    for j in range(len(titlePeriod)):
        portofoliosOfnSecuritiesBetasArray[i][j]=combinationsOfPortofolios(stocksBetaDataFrame,titlePeriod[j],sizePortofolio)[1][i]
rawIndex=numberOfPortofolios+1
portofoliosOfnSecuritiesDF=pd.DataFrame(portofoliosOfnSecuritiesBetasArray,columns=titlePeriod,index=range(1,rawIndex))
#portofoliosOfnSecuritiesDF.to_excel('Betas of Portofolios of N securities.xlsx')
#print(f'Τα Betas για τα portofolia που φτιάχνονται από {sizePortofolio} μετοχές είνα\n {portofoliosOfnSecuritiesDF}\n\n\n')      

