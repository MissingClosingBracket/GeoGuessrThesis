from math import sqrt
from math import pow
from helperFunctions import getDistance

#eucl
def calc(p1,p2):
    x1=p1[0]
    y1=p1[1]
    x2=p2[0]
    y2=p2[1]

    dist = sqrt(
        pow(x1-x2,2) +
        pow(y1-y2,2)
    )

    return dist

#haversine
def hav(x,y): 
    return getDistance(x,y)

data1 = [
    (14.75867745,55.1797539),
    (14.89183065,55.119337200000004),
    (15.06827895,55.061246249999996)
]
data2 = [
    (14.76468147,55.15867943),
    (14.92302334,55.1232714),
    (15.07548271,55.06935343)
]

for x in range(0, len(data1)):
    print(hav(data1[x], data2[x]))

''' used for guess comp. of CC and KMeans
lats = [14.75867745,14.89183065,15.06827895]
lons = [55.1797539,55.119337200000004,55.061246249999996]

[14.76468147 55.15867943]
[14.92302334 55.1232714 ]
[15.07548271 55.06935343]
'''