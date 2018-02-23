"""
The goal of this code is to create a graphic of 4 sub plots,
one per season, that shows the max min and min min
"""

# Import what we need
import numpy as np
import matplotlib.pyplot as plt

print "hey world"

station = ["IM_max_min.txt", "IM_min_min.txt"]
spring_max, summer_max, fall_max, winter_max = ([] for i in range(4))
spring_min, summer_min, fall_min, winter_min = ([] for i in range(4))

"""
We want to get the highest and lowest for the season.
These codes represent the combination of highest and
lowest minimum temperatures for a meteorological season.
In the high code, all "M" values are replaced with -100,
since that will never be the high. In the low code, all
"M" values will be replaced with 150, since this will never
be the low.
"""

### Working with Max Mins ###

# Spring Max Mins
with open(station[0], 'r') as f:
    for line in f.readlines()[3:]:
        l = line.split(',')
        del l[0]
        del l[-1]
        i = 0
        while i < len(l):
            if l[i] == " M" or l[i] == "M":
                l[i] = "-100"
            else:
                i += 1
        l = [float(i.strip(" ")) for i in l[2:5]]
        spring_max.append(max(l))

# Summer Max Mins
with open(station[0], 'r') as f:
    for line in f.readlines()[3:]:
        l = line.split(',')
        del l[0]
        del l[-1]
        i = 0
        while i < len(l):
            if l[i] == " M" or l[i] == "M":
                l[i] = "-100"
            else:
                i += 1
        l = [float(i.strip(" ")) for i in l[5:8]]
        summer_max.append(max(l))

# Fall Max Mins
# Note that these lines go to the second to last line,
# since fall 2017 doesn't exist at this point in time
with open(station[0], 'r') as f:
    for line in f.readlines()[3:-1]:
        l = line.split(',')
        del l[0]
        del l[-1]
        i = 0
        while i < len(l):
            if l[i] == " M" or l[i] == "M":
                l[i] = "-100"
            else:
                i += 1
        l = [float(i.strip(" ")) for i in l[8:11]]
        fall_max.append(max(l))

print "got here"

winter = []
# Winter Max Mins
with open(station[0], 'r') as f:
    for line in f.readlines()[3:]:
        l = line.split(',')
        del l[0]
        del l[-1]
        for i in l:
            i = i[1:]
        k = l[:2] + l[11:]
        winter += k
f.close()

for i in range(len(winter)):
    if winter[i] == " M":
        winter[i] = " -100"
winter = [float(i.strip(" ")) for i in winter[2:]]
winter = [winter[i:i+3] for i in xrange(0, len(winter), 3)]
for i in winter:
    winter_max.append(max(i))

for i in range(len(winter_max)):
    if winter_max[i] < 0.0:
        winter_max[i] = np.NaN


years1 = range(1965,2018)
years2 = range(1965,2017)

'''
print len(years1)
print len(years2)
print len(spring_max)
print len(summer_max)
print len(fall_max)
print len(winter_max)
'''

plt.figure(figsize=[18,10])
# top left, spring
plt.subplot(2,2,1)
plt.plot(years1, spring_max, 'r',linewidth=2)
plt.title("Spring Max Minimum Temperautures")
plt.xlabel("Year")
plt.ylabel("Temperature (F)")
# top right, summer
plt.subplot(2,2,2)
plt.plot(years1, summer_max, 'r',linewidth=2)
plt.title("Summer Max Minimum Temperautures")
plt.xlabel("Year")
plt.ylabel("Temperature (F)")
# bottom left, fall
plt.subplot(2,2,3)
plt.plot(years2, fall_max, 'r',linewidth=2)
plt.title("Fall Max Minimum Temperautures")
plt.xlabel("Year")
plt.ylabel("Temperature (F)")
# bottom right, winter
plt.subplot(2,2,4)
plt.plot(years2, winter_max[:-1], 'r',linewidth=2)
plt.title("Winter Max Minimum Temperautures")
plt.xlabel("Year")
plt.ylabel("Temperature (F)")
plt.suptitle("Indian Mills Maximum Min Temperatures", fontsize=14)
plt.savefig("seasonal_max_min.png", bbox_inches='tight')
#plt.show()

### Working with Min Mins ###

# Spring Min Mins
with open(station[1], 'r') as f:
    for line in f.readlines()[3:]:
        l = line.split(',')
        del l[0]
        del l[-1]
        i = 0
        while i < len(l):
            if l[i] == " M" or l[i] == "M":
                l[i] = "150"
            else:
                i += 1
        l = [float(i.strip(" ")) for i in l[2:5]]
        spring_min.append(min(l))

# Summer Min Mins
with open(station[1], 'r') as f:
    for line in f.readlines()[3:]:
        l = line.split(',')
        del l[0]
        del l[-1]
        i = 0
        while i < len(l):
            if l[i] == " M" or l[i] == "M":
                l[i] = "150"
            else:
                i += 1
        l = [float(i.strip(" ")) for i in l[5:8]]
        summer_min.append(min(l))

# Fall Min Mins
# Note that these lines go to the second to last line,
# since fall 2017 doesn't exist at this point in time
with open(station[1], 'r') as f:
    for line in f.readlines()[3:-1]:
        l = line.split(',')
        del l[0]
        del l[-1]
        i = 0
        while i < len(l):
            if l[i] == " M" or l[i] == "M":
                l[i] = "150"
            else:
                i += 1
        l = [float(i.strip(" ")) for i in l[8:11]]
        fall_min.append(min(l))

print "got here"


winter = []
# Winter Min Mins
with open(station[1], 'r') as f:
    for line in f.readlines()[3:]:
        l = line.split(',')
        del l[0]
        del l[-1]
        for i in l:
            i = i[1:]
        k = l[:2] + l[11:]
        winter += k
f.close()

for i in range(len(winter)):
    if winter[i] == " M":
        winter[i] = " 150"
winter = [float(i.strip(" ")) for i in winter[2:]]
winter = [winter[i:i+3] for i in xrange(0, len(winter), 3)]
for i in winter:
    winter_min.append(min(i))

for i in range(len(winter_min)):
    if winter_min[i] > 100.0:
        winter_min[i] = np.NaN

'''
print len(spring_min)
print len(summer_min)
print len(fall_min)
print len(winter_min)
'''

plt.figure(figsize=[18,10])
# top left, spring
plt.subplot(2,2,1)
plt.plot(years1, spring_min, 'b',linewidth=2)
plt.title("Spring Min Minimum Temperautures")
plt.xlabel("Year")
plt.ylabel("Temperature (F)")
# top right, summer
plt.subplot(2,2,2)
plt.plot(years1, summer_min, 'b',linewidth=2)
plt.title("Summer Min Minimum Temperautures")
plt.xlabel("Year")
plt.ylabel("Temperature (F)")
# bottom left, fall
plt.subplot(2,2,3)
plt.plot(years2, fall_min, 'b',linewidth=2)
plt.title("Fall Min Minimum Temperautures")
plt.xlabel("Year")
plt.ylabel("Temperature (F)")
# bottom right, winter
plt.subplot(2,2,4)
plt.plot(years2, winter_min[:-1], 'b',linewidth=2)
plt.title("Winter Min Minimum Temperautures")
plt.xlabel("Year")
plt.ylabel("Temperature (F)")
plt.suptitle("Indian Mills Minimum Min Temperatures", fontsize=14)
plt.savefig("seasonal_min_min.png", bbox_inches='tight')
#plt.show()





