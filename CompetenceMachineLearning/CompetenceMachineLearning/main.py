import DBhandler
from Competence import Competence
from SingleCompetenceModel import SingleCompetenceModel
from NumberFormatModel import NumberFormatModel
from ASCIIModel import ASCIIModel
from TokenizerDenseModel import TokenizerDenseModel
from TokenizerLSTMModel import TokenizerLSTMModel
from MatrixExampleWith2Annonces import MatrixExampleWith2Annonces
import MultipleOutputModel
import tensorflow as tf
from tensorflow import keras
import json
import matplotlib.pyplot as plt

def testLoadedModel(mod):
    test_data, test_label  = [], []
    if mod.modelType == "ASCII":
        training, test = db.loadAdvertDataASCII(mod.competenceID)
        for x in test:
            test_data.append(x.body)
            test_label.append(x.matchCurrentCompetence)
        test_data = keras.preprocessing.sequence.pad_sequences(test_data, value=32, padding='post', maxlen=2500)
    elif mod.modelType == "NumberFormatted":
        training, test = db.loadAdvertDataNumberFormat(mod.competenceID)
        for x in test:
            convert = x.numberFormat_body.split(' ')
            test_data.append(convert)
            test_label.append(x.matchCurrentCompetence)
        test_data = keras.preprocessing.sequence.pad_sequences(test_data, value=0, padding='post', maxlen=1000)
    elif mod.modelType == "Tokenized":
        training, test = self.db.loadAdvertDataTokenizer(self.competenceID)
        for x in test:
            test_data.append(x.body)
            test_label.append(x.matchCurrentCompetence)
        tokenize = keras.preprocessing.text.Tokenizer(1000, char_level=False)
        x_test = tokenize.texts_to_matrix(test_data)
    elif mod.modelType == "Multi":
        raise Exception("Error: Not implemented")
    else:
        raise Exception("Error: Unknown Model Type.")
    
    results = mod.model.evaluate(test_data, test_label)
    print('Test accuracy:', results)

if __name__ == '__main__':
    db = DBhandler.DBHandler()

    # Some kompetence ids for testing: 
    # 13712 - Java (computerprogrammering)
    # 12561 - Dansk
    # 12562 - Engelsk
    # 13737 - C#
    # 13721 - Erlang        |Example chosen for the little amount of data, for error finding|
    # 13013 - værdier
    # 13727 - JavaScript

    mod = TokenizerDenseModel("Javascript Test", 13727)
    mod.addDropoutLayer(0.2)
    mod.createModel()
    mod.trainModel(1, 20)

    #mod.saveModel()

    #mod2 = SingleCompetenceModel.loadModel(13727, "Javascript Test", "Tokenized")
    training, test = db.loadAdvertDataTokenizer(mod2.competenceID)
    data = training + test
    bodies, ids   = [], []

    for x in data:
        bodies.append(x.body)
        ids.append(x._id)

    mod.match(bodies, ids)



