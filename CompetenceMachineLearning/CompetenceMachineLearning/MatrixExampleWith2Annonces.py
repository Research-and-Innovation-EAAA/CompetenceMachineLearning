import tensorflow as tf
from tensorflow import keras
import numpy as np
import random
import DBhandler
import os

from Competence import Competence
from SingleCompetenceModel import SingleCompetenceModel
from sklearn.preprocessing import LabelBinarizer, LabelEncoder

class MatrixExampleWith2Annonces():

    def printMatrix(self):
        twoAnnonces = ["Søger datamatiker, du skal have færdigheder indenfor programmering, bla. Java, C#, JavaScrip m.m.", 
                       "Søger IT-Support. Som en del a jobbet vil din opgave være at afhjælper kunderne med deres IT problemer"]
        max_words = 10
        tokenize = keras.preprocessing.text.Tokenizer(num_words=max_words, char_level=False)
        tokenize.fit_on_texts(twoAnnonces)
        print("WORD Count: " + str(tokenize.word_counts) + "\n")
        print("Number of Annonces: " + str(tokenize.document_count) + "\n" )
        print("Word Index: " + str(tokenize.word_index) + "\n")
        print("Word Docs: " + str(tokenize.word_docs) + "\n")

        encoded_docs = tokenize.texts_to_matrix(twoAnnonces)
        print(encoded_docs)
