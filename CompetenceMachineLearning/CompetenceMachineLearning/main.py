import DBhandler
from Competence import Competence
from SingleCompetenceModel import SingleCompetenceModel
from NumberFormatModel import NumberFormatModel
from ASCIIModel import ASCIIModel
from TokenizerModel import TokenizerModel
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
        raise Exception("Error: Not implemented")
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

    mod = TokenizerModel("Testname", 12562)
    mod.addStandardLayer(32)
    mod.addDropoutLayer(0.1)
    mod.addStandardLayer(32)
    mod.addDropoutLayer(0.1)
    mod.createModel()
    mod.trainModel(1, 10)
    
    mod.saveModel()

    #mod = MultipleOutputModel.MultipleOutputModel()
    #mod.trainModel()

    #mod = SingleCompetenceModel.loadModel(13712, "Testname", "NumberFormatted")
    #testLoadedModel(mod)
    



