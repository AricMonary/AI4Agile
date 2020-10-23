import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import MeanShift
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer

with open('epic.txt') as f:
    documents = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
documents = [x.strip() for x in documents] 

model = Pipeline(
  steps=[
    ('tfidf', TfidfVectorizer()),
    ('trans', FunctionTransformer(lambda x: x.todense(), accept_sparse=True)),
    ('clust', MeanShift())
  ])

model.fit(documents)

result = [(label,doc) for doc,label in zip(documents, model.named_steps['clust'].labels_)]

for label,doc in sorted(result):
  print(label, doc)

labels = model.labels_
cluster_centers = model.cluster_centers_

labels_unique = np.unique(labels)
n_clusters_ = len(labels_unique)

print("number of estimated clusters : %d" % n_clusters_)

order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()
for i in range(n_clusters_):
    print("Cluster %d:" % i),
    for ind in order_centroids[i, :10]:
        print(' %s' % terms[ind]),
    print

Y = vectorizer.transform(["Add a background color to cells that can be any RGB color."])
prediction = model.predict(Y)
print(prediction)

output = []

#for x in range(len(X)):
#

print(X)