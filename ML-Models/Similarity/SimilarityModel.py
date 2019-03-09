import numpy as np
from scipy import spatial
from gensim.models import KeyedVectors
import os
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def avg_feature_vector(sentence, model, num_features, index2word_set):
    words = sentence.split()
    feature_vec = np.zeros((num_features, ), dtype='float32')
    n_words = 0
    for word in words:
        if word in index2word_set:
            n_words += 1
            feature_vec = np.add(feature_vec, model[word])
    if (n_words > 0):
        feature_vec = np.divide(feature_vec, n_words)
    return feature_vec

def loadModel():
    model = KeyedVectors.load(ROOT_DIR+"/model.bin")
    index2word_set = set(model.wv.index2word)
    print("Loaded Model")
    return model, index2word_set


def predict(model, index2word_set, sentence1, sentence2):
    s1_afv = avg_feature_vector(sentence1, model=model, num_features=150, index2word_set=index2word_set)
    s2_afv = avg_feature_vector(sentence2, model=model, num_features=150, index2word_set=index2word_set)
    sim = 1 - spatial.distance.cosine(s1_afv, s2_afv)
    return round(sim * 100, 2)

