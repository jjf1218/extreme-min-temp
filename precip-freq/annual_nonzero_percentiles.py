# -*- coding: utf-8 -*-
"""
Updated on Wed Aug 29 11:59:00 2018

Precipitation Percentile Script
Created May 21, 2018

A python script to take the daily precipitation data from SC_ACIS for a 
range of years at one station, and create a chart looking at the 90th, 95th,
and 99th percentile of events. We should end with two graphs. One of them 

(C) Joey Fogarty 2018
"""

### Import needed Python libraries ###
import numpy as np
import sys
import csv
from collections import Counter
import itertools

#### Get Data ###

"""
First we want to grab the data from a CSV file, retrieved from the SC-ACIS
for a NJ station. NOTE: When changing stations, be sure to change the
code down in the last three sections, so that the CSV files properly
reflect the station being analyzed.
"""

station = "precip_data/sussex_precip_POR_adjusted.txt"

date = []
daily_precip = []
l2 = []
with open(station, 'r') as f:
    for line in f.readlines():
        l = line.split(', ')
        l2.append(l)
        date.append(l[0])
        daily_precip.append(l[1])


### Length, Decimal, and Nonnegative Verification ###

"""
The amount of dates should match the amount of precipitation values, so we
want to make sure both lists are the same length, and do not continue if
these values do not match.

COMING SOON: We also want to make sure that any data going into the following
code has two decimal places, and is a nonnegative number.
"""

if len(date) == len(daily_precip):
    print " Date length (" + str(len(date)) \
    + ") and Daily Precip length (" + str(len(daily_precip)) \
    + ") match in length."
    pass
else:
    print "Date length (" + str(len(date)) \
    + ") and Daily Precip length (" + str(len(daily_precip)) \
    + ") do not match in length."
    sys.exit("Lengths do not match, code stopped.")

### Organizing the Data ###

"""
We want to make the actual precipitation values integers, and keep
the dates as strings. We will also convert all trace/missing values to 0.00.
"""

daily_precip = map(lambda s: s.strip(), daily_precip)
for i in range(len(daily_precip)):
    if daily_precip[i] == "T":
        daily_precip[i] = 0.00
    elif daily_precip[i] == "M":
        daily_precip[i] = 0.00
    elif daily_precip[i] == 0.01:
        daily_precip[i] = 0.00
    elif daily_precip[i] == 0.02:
        daily_precip[i] = 0.00
    else:
        daily_precip[i] = np.float(daily_precip[i])

"""
We now have two lists of equal length, one full of strings of dates, and
the other full of floats of precipitation values. Now we put both of these
lists into one dictionary to work with.
"""

precip_dict = dict(zip(date, daily_precip))
print " Precipitation Dictionary Created"

amounts_dict = {}

for a, b in enumerate(date):
    
    amounts_dict[date[a][0:4]] = [daily_precip[a]]

for i, j in enumerate(l2):
    if i == len(date) - 1:
        break
    if j[0][0:4] == l2[i+1][0][0:4]:
        amounts_dict[l2[i+1][0][0:4]].append(float(daily_precip[i+1]))

years = [str(i) for i in list(amounts_dict.keys())]
years.sort(key=int)


p90_amounts = []
p95_amounts = []
p99_amounts = []

for y in years:
    
    flags = [0.0, 0.01, 0.02]
    amounts_dict[y] = [i for i in amounts_dict[y] if i not in flags]
    amounts_dict[y] = np.array(amounts_dict[y])

    p90 = np.percentile(amounts_dict[y],90)
    p90_sum_list = []
    for precip in amounts_dict[y]:
        if precip >= p90:
            p90_sum_list.append(precip)
    p90_amounts.append(round(sum(p90_sum_list),2))
    
    p95 = np.percentile(amounts_dict[y],95)
    p95_sum_list = []
    for precip in amounts_dict[y]:
        if precip >= p95:
            p95_sum_list.append(precip)
    p95_amounts.append(round(sum(p95_sum_list),2))
    
    
    p99 = np.percentile(amounts_dict[y],99)
    p99_sum_list = []
    for precip in amounts_dict[y]:
        if precip >= p99:
            p99_sum_list.append(precip)
    p99_amounts.append(round(sum(p99_sum_list),2))
    
print p90_amounts
print p95_amounts
print p99_amounts



with open('SS_nonzero_percentile_data.csv', 'wb') as f: #change station!
    writer = csv.writer(f)
    writer.writerow(["Year"])
    for year in years:
        writer.writerow([year])
    writer.writerow(["90th Percentile"])
    for i in p90_amounts:
        writer.writerow([i])
    writer.writerow(["95th Percentile"])
    for i in p95_amounts:
        writer.writerow([i])
    writer.writerow(["99th Percentile"])
    for i in p99_amounts:
        writer.writerow([i])


