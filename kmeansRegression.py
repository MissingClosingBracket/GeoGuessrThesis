#Thank you https://www.reneshbedre.com/blog/kmeans-clustering-python.html and https://www.dominodatalab.com/blog/getting-started-with-k-means-clustering-in-python

from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from euclideanDistnaceCalculater import calc
import matplotlib.lines as lines

dataset, classes = make_blobs(n_samples=1_000_000, n_features=2, centers =1, cluster_std=0.5, center_box=(1, 2), random_state=1337)
df = pd.DataFrame(dataset, columns=['x', 'y'])

regressionData = []
iterations = 30
centroids = None
def f(x):
    if x == 0:
        return 'ClusterC'
    if x == 1:
        return 'ClusterB'
    if x == 2:
        return 'ClusterA'

for i in range(iterations):
    kmeans = KMeans(
        n_clusters=3, 
        init=(centroids if centroids is not None else 'random'), 
        random_state=170, 
        n_init=1, 
        max_iter=1)
    kmeans.fit(df)
    centroids = kmeans.cluster_centers_

    regressionData.append([centroids[2], centroids[1], centroids[0]])

finalCentroids = regressionData[iterations-1]

plotDataA = []
plotDataB = []
plotDataC = []
i = 1

for points in regressionData:
    
    distA = calc(points[0], finalCentroids[0])
    distB = calc(points[1], finalCentroids[1])
    distC = calc(points[2], finalCentroids[2])

    plotDataA.append([i,distA])
    plotDataB.append([i,distB])
    plotDataC.append([i,distC])
    i+=1

# Initialize layout
fig, ax = plt.subplots(figsize = (9, 9))

#colors
cmap = plt.cm.get_cmap('viridis')
colA = cmap(0.2)
colB = cmap(0.5)
colC = cmap(0.8)

# Add scatterplot and lines
A = lines.Line2D(xdata=[x[0] for x in plotDataA], ydata=[x[1] for x in plotDataA],color=colA,linewidth=2)
ax.add_line(A)

B = lines.Line2D(xdata=[x[0] for x in plotDataB], ydata=[x[1] for x in plotDataB],color=colB,linewidth=2)
ax.add_line(B)

C = lines.Line2D(xdata=[x[0] for x in plotDataC], ydata=[x[1] for x in plotDataC],color=colC,linewidth=2)
ax.add_line(C)

ax.scatter([x[0] for x in plotDataA], [x[1] for x in plotDataA], s=20, alpha=0.7, label="ClusterA", color=colA)
ax.scatter([x[0] for x in plotDataB], [x[1] for x in plotDataB], s=20, alpha=0.7, label="ClusterB", color=colB)
ax.scatter([x[0] for x in plotDataC], [x[1] for x in plotDataC], s=20, alpha=0.7, label="ClusterC", color=colC)

ax.axes.set_facecolor('black')
plt.xlabel("Iteration")
plt.ylabel("Distance to final centroid")
plt.legend(loc="upper right")
plt.show()


