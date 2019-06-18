"""
Bin Separation Script
Created Feb 09, 2018
A python script to take the daily precipitation data from SC_ACIS for a 
range of years at one station, and separate the data into pre-defined
"precip bins." This script should end with a yearly frequency for each 
precip bin.
(C) Joey Fogarty 2018
"""

### Import needed Python libraries ###
import numpy as np
import sys
import csv

#### Get Data ###

"""
We want to define certain "bins" that daily precip values will be sorted into.
The bins are defined as follows: {0-0.02 and T, 0.03-0.10, 0.11-0.25, 0.26-0.50,
0.51-1.00, 1.01-1.50, 1.51-2.00, 2.01-2.50, 2.51-3.00, 3.01-4.00, 4.01-5.00,
5.01-6.00, 6.01-7.00, 7.01+} 
"""

station = "precip_data/nb_precip_POR_adjusted.txt"

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
"""

flags = ["T", "M", "S"]
daily_precip = map(lambda s: s.strip(), daily_precip)
for i in range(len(daily_precip)):
    if daily_precip[i] in flags:
        daily_precip[i] = 0.00
    else:
        daily_precip[i] = np.float(daily_precip[i])

"""
We now have two lists of equal length, one full of strings of dates, and
the other full of floats of precipitation values. Now we must categorize
the data. Each year should have a certain amount of frequencies for
each category.
First, we will initialize a nested dictionary for the data. In this one
dictionary, it will contain all the years in whatever station file is given
"""

precip_dict = {}
for yr in range(int(date[0][0:4]),int(date[-1][0:4])+1):
    precip_dict[yr] = {}

"""
Now, we add all of this data into the empty dictionary
"""

for i in range(len(date)):
    precip_dict[int(date[i][0:4])][date[i]] = daily_precip[i]
print " Precipitation Dictionary Created"

"""
We will define the bins discussed above as A, B, C, etc, so that it is
easier to code. Here is an official category breakdown:
A = 0-0.02 and T
B = 0.03-0.10
C = 0.11-0.25
D = 0.26-0.50
E = 0.51-1.00
F = 1.01-1.50
G = 1.51-2.00
H = 2.01-2.50
I = 2.51-3.00
J = 3.01-4.00
K = 4.01-5.00
L = 5.01-6.00
M = 6.01-7.00
N = 7.01+
For each year in the dictionary, each day will have a value A-N assigned to
it. We first initialize ANOTHER nested dictionary, but this time, each year
will have keys A-N, and values of the frequency A-N
"""

precip_category = ["A", "B", "C", "D", "E", "F", "G", \
                   "H", "I", "J", "K", "L", "M", "N"]

precip_freq = {}
for yr in range(int(date[0][0:4]),int(date[-1][0:4])+1):
    precip_freq[yr] = {key: 0 for key in precip_category}

for i in range(len(date)):
    if precip_dict[int(date[i][0:4])][date[i]] < 0.03:
        precip_freq[int(date[i][0:4])]["A"] += 1
    elif precip_dict[int(date[i][0:4])][date[i]]  < 0.11:
        precip_freq[int(date[i][0:4])]["B"] += 1
    elif precip_dict[int(date[i][0:4])][date[i]]  < 0.26:
        precip_freq[int(date[i][0:4])]["C"] += 1
    elif precip_dict[int(date[i][0:4])][date[i]]  < 0.51:
        precip_freq[int(date[i][0:4])]["D"] += 1
    elif precip_dict[int(date[i][0:4])][date[i]]  < 1.01:
        precip_freq[int(date[i][0:4])]["E"] += 1
    elif precip_dict[int(date[i][0:4])][date[i]]  < 1.51:
        precip_freq[int(date[i][0:4])]["F"] += 1
    elif precip_dict[int(date[i][0:4])][date[i]]  < 2.01:
        precip_freq[int(date[i][0:4])]["G"] += 1
    elif precip_dict[int(date[i][0:4])][date[i]]  < 2.51:
        precip_freq[int(date[i][0:4])]["H"] += 1
    elif precip_dict[int(date[i][0:4])][date[i]]  < 3.01:
        precip_freq[int(date[i][0:4])]["I"] += 1
    elif precip_dict[int(date[i][0:4])][date[i]]  < 4.01:
        precip_freq[int(date[i][0:4])]["J"] += 1
    elif precip_dict[int(date[i][0:4])][date[i]]  < 5.01:
        precip_freq[int(date[i][0:4])]["K"] += 1
    elif precip_dict[int(date[i][0:4])][date[i]]  < 6.01:
        precip_freq[int(date[i][0:4])]["L"] += 1
    elif precip_dict[int(date[i][0:4])][date[i]]  < 7.01:
        precip_freq[int(date[i][0:4])]["M"] += 1
    else:
        precip_freq[int(date[i][0:4])]["N"] += 1


### Verification ###

"""
As a quick verification, we can check if the amount of frequencies for
a year add up to a reasonable number (i.e. 365 or 366). This is done below:
"""

years = list(precip_freq.keys())
verify = []
for i in range(len(years)):
    verify.append(sum(precip_freq[years[i]].values()))
#print verify

### Visualization ###

"""
The creation of the 3D plot can be done in Excel. Right now, we want to
create a csv file with the year as the first column, and the corresponding
precipitation categories ("A", "B", "C"..., etc) the following columns, from
lowest to highest.
"""

def mergedict(a,b):
    a.update(b)
    return a
'''
with open("test_output.csv", "wb") as f:
    w = csv.DictWriter(f, precip_category)
    w.writeheader()
    for k,d in sorted(precip_freq.items()):
        w.writerow(mergedict({'A': k},d))
'''
