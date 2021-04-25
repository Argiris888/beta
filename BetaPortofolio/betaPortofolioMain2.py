from pandas_datareader import data
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.stats.stats import pearsonr 
import  yahoo_finance 


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
sizePortofolio=10
#######################################################################################




stocksBetaDataFrame=pd.read_excel('IndividualsStocksBeta.xlsx',index_col=0)

    
def estimatePortofolioBeta(stocksBetaDataFrame,period,listOfTickers): ### ypologizoume to beta enos portofoliou, gia mia periodo

   
    betas_list=[]

    ### euresh apo dataframe tou beta twn metoxwn pou thelw
    for name in listOfTickers:

         betas_list.append(stocksBetaDataFrame.loc[listOfTickers,period])

    portofolio_beta=np.mean(betas_list)
    return portofolio_beta


def combinationsOfPortofolios(stocksBetaDataFrame,period,sizePortofolio): ###vriskoume olous tous mh epikaluptomenous sunduasmous metoxwn, pou prokuptoun kata auksousa seira, mias periodou

    ### taksinomhsh dataframe ths periodou (series dld) analoga me to beta , kata ayksousa seira
    sortedBeta=stocksBetaDataFrame[period].sort_values()

    ### gia na parw taksinomhmenh lista twn sumvolwn twn metoxwn tou portofoliou mias sugkekrimenhs periodou
    sortedBeta=list(sortedBeta.index)

    i=sizePortofolio
    portofoliosList=[]

    ### me auto ton tropo tha parw olous tous dunatous sunduasmous (portofolia),(ta sumvola mono) N metoxwn , apo mia lista metoxwn, me beta pou auksanei
    while i<=len(sortedBeta):  ### an to i kseperasei to megethos ths listas, mhn sunexiseis me allo sunduasmo
        portofoliosList.append(sortedBeta[(i-sizePortofolio):i])
        i=i+sizePortofolio
    
    ### euresh tou beta gia kathe portofolio pou periexei to portofoliolist 
    nStocksPortofolioBeta=[]
    for portofolio in portofoliosList:
    
          nStocksPortofolioBeta.append(estimatePortofolioBeta(stocksBetaDataFrame,period,portofolio))

    ### mesh timh gia ta beta olwn twn dunatwn portofoliwn pou kataskeuazontai apo N metoxes (size of portofolio)
    meanOfnStocksPortofolioBeta=np.mean(nStocksPortofolioBeta)
    return [meanOfnStocksPortofolioBeta,nStocksPortofolioBeta,portofoliosList]
#print(combinationsOfPortofolios(stocksBetaDataFrame,titlePeriod[2],20))


def correlationCoefficient(stocksBetaDataFrame,period1,period2,sizePortofolio):
    ### apo ta  portofolia pou periexoun N metoxes, theloume twn suntelesth susxetishs twn betas tous metaksu 2 periodwn
    a=combinationsOfPortofolios(stocksBetaDataFrame,period1,sizePortofolio)[1]
    portofolioList=combinationsOfPortofolios(stocksBetaDataFrame,period1,sizePortofolio)[2] 
    b=[]
    for portofolio in portofolioList:
        b.append(estimatePortofolioBeta(stocksBetaDataFrame,period2,portofolio))
    corcoef=pearsonr(a,b)
    return corcoef[0]

t=correlationCoefficient(stocksBetaDataFrame,titlePeriod[0],titlePeriod[1],10)
print(t)


def adjustmentPerPeriod(stocksBetaDataFrame,period1,period2):

    ### ols metaksu twn beta 2 periodown gia oles tis metoxes
    y=stocksBetaDataFrame[period2]
    x=stocksBetaDataFrame[period1]
    x=sm.add_constant(x)
    model=sm.OLS(y,x,missing='drop')
    results=model.fit()
    return results.params


#print(adjustmentPerPeriod(stocksBetaDataFrame,titlePeriod[0],titlePeriod[1]))


