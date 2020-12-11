from gensim.models import Word2Vec
import gensim as gensim
import numpy as np
from collections import Counter
import itertools
from sklearn.metrics.pairwise import cosine_similarity


# Split paragraph into an array and eliminate bad sentence
def pre_process_story(story_input):
    story_sentences = story_input.split(".")

    # Remove bad sentences
    for story_sentence in story_sentences:
        if len(story_sentence) < 5:
            story_sentences.remove(story_sentence)

    # Strip white spaces
    for i in range(len(story_sentences)):
        story_sentences[i] = story_sentences[i].strip()

    return story_sentences


# Load Google's pre-trained Word2Vec model.
def load_emb_model(directory):
    word_emb_model = gensim.models.KeyedVectors.load_word2vec_format(directory, binary=True)
    return word_emb_model


# Map words frequency in document
def map_word_frequency(document):
    return Counter(itertools.chain(*document))


# Return the sif feature vectors for two sentences
def get_sif_feature_vectors(sentence1, sentence2, word_emb_model):
    sentence1 = [token for token in sentence1.split() if token in word_emb_model.vocab]
    sentence2 = [token for token in sentence2.split() if token in word_emb_model.vocab]
    word_counts = map_word_frequency((sentence1 + sentence2))
    embedding_size = 300  # size of vector in word embeddings
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


# Return the cosine similarity between two vectors
def get_cosine_similarity(feature_vec_1, feature_vec_2):
    return cosine_similarity(feature_vec_1.reshape(1, -1), feature_vec_2.reshape(1, -1))[0][0]


# Function decision to generate comparison coefficient
def function_decision(story_sentences, word_emb_model):
    my_dict = {}

    for i in range(0, len(story_sentences)):
        for j in range(i + 1, len(story_sentences)):
            feature_vector = get_sif_feature_vectors(story_sentences[i], story_sentences[j], word_emb_model)
            cosine_similarity_value = get_cosine_similarity(feature_vector[0], feature_vector[1])
            my_dict[cosine_similarity_value] = (story_sentences[i], story_sentences[j])
    return my_dict


def generate_stories(stories, coefficient, word_emb_model):
    # Used story set
    used_stories_set = set()

    # Generate comparison coefficient for all sentences
    story_dict = function_decision(stories, word_emb_model)

    # Result list
    result = []

    # Threshold coefficient
    processing_dict = {}
    single_dict = {}

    # Split sentences bases on threshold
    for grade in story_dict:
        if grade > coefficient:
            processing_dict[grade] = story_dict[grade]
        else:
            single_dict[grade] = story_dict[grade]

    # The list that holds all the pairs sentences that need to processing
    # This list can hold duplicates of first sentences
    processing_list = []

    for value in processing_dict.values():
        processing_list.append(value)

    # Iterate through the processing list
    while processing_list:
        # Current new story set
        new_story_set = set()

        # Add all vectors that are related to each other
        for item in processing_list:
            first_vector = item[0]
            second_vector = item[1]
            if not new_story_set:
                # If the set is empty then just add the two vectors
                new_story_set.add(first_vector)
                new_story_set.add(second_vector)

            if first_vector in new_story_set or second_vector in new_story_set:
                # If the set is not empty then only add if one of the vector appears
                # Maintain the relationship between vector pairs
                new_story_set.add(first_vector)
                new_story_set.add(second_vector)

                # Add to the used story set to keep track of the stories
                used_stories_set.add(first_vector)
                used_stories_set.add(second_vector)

        # Remove all trace of vectors already been used
        # Loop through the current new story set
        for sentence_in_new_story_set in new_story_set:
            # Loop through the processing list
            for sentences_pair in processing_list:
                first_sentence = sentences_pair[0]
                second_sentence = sentences_pair[1]
                if first_sentence == sentence_in_new_story_set or second_sentence == sentence_in_new_story_set:
                    processing_list.remove(sentences_pair)

        # Add sentences together to form new user story
        result_story = ""
        for item in stories:
            if item in new_story_set:
                result_story += item + ". "

        result.append(result_story)

    return result, used_stories_set


# Optimize a story with a threshold number using the given Word2Vec model.
def optimize_story(input_story, threshold, directory='./GoogleNews-vectors-negative300.bin'):
    # Load Google's pre-trained Word2Vec model.
    word_emb_model = load_emb_model(directory)

    # Get sentences
    stories = pre_process_story(input_story)

    # Generate optimized stories and used stories
    optimized_stories, used_stories_set = generate_stories(stories, threshold, word_emb_model)

    # Get single stories
    single_stories = set(stories) - used_stories_set

    # Get the result optimized stories
    result = optimized_stories + list(single_stories)

    return result


# story = "The spreadsheet should have Columns A to Z and Rows 1 to 50. The cells should be referenceable from their " \
#          "corresponding name (Example: A1, B42, etc.). Cells can reference other cells for expressions or text. Update " \
#          "cells that are referencing other cells when the referenced cell is updated. Cells should be able to evaluate " \
#          "mathematical statements. Arithmetic expressions are represented as trees. Support for addition, subtraction, " \
#          "multiplication, division, and parentheses. Add a background color to cells that can be any RGB color. Be " \
#          "able to change the background color of many cells at once. Allow for color and text changing to be undone. " \
#          "Be able to redo any undone changes. Allow for the contents of the spreadsheet to be saved. Do not preserve " \
#          "the undo/redo system for when the spreadsheet is saved. Select the folder to save the file in. "
#
# example = optimize_story(story, 0.69)
#
# print(example)


