from pandas_datareader import data, wb
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import seaborn as sns


sns.set_style('whitegrid')

from pandas_datareader.iex.daily import IEXDailyReader


start = datetime.datetime(2014, 1, 1)
end = datetime.datetime(2017, 1, 1)

BAC = data.DataReader("BAC", 'iex', start, end)
#print(BAC)
C = data.DataReader("C", 'iex', start, end)
#print(C)
GS = data.DataReader("GS", 'iex', start, end)
#print(GS)
JPM = data.DataReader("JPM", 'iex', start, end)
#print(JPM)
MS = data.DataReader("MS", 'iex', start, end)
#print(MS)
WFC = data.DataReader("WFC", 'iex', start, end)
#print(WFC)


#Alt
df = data.DataReader(['BAC','C','GS','JPM','MS','WFC'], 'iex', start, end)
print(df)

tickers = ['BAC','C','GS','JPM','MS','WFC']
bank_stocks = pd.concat([ BAC,C,GS,JPM,MS,WFC], axis=1, keys=tickers)
bank_stocks.columns.names = ['Bank Ticker', 'Stock Info']
print(bank_stocks.head())

#for tick in tickers:
    #print(bank_stocks[tick].max())

#Max close price for each bank
print(bank_stocks.xs(key='close', axis=1, level='Stock Info').max())

returns = pd.DataFrame()
for tick in tickers:
    returns[tick+' Return'] = bank_stocks[tick]['close'].pct_change()
print(returns.head())

sns.pairplot(returns[1:])
plt.show()

#print(returns['BAC Return'].argmin()) NECE DA OCITA ARGMIN
#Worst and best day for each bank at close
print(returns.idxmin())
print(returns.idxmax())

print(returns.std())
print(returns.loc['2015-01-01':'2015-12-31'].std())

sns.distplot(returns.loc['2015-01-01':'2015-12-31']['MS Return'], color='green', bins=100)
plt.show()

sns.distplot(returns.loc['2016-01-01':'2016-31-12']['C Return'], color='red', bins=100)
plt.show()

#for tick in tickers:
    #bank_stocks[tick]['close'].plot(figsize=(12,4), label=tick)
#plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
#plt.show()

#OR ALT

bank_stocks.xs(key='close', axis=1, level='Stock Info').plot()
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.show()

#30 days average closed price for BAC
plt.figure(figsize=(12,6))
BAC['close'].loc['2015-01-01':'2016-01-01'].rolling(window=30).mean().plot(label='30 Days Average')
BAC['close'].loc['2015-01-01':'2016-01-01'].plot(label='Closed')
plt.legend()
plt.show()

#Corellation between banks
sns.heatmap(bank_stocks.xs(key='close', axis=1,level='Stock Info').corr(), annot=True)
plt.show()

sns.clustermap(bank_stocks.xs(key='close', axis=1,level='Stock Info').corr(), annot=True)
plt.show()