def meanSquareErrors(stocksBetaDataFrame,period0,period1,period2,sizePortofolio):
    ### to meso ektimhmeno beta gia ta portofolia N metoxwn pou sthrizetai mono sthn timh tou mesou beta ths prohgoumenhs periodous
    estimatedPortofoliosBetaWithoutAdj=combinationsOfPortofolios(stocksBetaDataFrame,period1,sizePortofolio)[1]

    ### h ektimhsh tou mesa beta me thn prosarmogh tou blume, opou xrhsimopoioume th sxesh metaksu twn beta 2 prohgoumenwn periodwn
    ###, kai thn efarmozoume sthn ektimhsh (panw sto meso beta twn portofoliwn N metoxwn) ths teleutaias periodou
    adjustment=adjustmentPerPeriod(stocksBetaDataFrame,period0,period1)
    estimatedPortofoliosBetaWithAdj=adjustment[0] +adjustment[1]*np.array(estimatedPortofoliosBetaWithoutAdj)

    ### to pragmatiko meso beta ths periodou pou theloume na ektimhsoume, opote gia ta idia portofolia pou xrhsimopoihshame sthn rohgoumenh periodo gia provlepsh
    ### vrhskoume to pragmatiko tous beta mia periodo mprosta
    portofoliosList=combinationsOfPortofolios(stocksBetaDataFrame,period1,sizePortofolio)[2]
    nStocksPortofolioBeta=[]
    for portofolio in portofoliosList:
    
          nStocksPortofolioBeta.append(estimatePortofolioBeta(stocksBetaDataFrame,period2,portofolio))

    realizedPortofoliosBeta=nStocksPortofolioBeta

    A=estimatedPortofoliosBetaWithoutAdj
    B=estimatedPortofoliosBetaWithAdj
    C=realizedPortofoliosBeta
    ### mesa tetragvnika sfalmata gia tis 2 ektimhseis
    meanSquareErrorWithoutAdjustment=np.square(np.subtract(A, C)).mean()
    meanSquareErrorWithAdjustment=np.square(np.subtract(B, C)).mean()

    

    return [meanSquareErrorWithoutAdjustment,meanSquareErrorWithAdjustment,estimatedPortofoliosBetaWithoutAdj,estimatedPortofoliosBetaWithAdj,realizedPortofoliosBeta,adjustment]

#print(meanSquareErrors(stocksBetaDataFrame,titlePeriod[1],titlePeriod[2],titlePeriod[3],20))



########################################## Descriptive Statistics Block #######################################################

def descriptiveStatisticsSample(stocksBetaDataFrame):
    ### kapoia vasika perigrafika statistika tou deigmatos mas
    meanOfPeriod=[]
    stdvOfPeriod=[]
    percentilesOfPeriod=[]
    for col in stocksBetaDataFrame:
        meanOfPeriod.append(np.mean(stocksBetaDataFrame[col]))
        stdvOfPeriod.append(np.std(stocksBetaDataFrame[col]))
        percentilesOfPeriod.append(np.percentile(stocksBetaDataFrame[col], [10, 25, 50, 75, 90]).tolist())
    return meanOfPeriod,stdvOfPeriod, percentilesOfPeriod

#print(f'Οι μέσες τιμές των περιόδων\n {stocksBetaDataFrame.columns.to_list()} είναι\n {descriptiveStatisticsSample(stocksBetaDataFrame)[0]}\n'\
#      f'Οι τυπικές αποκλίσεις των περιόδων\n {stocksBetaDataFrame.columns.to_list()} είναι\n {descriptiveStatisticsSample(stocksBetaDataFrame)[1]}\n'\
#      f'Τα ποσοστιαία σημεία 10,25,50,75,90 για τις περιόδους\n {stocksBetaDataFrame.columns.to_list()} είναι\n {descriptiveStatisticsSample(stocksBetaDataFrame)[2]}\n\\n\n\n\n' )

####################################################################################################################################


######################################## Correlation Coefficient Data Frame ########################################################

### pinakas gia suntelesth susxetisewn metaksu twn portofoliwn N metoxwn gia 2 periodous, opou oi grammes einai to megethos N twn portofoliwn, kai sthles oi periodoi twn beta
portofolioSizeVector=[1,2,4,7,10,15]
correlationArray=np.zeros((len(portofolioSizeVector),len(titlePeriod)-1))

for row in range(len(portofolioSizeVector)):

    for column in range(len(titlePeriod)-1):
        correlation=correlationCoefficient(stocksBetaDataFrame,titlePeriod[column],titlePeriod[column+1],portofolioSizeVector[row])
        correlationArray[row][column]=correlation
#print(correlationArray)

#### ftiaxnoum ta onomata stis sthles gia to DataFrame
titlePeriod2=[]
for i in range(len(titlePeriod)-1):
    period=' : '.join([titlePeriod[i],titlePeriod[i+1]])  
    titlePeriod2.append(period)

correlationDataFrame=pd.DataFrame(correlationArray,columns=titlePeriod2,index=portofolioSizeVector)        
print(f'Ο πίνακας συσχετίσεων μεταξύ των περιόδων είναι\n {correlationDataFrame}\n\n\n')
#correlationDataFrame.to_excel('correlationDataFrame.xlsx')

###############################################################################################################################################



########################################## Adjustment Models OLS between periods ##############################################################

### mas emfanizei tis parametrous tou montelou prosarmoghs metaksu 2 periodwn
 
