#!/usr/bin/python
#coding: utf-8



### this is a transformation file
###from "Fri, Nov 5, 2018" to standard datetime for matching


import pandas
import numpy
from datetime import datetime


##need to be your own directory
date=pandas.read_csv('/Users/dongyifu/Desktop/basktest.csv')

#simple test
t=date["DATE"][1]
print date["DATE"][1]
print list(t)
list_t=list(t)
del list_t[0:5]
print ''.join(list_t)
chenggong= ''.join(list_t)
print type(chenggong)



# begin
t=date["DATE"]
date_list=[0]
for i in range(len(date["DATE"])):

	date=t[i]
	date=list(date)
	del date[0:5]
	date_adjust=''.join(date)
	datetime_adjust=datetime.strptime(date_adjust,"%b %d,%Y")
	dt_adjust = datetime_adjust.strftime("%Y-%m-%d %H:%M:%S")
	ta = list(dt_adjust)
	del ta[10:19]
	ta = ''.join(ta)
	date_list.append(ta)

del date_list[0]

print date_list

# now the "date" has changed by the loop, so we need to re-import from our directory.
date=pandas.read_csv('/Users/dongyifu/Desktop/basktest.csv')

#add column
date["date"]=date_list

##need to change to be your own directory
date.to_csv("/Users/dongyifu/Desktop/badjustbasket.csv")  ##need to be your own directory
