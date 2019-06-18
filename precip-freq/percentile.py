"""
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
the dates as strings. We will also convert all trace/missing values to 0.00.
"""

daily_precip = map(lambda s: s.strip(), daily_precip)
for i in range(len(daily_precip)):
    if daily_precip[i] == "T":
        daily_precip[i] = 0.00
    elif daily_precip[i] == "M":
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

### Creating the Percentile Dictionaries ###

"""
Now, we want to find the 90th, 95th, and 99th percentile of precip for this
station. We also want to find the 90th, 95th, and 99th percentile by year as
well. This will allow us to constuct the two graphs. We will do this by sorting
the dictionary and then finding the top percentages, and then counting the
frequency of each year in those percentiles. 
"""

daily_precip_array = np.array(daily_precip)
p90 = np.percentile(daily_precip_array,90)
p95 = np.percentile(daily_precip_array,95)
p99 = np.percentile(daily_precip_array,99)
#print p90, p95, p99

"""
So, if a value is:
>= p90, it's in the 90th percentile
>= p95, it's in the 95th percentile
>= p99, it's in the 99th percentile

Now we will change the value in the dictionary if the key is above any
of these thresholds.
"""

p90_years, p95_years, p99_years = ([] for i in range(3))
#p90_events, p95_events, p99_events = ([] for i in range(3))

for k, v in precip_dict.items():
    if v >= p99:
        p90_years.append(k[0:4])
#        p90_events.append(v)
    if v >= p95:
        p95_years.append(k[0:4])
#        p95_events.append(v)
    if v >= p90:
        p99_years.append(k[0:4])
#        p99_events.append(v)

#print p90_events, len(p90_events)
#print p95_events, len(p95_events)
#print p99_events, len(p99_events)
#print len(p90_years)
#print len(p95_years)
#print len(p99_years)

"""
We now have three lists, each containing the dates that are in the
90th, 95th, and 99th percentile of events. We then calculate how many
times a 90/95/99th percentile event has occured in all of the years in
this period of record. Each year will have its own list with three
variables, all frequencies of 90/95/99th percentile events.
"""

p90_dict = dict(Counter(p90_years))
p95_dict = dict(Counter(p95_years))
p99_dict = dict(Counter(p99_years))

#print "here is p90 dict:"
#print p90_dict

"""
Let's also create a dictionary with the total amount of precipitation events
for each year, and this will also be exported to a .csv file. To do this, we
will delete any element from the dictionary that has a 0.00" precip value. 
Reminder that this includes Missing as well as Trace events, since they were
changed to 0.00 events.
"""

precip_events = [[d, p][0][0:4] for d, p in zip(date, daily_precip) if p != 0.00]
precip_events_dict = dict(Counter(precip_events))
print precip_events_dict

### Percentage of Total Precipitation ###

"""
We will now try to add to our CSV file total yearly precipitation, as well as 
the sum of the 90/95/99th percentile events. First, we grab data from another
file to retrieve annual precipitation values
"""
'''
annual = "precip_data/nb_monthly_precip.txt"
year_annualprecip = []
monthly_precipvalues = []
with open(annual, 'r') as f:
    for line in f.readlines():
        l = line.split(', ')
        year_annualprecip.append(l[0])
        monthly_precipvalues.append(float(l[-1]))
#print year_annualprecip
#print monthly_precipvalues
annual_precip_dict = dict(zip(year_annualprecip, monthly_precipvalues))
'''
date2 = [d[0:4] for d in date] #gives list of years

# First we create a blank dictionary with just the years
sum_of_p_events_dict_90 = {}
sum_of_p_events_dict_95 = {}
sum_of_p_events_dict_99 = {}
for yr in range(int(date[0][0:4]),int(date[-1][0:4])+1):
    sum_of_p_events_dict_90[yr] = []
for yr in range(int(date[0][0:4]),int(date[-1][0:4])+1):
    sum_of_p_events_dict_95[yr] = []
for yr in range(int(date[0][0:4]),int(date[-1][0:4])+1):
    sum_of_p_events_dict_99[yr] = []

for yr, precip in zip(date2, daily_precip):
    if precip >= p99:
        sum_of_p_events_dict_99[int(yr)].append(precip)
    if precip >= p95:
        sum_of_p_events_dict_95[int(yr)].append(precip)
    if precip >= p90:
        sum_of_p_events_dict_90[int(yr)].append(precip)

for k, v in sum_of_p_events_dict_90.items():
    sum_of_p_events_dict_90[k] = round(sum(v),2)
for k, v in sum_of_p_events_dict_95.items():
    sum_of_p_events_dict_95[k] = round(sum(v),2)
for k, v in sum_of_p_events_dict_99.items():
    sum_of_p_events_dict_99[k] = round(sum(v),2)

print sum_of_p_events_dict_90
print sum_of_p_events_dict_95
print sum_of_p_events_dict_99

### Creating the CSV File ###

"""
Now we want to create a .csv file with all of the data, so that this data
may be manipulated in Excel.
"""

with open('test_SS_percentile_data.csv', 'wb') as f: #change station!
    writer = csv.writer(f)
    writer.writerow(["Total Events"])
    for key, value in precip_events_dict.items():
        writer.writerow([key, value])
    writer.writerow(["90th Percentile"])
    for key, value in p90_dict.items():
        writer.writerow([key, value])
    writer.writerow(["95th Percentile"])
    for key, value in p95_dict.items():
        writer.writerow([key, value])
    writer.writerow(["99th Percentile"])
    for key, value in p99_dict.items():
        writer.writerow([key, value])
#    writer.writerow(["Total Annual Precipitation"])
#    for key, value in annual_precip_dict.items():
#        writer.writerow([key, value])
    writer.writerow(["Total 90th P Precipitation"])
    for key, value in sum_of_p_events_dict_90.items():
        writer.writerow([key, value])
    writer.writerow(["Total 95th P Precipitation"])
    for key, value in sum_of_p_events_dict_95.items():
        writer.writerow([key, value])
    writer.writerow(["Total 99th P Precipitation"])
    for key, value in sum_of_p_events_dict_99.items():
        writer.writerow([key, value])
f.close()