for i in range(len(titlePeriod)-2):

      params=adjustmentPerPeriod(stocksBetaDataFrame,titlePeriod[i],titlePeriod[i+1])
      #print('THE REGRESSION TENDENCY OF ESTIMATED BETA COEFFICIENTS FOR INDIVUAL SECURITIES BETWEEN '\
      #f'{titlePeriod[i]} and {titlePeriod[i+1]} is : \n a={params[0]:4.3f} \n b={params[1]:4.3f}\n\n\n')

################################################################################################################################################

 


##################################################### MeanSquareError DataFrame ################################################################

### meso tetragwniko sfalma metaksu pragmatikwn kai ektimhmenwn (me duo tropous) beta twn portofoliwn pou ftiaxnontai apo N metoxes, gia diafores times tou N

portofolioSizeVector=[1,2,3,5,8,10,12,15,25,50]
meanSquareErrorArray=np.zeros((len(portofolioSizeVector),(len(titlePeriod)-2)*2))
for row in range(len(portofolioSizeVector)):
    column=0
    for i in range(len(titlePeriod)-2):
        ### titlePeriod[i] kai titlePeriod[i+1] einai oi periodoi evreshs tou adjustment, kai titlePeriod[i+2] einai h periodos provlepshs
        meanSquare=meanSquareErrors(stocksBetaDataFrame,titlePeriod[i],titlePeriod[i+1],titlePeriod[i+2],portofolioSizeVector[row])
        ### h prwth sthlh afora to meso sfalma me thn provlepsh me toa istoriko beta twn portofoliwn N metoxwn
        meanSquareErrorArray[row][column]=meanSquare[0]
        ### h deuterh sthlh afora to meso tetragwniko sfalma tou prosarmozmenou beta
        meanSquareErrorArray[row][column+1]=meanSquare[1]
        ### gia na upologisei to epomeno set sthlwn gia thn grammh pou eimaste (arithmo metoxwn portofoliou)
        column+=2

#print(meanSquareErrorArray)
### ftixnoume dataframe gia meansquare errors ana megethos portofoliou kai ana periodo
### arxika ftiaxnoume tis onomasies stis sthles sto dataframe ana periodo gia tis 2 methodous
colNames=[2*(x,) for x in titlePeriod[2:]]    # mou diplasiazei mesa se touples thn periodo
colNames=[item for tupla in colNames for item in tupla]      # einai tuples mesa se lista kai tis kanoume flat     

#meanSquareDataFrame=pd.DataFrame( meanSquareErrorArray,columns=colNames,index=portofolioSizeVector)        
#print(f'The mean Square Errors of our estimations are\n {meanSquareDataFrame}\n\n\n')
#meanSquareDataFrame.to_excel('meanSquareError.xlsx')      

##################################################################################################################################################   
 
 


####################### estimated Beta Coefficients DataFrame for portofolios of N securities for each Period ####################################
sizePortofolio=10
numberOfPortofolios=int(len(stocksBetaDataFrame.index)/sizePortofolio)
portofoliosOfnSecuritiesBetasArray=np.zeros((numberOfPortofolios,len(titlePeriod)*2-2))
for i in range(numberOfPortofolios):
    column2=0
    for j in range(len(titlePeriod)-1):
        ### apo thn sunarthsh me tous sunduasmous metoxwn ana N metoxes, dwse to beta tou i portofolio
        portofoliosOfnSecuritiesBetasArray[i][column2]=combinationsOfPortofolios(stocksBetaDataFrame,titlePeriod[j],sizePortofolio)[1][i]

        ### finding the beta of the same portofolios of N securities used in previous period for the next period, for comparison
        portofolio=combinationsOfPortofolios(stocksBetaDataFrame,titlePeriod[j],sizePortofolio)[2][i]   # lista
        portofoliosOfnSecuritiesBetasArray[i][column2+1]=estimatePortofolioBeta(stocksBetaDataFrame,titlePeriod[j+1],portofolio)
        column2+=2
#print(portofoliosOfnSecuritiesBetasArray)       
rawIndex=numberOfPortofolios+1
columnsDF=[titlePeriod[0],titlePeriod[1],titlePeriod[1],titlePeriod[2],titlePeriod[2],titlePeriod[3]]
#portofoliosOfnSecuritiesDF=pd.DataFrame(portofoliosOfnSecuritiesBetasArray,columns=columnsDF,index=range(1,rawIndex))
#portofoliosOfnSecuritiesDF.to_excel('Betas of Portofolios of N securities.xlsx')
#print(f'Τα Betas για τα portofolia που φτιάχνονται από {sizePortofolio} μετοχές είνα\n {portofoliosOfnSecuritiesDF}\n\n\n')      
