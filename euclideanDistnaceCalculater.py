from math import sqrt
from math import pow

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

data1 = [
(1.8890016, 0.87425904),
(1.98220248, 0.71230824),
(2.11406729, 0.68280203),
(2.25307478, 0.69858443)
]
data2 = (2.25307478, 0.69858443)

for entry in data1:
    calc(entry, data2)
