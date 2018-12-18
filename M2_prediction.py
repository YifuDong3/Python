# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 17:52:31 2018

Prediction m2 for macroeconomics researching

"""

import warnings
import itertools
import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import datetime
plt.style.use('fivethirtyeight')

from WindPy import w
from datetime import *
w.start()

wsd_data=w.edb("M0001384,M5525755,M5525756", "2002-12-31",  datetime.today(),"Fill=Previous")

MacroData=pd.DataFrame(wsd_data.Data, index=wsd_data.Codes, columns=wsd_data.Times).T
'''
没有单位
'''

MacroData.columns = ["M2","Community financing","rmb loan"]

y=MacroData["M2"]

y.plot(figsize=(15,6))
plt.show()


# Define the p, d and q parameters to take any value between 0 and 2
p = d = q = range(0, 2)

# Generate all different combinations of p, q and q triplets
pdq = list(itertools.product(p, d, q))

# Generate all different combinations of seasonal p, q and q triplets
seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]

print('Examples of parameter combinations for Seasonal ARIMA...')
print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[1]))
print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[2]))
print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[3]))
print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[4]))


# start AIC searching
warnings.filterwarnings("ignore") # specify to ignore warning messages

AIC_list = pd.DataFrame({},columns = ['param','param_seasonal','AIC'])

for param in pdq:
    for param_seasonal in seasonal_pdq:
        try:
            mod = sm.tsa.statespace.SARIMAX(y,
                                            order=param,
                                            seasonal_order=param_seasonal,
                                            enforce_stationarity=False,
                                            enforce_invertibility=False)

            results = mod.fit()

            print('ARIMA{}x{} - AIC:{}'.format(param, param_seasonal, results.aic))
            temp = pd.DataFrame([[ param ,  param_seasonal , results.aic ]], columns=['param','param_seasonal','AIC'])
            AIC_list = AIC_list.append( temp, ignore_index=True)  # DataFrame append 는 일반 list append 와 다르게 이렇게 지정해주어야한다.
            del temp
            
        except:
            continue
        
        
m = np.amin(AIC_list['AIC'].values) # Find minimum value in AIC
l = AIC_list['AIC'].tolist().index(m) # Find index number for lowest AIC
Min_AIC_list = AIC_list.iloc[l,:]       
    
#step 5

mod = sm.tsa.statespace.SARIMAX(y,
                                order= Min_AIC_list.param,
                                seasonal_order=Min_AIC_list.param_seasonal,
                                enforce_stationarity=False,
                                enforce_invertibility=False)

results = mod.fit()

print("### Min_AIC_list ### \n{}".format(Min_AIC_list))

print(results.summary().tables[1])


results.plot_diagnostics(figsize=(15, 12))
plt.show()

#step6
pred = results.get_prediction(start=pd.to_datetime('2016-01-31'), dynamic=False)
pred_ci = pred.conf_int()

#index
date_time = datetime.strptime('2001-1-31','%Y-%m-%d')
ax = y[date_time.date():].plot(label='observed')
pred.predicted_mean.plot(ax=ax, label='One-step ahead Forecast', alpha=.7)

ax.fill_between(pred_ci.index,
                pred_ci.iloc[:, 0],
                pred_ci.iloc[:, 1], color='k', alpha=.2)

ax.set_xlabel('Date')
ax.set_ylabel('import Levels')
plt.legend()

plt.show()

#step 6 quantify the accuracy of our forecasts
y_forecasted = pred.predicted_mean
y_truth = y[date_time.date():]

# Compute the mean square error
mse = ((y_forecasted - y_truth) ** 2).mean()
print('The Mean Squared Error of our forecasts is {}'.format(round(mse, 2)))


#step 7 Plotting the observed and forecasted of the time series
pred_uc = results.get_forecast(steps=12)
pred_ci = pred_uc.conf_int()

ax = y.plot(label='observed', figsize=(20, 15))
pred_uc.predicted_mean.plot(ax=ax, label='Forecast')
ax.fill_between(pred_ci.index,
                pred_ci.iloc[:, 0],
                pred_ci.iloc[:, 1], color='k', alpha=.25)
ax.set_xlabel('Date')
ax.set_ylabel('import Levels')

plt.legend()
plt.show()

# calculate the list of 12 predicted values 
m2_predicted = pred_uc.predicted_mean.values

# fetch the previous year M2 values
previous_m2 = y.iloc[-12:].values

# predicted M2 growth rate in next twelve months
m2_growth = pd.Series(m2_predicted/previous_m2-1)*100

print (m2_growth)