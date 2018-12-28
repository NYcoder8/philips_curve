import pandas as pd
import pandas_datareader as pdm


# recession indicators via NBER http://www.nber.org/cycles.html

r_df = pd.DataFrame(columns =['Peak','Trough'], 
    data =[['1948-11-01','1949-10-01'],
           ['1953-07-01','1954-05-01'],
           ['1957-08-01','1958-04-01'],
           ['1960-04-01','1961-02-01'],
           ['1969-12-01','1970-11-01'],
           ['1973-11-01','1975-03-01'],
           ['1980-01-01','1980-07-01'],
           ['1981-07-01','1982-11-01'],
           ['1990-07-01','1991-03-01'],
           ['2001-03-01','2001-11-01'],
           ['2007-12-01','2009-06-01']])

r_df['Peak'] = pd.to_datetime(r_df['Peak'])
r_df['Trough'] = pd.to_datetime(r_df['Trough'])

# econ data symbol and name setup

symbols = [('PCEPILFE', 'Core PCE'),
            ('UNRATE','Unemployment Rate'),
            ('EMRATIO','Employment-to-Population Ratio'),
            ('LNS12300060', 'Prime Working Age Employment-to-Population Ratio'),
            ('NROU','Natural Rate of Unemploymnet')]
s_columns = ['Symbol','Varname']            

ticker_set =pd.DataFrame.from_records(symbols,columns=s_columns)
ticker = ticker_set['Symbol']

# download the data from FRED
df = pdm.DataReader(ticker, 'fred', start='1958-01-01')


#df = df.join(ticker_set, how='left', on='Symbol')

# convert to quarterly data
dfq = df.set_index(df.index).resample('QS')['LNS12300060','NROU','UNRATE','PCEPILFE'].mean()

#rename columns
dfq.columns =['epop','nrou','unrate','pce']

# Add additional columns for lags and slack
dfq['pce_inf'] =100*(dfq['pce']/dfq['pce'].shift(4)-1)
dfq['slack'] = dfq['unrate']-dfq['nrou']
dfq['pce_lag']=dfq['pce_inf'].shift(4)


# plots

import matplotlib.pyplot as plt

plt.style.use('ggplot')


plt.plot(dfq.pce_inf['1959':'1985'], '--', label="Inflation") 
plt.plot(dfq.slack['1959':'1985'], label ="Slack") 
plt.legend()
plt.axvspan('1960-04-01','1961-02-01',alpha=0.5)
plt.axvspan('1969-12-01','1970-11-01',alpha=0.5)
plt.axvspan('1973-11-01','1975-03-01',alpha=0.5)
plt.axvspan('1980-01-01','1980-07-01',alpha=0.5)
plt.axvspan('1981-07-01','1982-11-01',alpha=0.5)

