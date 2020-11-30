from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.preprocessing import StandardScaler

with open('epic.txt') as f:
    documents = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
documents = [x.strip() for x in documents] 

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(documents)

print(X.vocabulary_)

model = DBSCAN(eps=0.3, min_samples=2).fit(X)
clusterCount = model.labels_.size
labels = model.labels_

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
n_noise_ = list(labels).count(-1)

print('Estimated number of clusters: %d' % n_clusters_)
print('Estimated number of noise points: %d' % n_noise_)
#print("Homogeneity: %0.3f" % metrics.homogeneity_score(X, labels))
#print("Completeness: %0.3f" % metrics.completeness_score(X, labels))
#print("V-measure: %0.3f" % metrics.v_measure_score(X, labels))
#print("Adjusted Rand Index: %0.3f" % metrics.adjusted_rand_score(X, labels))
#print("Adjusted Mutual Information: %0.3f" % metrics.adjusted_mutual_info_score(X, labels))
#print("Silhouette Coefficient: %0.3f" % metrics.silhouette_score(X, labels))

#print("Clusters:")
#results = model.components_
#terms = vectorizer.get_feature_names()

#for i in range(clusterCount):
#    print("Cluster %s:" % (i + 1))
#    for j in range(results.toarray()[i].size):
#        if results.toarray()[i][j] != 0:
#            print(terms[j])
#    print()

#print("Prediction")

#Y = vectorizer.transform(["Add a background color to cells that can be any RGB color."])
#prediction = model.predict(Y)
#print(prediction)

#Y = vectorizer.transform(["The spreadsheet should have Columns A to Z and Rows 1 to 50."])
#prediction = model.predict(Y)
#print(prediction)