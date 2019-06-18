"""
Top 1% of NONZERO Events
Created on Mon Jun 04 10:50:40 2018

A python script to find the top 1% of nonzero events in a year, so that
the changes may be tracked through time.
 
(C) Joey Fogarty 2018
"""

### Import needed Python libraries ###
import numpy as np
import sys
import csv
from collections import Counter
import matplotlib.pylab as plt
from numpy.polynomial.polynomial import polyfit
from scipy import stats

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
with open(station, 'r') as f:
    for line in f.readlines():
        l = line.split(', ')
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
the dates as strings. We will also convert all trace values to 0.00.
Some values end in an "A" for accumulation. For this code, we want to ignore
these, so a function will be defined first
"""

def accum(n):
    return float(str(n)[:-1])

#print accum("2.78A")
#print accum("2A")

flags = ["T", "M", "S"]
daily_precip = map(lambda s: s.strip(), daily_precip)
for i in range(len(daily_precip)):
    if daily_precip[i] in flags:
        daily_precip[i] = 0.00
    elif daily_precip[i][-1] == "A":
        daily_precip[i] = accum(daily_precip[i])
    else:
        daily_precip[i] = np.float(daily_precip[i])

"""
We now have two lists of equal length, one full of strings of dates, and
the other full of floats of precipitation values. Now we put both of these
lists into one dictionary to work with.
"""

precip_dict = dict(zip(date, daily_precip))
print " Precipitation Dictionary Created"

### Creating the Percentile Dictionaries ###

"""
Now we want to find the 99th percentile of non-zero events, so we will use
the same method of iterating precipitation values into separate years, but
instead of having a condition where the value must be over a certain percentile,
the value must now not equal zero.
"""

date2 = [d[0:4] for d in date] #gives list of years

# First we create a blank dictionary with just the years
precip_dict_by_year = {}

for yr in range(int(date[0][0:4]),int(date[-1][0:4])+1):
    precip_dict_by_year[yr] = []

for yr, precip in zip(date2, daily_precip):
    if precip != 0.00:
        precip_dict_by_year[int(yr)].append(precip)
    
#Now we will convert the Precip Dict to an array

print list(set(date2))

for k, v in precip_dict_by_year.iteritems():
    precip_dict_by_year[k] = max(v)
print precip_dict_by_year

### Plotting ###

"""
Now each year has the top 1% of non-zero precipitation events, we will sort
the dictionary and extract pairs of tuples from the dictionary, and plot both
the points and the regression line
"""
'''
pairs = sorted(precip_dict_by_year.items())
x, y = zip(*pairs)
plt.plot(x, y, '.')
plt.show()
'''

with open('SS_nonzero_data.csv', 'wb') as f: #change station!
    writer = csv.writer(f)
    writer.writerow(["Top of Nonzero Events"])
    for key, value in precip_dict_by_year.items():
        writer.writerow([key, value])





























