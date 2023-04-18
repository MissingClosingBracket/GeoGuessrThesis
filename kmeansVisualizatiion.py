#Thank you https://www.reneshbedre.com/blog/kmeans-clustering-python.html and https://www.dominodatalab.com/blog/getting-started-with-k-means-clustering-in-python

from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

dataset, classes = make_blobs(n_samples=100, n_features=2, centers =3, cluster_std=5, center_box=(0, 100), random_state=13377)
df = pd.DataFrame(dataset, columns=['x', 'y'])

iterations = 3
centroids = None
def f(x):
    if x == 0:
        return 'ClusterA'
    if x == 1:
        return 'ClusterB'
    if x == 2:
        return 'ClusterC'

for i in range(iterations):
    kmeans = KMeans(
        n_clusters=3, 
        init=(centroids if centroids is not None else 'random'), 
        random_state=13375, 
        n_init=1, 
        max_iter=1)
    kmeans.fit(df)
    centroids = kmeans.cluster_centers_
    print(centroids)
    kmeans.labels_ = np.array([f(x) for x in kmeans.labels_])
    sns.scatterplot(data=df, x="x", y="y", hue=kmeans.labels_, palette="viridis", s=10)
    fig = plt.scatter(kmeans.cluster_centers_[:,0], kmeans.cluster_centers_[:,1], 
                marker="X", c="yellow", s=60, label="Centroids")
    ax = fig.axes.set_facecolor('black')
    plt.legend(loc="upper left")
    plt.show()

