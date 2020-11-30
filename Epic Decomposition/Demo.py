import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import MeanShift, estimate_bandwidth
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer

with open('epic.txt') as f:
    documents = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
documents = [x.strip() for x in documents] 

vectorizer = TfidfVectorizer(stop_words='english', smooth_idf=True,use_idf=True)
X = vectorizer.fit_transform(documents)

bandwidth = estimate_bandwidth(X.toarray(), quantile=0.3, n_jobs=-1)

model = MeanShift(bin_seeding=True, n_jobs=-1)
model.fit(X.toarray())
labels = model.labels_
cluster_centers = model.cluster_centers_

labels_unique = np.unique(labels)
n_clusters_ = len(labels_unique)

print(n_clusters_)

#labels = model.labels_
#cluster_centers = model.cluster_centers_

#labels_unique = np.unique(labels)
#n_clusters_ = len(labels_unique)

#print("number of estimated clusters : %d" % n_clusters_)

#order_centroids = model.cluster_centers_.argsort()[:, ::-1]
#terms = vectorizer.get_feature_names()
#for i in range(n_clusters_):
#    print("Cluster %d:" % i),
#    for ind in order_centroids[i, :10]:
#        print(' %s' % terms[ind]),
#    print

#Y = vectorizer.transform(["Add a background color to cells that can be any RGB color."])
#prediction = model.predict(Y)
#print(prediction)

#output = []

#for x in range(len(X)):
#

#print(X)