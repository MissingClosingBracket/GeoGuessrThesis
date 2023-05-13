from helperFunctions import getDistance
from math import sqrt

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

#Bornholm:((15.12845159375, 55.06021289375), (14.71319220625, 55.222993624999994)) -> 49.39168946948267km
#Malta: ((14.531639379999998, 35.809913025), (14.202205349999996, 36.070482760000004)) -> 46.16277106066941

bornholmCoords = [(15.12845159375, 55.06021289375), (14.71319220625, 55.222993624999994)]
bornholmEntireDist = getDistance(bornholmCoords[0], bornholmCoords[1])

maltaCoords = [(14.531639379999998, 35.809913025), (14.202205349999996, 36.070482760000004)]
maltaEntireDist = getDistance(maltaCoords[0], maltaCoords[1])

bornholmMiddlePoint = ( (bornholmCoords[0][0] + bornholmCoords[1][0])/2.0, (bornholmCoords[0][1] + bornholmCoords[1][1])/2.0 )
bornholmMiddleDist1 = getDistance(bornholmMiddlePoint, bornholmCoords[0])
bornholmMiddleDist2 = getDistance(bornholmMiddlePoint, bornholmCoords[1])

maltaMiddlePoint = ((maltaCoords[0][0] + maltaCoords[1][0])/2.0,(maltaCoords[0][1] + maltaCoords[1][1])/2.0)
maltaMiddleDist1 = getDistance(maltaMiddlePoint, maltaCoords[0])
maltaMiddleDist2 = getDistance(maltaMiddlePoint, maltaCoords[1])

bornholmHaversineHalf1 =  (bornholmMiddleDist1/bornholmEntireDist) * 100
#print('Bornholm haversine half percent 1: ', bornholmHaversineHalf1) #Should be close to 50%
bornholmHaversineHalf2 =  (bornholmMiddleDist2/bornholmEntireDist) * 100
#print('Bornholm haversine half percent 2: ', bornholmHaversineHalf2) #Should be close to 50%
print('Diff in percent Bornholm: ', (50.0-bornholmHaversineHalf1)*2)

maltaHaversineHalf1 = (maltaMiddleDist1/maltaEntireDist) * 100
#print('Malta haversine half percent 1: ', maltaHaversineHalf1) #Should be close to 50%
maltaHaversineHalf2 = (maltaMiddleDist2/maltaEntireDist) * 100
#print('Malta haversine half percent 2: ', maltaHaversineHalf2) #Should be close to 50%
print('Diff in percent Malta: ', (50.0-maltaHaversineHalf1)*2)


####################################


bornholmEntireEuclideanDist = calc(bornholmCoords[0], bornholmCoords[1])
maltaEntireEuclideanDist = calc(maltaCoords[0], maltaCoords[1])

bornholmEuclideanHalfDist1 = calc(bornholmCoords[0], bornholmMiddlePoint)
bornholmEuclideanHalfDist2 = calc(bornholmCoords[1], bornholmMiddlePoint)
maltaEuclideanHalfDist1 = calc(maltaCoords[0], maltaMiddlePoint)
maltaEuclideanHalfDist2 = calc(maltaCoords[1], maltaMiddlePoint)

bornholmEuclideanHalf1 =  (bornholmEuclideanHalfDist1/bornholmEntireEuclideanDist) * 100
print('Bornholm euclidean half percent 1: ', bornholmEuclideanHalf1) #Should be exactly 50%
bornholmEuclideanHalf2 =  (bornholmEuclideanHalfDist2/bornholmEntireEuclideanDist) * 100
print('Bornholm euclidean half percent 2: ', bornholmEuclideanHalf2) #Should be exactly 50%

maltaEuclideanHalf1 =  (maltaEuclideanHalfDist1/maltaEntireEuclideanDist) * 100
print('Malta euclidean half percent 1: ', maltaEuclideanHalf1) #Should be exactly 50%
maltaEuclideanHalf2 =  (maltaEuclideanHalfDist2/maltaEntireEuclideanDist) * 100
print('Malta euclidean half percent 2: ', maltaEuclideanHalf2) #Should be exactly 50%