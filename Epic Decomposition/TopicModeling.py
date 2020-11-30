from collections import defaultdict
from gensim import corpora

documents = ['Any changes on the spreadsheet should be resolved instantaneously.',
             'Run as an independent application on Windows.',
             'Update cells that are referencing other cells when the referenced cell is updated.',
             'Allow for the contents of the spreadsheet to be saved.',
             'Allow for color and text changing to be undone.',
             'Add a background color to cells that can be any RGB color.',
             'Cells should be able to evaluate mathematical statements.'
            ]

# remove common words and tokenize
stoplist = set('for a of the and to in'.split())
texts = [
    [word for word in document.lower().split() if word not in stoplist]
    for document in documents
]

# remove words that appear only once
frequency = defaultdict(int)
for text in texts:
    for token in text:
        frequency[token] += 1

texts = [
    [token for token in text if frequency[token] > 1]
    for text in texts
]

dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]

from gensim import models

tfidf = models.TfidfModel(corpus)  # step 1 -- initialize a model

doc_bow = [(0, 1), (1, 1)]
print(tfidf[doc_bow])  # step 2 -- use the model to transform vectors

corpus_tfidf = tfidf[corpus]
for doc in corpus_tfidf:
    print(doc)

lsi_model = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=3)  # initialize an LSI transformation
corpus_lsi = lsi_model[corpus_tfidf]  # create a double wrapper over the original corpus: bow->tfidf->fold-in-lsi

lsi_model.print_topics(2)

Hdp_model = models.HdpModel(corpus, id2word=dictionary)
corpus_Hdp = Hdp_model[corpus_tfidf]

# both bow->tfidf and tfidf->lsi transformations are actually executed here, on the fly
for doc, as_text in zip(Hdp_model, documents):
    print(doc, as_text)