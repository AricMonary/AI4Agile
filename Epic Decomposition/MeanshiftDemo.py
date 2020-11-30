from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import MeanShift
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer

documents = ['A blind or visually impaired person should be able to navigate inside or outside.', 
'The core emphasis is the safety of the user, the app should be able to avoid obstacles and collisions.',
'The app should accept the users location and preferably suggest a destination based on the users habits.',
'Suggest more than one route to the destination, telling the user to walk a certain distance, calling emergency if app detects a fall, customizable and extensible.',
'App should be able to utilize voice recognition.']

pipeline = Pipeline(
  steps=[
    ('tfidf', TfidfVectorizer()),
    ('trans', FunctionTransformer(lambda x: x.todense(), accept_sparse=True)),
    ('clust', MeanShift())
  ])

pipeline.fit(documents)
pipeline.named_steps['clust'].labels_

result = [(label,doc) for doc,label in zip(documents, pipeline.named_steps['clust'].labels_)]

for label,doc in sorted(result):
  print(label, doc)