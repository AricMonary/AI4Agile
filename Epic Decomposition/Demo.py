# %% Load data
from jange import ops, stream, vis

ds = stream.from_csv(
    "https://raw.githubusercontent.com/jangedoo/jange/master/dataset/bbc.csv",
    columns="news",
    context_column="type",
)

# %% Extract clusters
# Extract clusters
result_collector = {}
clusters_ds = ds.apply(
    ops.text.clean.pos_filter("NOUN", keep_matching_tokens=True),
    ops.text.encode.tfidf(max_features=5000, name="tfidf"),
    ops.cluster.minibatch_kmeans(n_clusters=5),
    result_collector=result_collector,
)

# %% Get features extracted by tfidf
features_ds = result_collector[clusters_ds.applied_ops.find_by_name("tfidf")]

# %% Visualization
reduced_features = features_ds.apply(ops.dim.tsne(n_dim=2))
vis.cluster.visualize(reduced_features, clusters_ds)

# visualization looks good, lets export the operations
with ops.utils.disable_training(cluster_ds.applied_ops) as cluster_ops:
    with open("cluster_ops.pkl", "wb") as f:
        pickle.dump(cluster_ops, f)

# in_another_file.py
# load the saved operations and apply on a new stream to retrieve the clusters
with open("cluster_ops.pkl", "rb") as f:
    cluster_ops = pickle.load(f)

clusters_ds = input_ds.apply(cluster_ops)