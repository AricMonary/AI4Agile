import shutil

import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from tensorflow.python import platform
from unidecode import unidecode
import string


def pre_process(corpus):
    # convert input corpus to lower case.
    corpus = corpus.lower()
    # collecting a list of stop words from nltk and punctuation form
    # string class and create single array.
    stopset = stopwords.words('english') + list(string.punctuation)
    # remove stop words and punctuations from string.
    # word_tokenize is used to tokenize the input corpus in word tokens.
    corpus = " ".join([i for i in word_tokenize(corpus) if i not in stopset])
    # remove non-ascii characters
    corpus = unidecode(corpus)
    return corpus


print(pre_process("Sample of non ASCII: Ceñía. How to remove stopwords and punctuations?"))

from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

lemmatizer = WordNetLemmatizer()
sentence = "The striped bats are hanging on their feet for best"
words = word_tokenize(sentence)

from sklearn.feature_extraction.text import TfidfVectorizer

# sentence pair
corpus = ["A girl is styling her hair.", "A girl is brushing her hair."]
for c in range(len(corpus)):
    corpus[c] = pre_process(corpus[c])
# creating vocabulary using uni-gram and bi-gram
tfidf_vectorizer = TfidfVectorizer(ngram_range=(1, 2))
tfidf_vectorizer.fit(corpus)

feature_vectors = tfidf_vectorizer.transform(corpus)

from gensim.models import Word2Vec
import gensim as gensim
import numpy as np

# Load Google's pre-trained Word2Vec model.
word_emb_model = gensim.models.KeyedVectors.load_word2vec_format('./GoogleNews-vectors-negative300.bin', binary=True)

from collections import Counter
import itertools


def map_word_frequency(document):
    return Counter(itertools.chain(*document))


def get_sif_feature_vectors(sentence1, sentence2, word_emb_model=word_emb_model):
    sentence1 = [token for token in sentence1.split() if token in word_emb_model.vocab]
    sentence2 = [token for token in sentence2.split() if token in word_emb_model.vocab]
    word_counts = map_word_frequency((sentence1 + sentence2))
    embedding_size = 300  # size of vectore in word embeddings
    a = 0.001
    sentence_set = []
    for sentence in [sentence1, sentence2]:
        vs = np.zeros(embedding_size)
        sentence_length = len(sentence)
        for word in sentence:
            a_value = a / (a + word_counts[word])  # smooth inverse frequency, SIF
            vs = np.add(vs, np.multiply(a_value, word_emb_model[word]))  # vs += sif * word_vector
        vs = np.divide(vs, sentence_length)  # weighted average
        sentence_set.append(vs)
    return sentence_set


from sklearn.metrics.pairwise import cosine_similarity


def get_cosine_similarity(feature_vec_1, feature_vec_2):
    return cosine_similarity(feature_vec_1.reshape(1, -1), feature_vec_2.reshape(1, -1))[0][0]


# print("Comparison")
#
# vector1 = "The spreadsheet should have Columns A to Z and Rows 1 to 50."
#
# vector2 = "The cells should be referencable from their corresponding name (Example: A1, B42, etc.)."
#
# vector3 = "Cells can reference other cells for expressions or text."
#
# vector4 = "Update cells that are referencing other cells when the referenced cell is updated."
#
# print("Get feature vector 1 and 2")
# feature_vector12 = get_sif_feature_vectors(vector1, vector2, word_emb_model)
# print("Get comparison between 1 and 2")
# print(get_cosine_similarity(feature_vector12[0], feature_vector12[1]))
#
# print("Get feature vector 1 and 3")
# feature_vector13 = get_sif_feature_vectors(vector1, vector3, word_emb_model)
# print("Get comparison between 1 and 3")
# print(get_cosine_similarity(feature_vector13[0], feature_vector13[1]))
#
# print("Get feature vector 1 and 4")
# feature_vector14 = get_sif_feature_vectors(vector1, vector4, word_emb_model)
# print("Get comparison between 1 and 4")
# print(get_cosine_similarity(feature_vector14[0], feature_vector14[1]))

# Split paragraph into an array and eliminate bad sentence
def pre_process_story(story):
    story_sentences = story.split(".")

    # Remove bad sentences
    for story_sentence in story_sentences:
        if len(story_sentence) < 5:
            story_sentences.remove(story_sentence)

    return story_sentences

# Function decision to generate comparison coefficient
def function_decision(story_sentences):
    my_dict = {}

    for i in range(0, len(story_sentences)):
        for j in range(i + 1, len(story_sentences)):
            feature_vector = get_sif_feature_vectors(story_sentences[i], story_sentences[j], word_emb_model)
            cosine_similarity = get_cosine_similarity(feature_vector[0], feature_vector[1])
            my_dict[cosine_similarity] = (story_sentences[i], story_sentences[j])
    return my_dict

story = "The spreadsheet should have Columns A to Z and Rows 1 to 50. The cells should be referencable from their " \
        "corresponding name (Example: A1, B42, etc.). Cells can reference other cells for expressions or text." \
        "Update cells that are referencing other cells when the referenced cell is updated. "

print(pre_process_story(story))
print(len(pre_process_story(story)))

stories = pre_process_story(story)

# Generate comaprison coefficient for all sentences
story_dict = function_decision(stories)
for thing in story_dict:
    print(thing)

# Threshold coefficient
coefficient = 0.65
processing_dict = {}
single_dict = {}

# Split sentences bases on threshold
for grade in story_dict:
    if grade > coefficient:
        processing_dict[grade] = story_dict[grade]
    else:
        single_dict[grade] = story_dict[grade]

for thing in processing_dict:
    print(thing)

# Generate new sentence
new_story_set = set()

# Use original sentence to keep the order of the sentences
for thing in processing_dict.values():
    new_story_set.add(thing[0])
    new_story_set.add(thing[1])

print(new_story_set)

# Add sentences together to form new user story
result_story = ""
for thing in stories:
    if thing in new_story_set:
        result_story += thing + ". "

print(result_story)



