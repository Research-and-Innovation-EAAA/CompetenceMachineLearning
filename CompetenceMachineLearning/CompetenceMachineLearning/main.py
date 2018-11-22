import DBhandler
from Competence import Competence
from NumberFormatModel import NumberFormatModel
from ASCIIModel import ASCIIModel
import MultipleOutputModel
import tensorflow as tf
from tensorflow import keras
import json
import matplotlib.pyplot as plt
from SingleCompetenceModel import SingleCompetenceModel

def testLoadedModel(mod):
    test = None
    if mod.modelType == "ASCII":
        raise Exception("Error: Not implemented, Sync & use the new method name")
    elif mod.modelType == "NumberFormatted":
        training, test = db.loadAdvertDataNumberFormat(mod.competenceID)
    elif mod.modelType == "Tokenized":
        raise Exception("Error: Not implemented")
    elif mod.modelType == "Multi":
        raise Exception("Error: Not implemented")
    else:
        raise Exception("Error: Unknown Model Type.")
    
    test_data, test_label  = [], []
    for x in test:
        convert = x.numberFormat_body.split(' ')
        test_data.append(convert)
        test_label.append(x.matchCurrentCompetence)
    test_data = keras.preprocessing.sequence.pad_sequences(test_data,
                                                            value=0,
                                                            padding='post',
                                                            maxlen=1000)
    
    results = mod.model.evaluate(test_data, test_label)
    
    print('Test accuracy:', results)

if __name__ == '__main__':
    db = DBhandler.DBHandler()

    # Some kompetence ids for testing: 
    # 13712 - Java (computerprogrammering)
    # 12561 - Dansk
    # 12562 - Engelsk
    # 13737 - C#

    #mod = NumberFormatModel("Testname", 13712)
    #mod.addStandardLayer(32)
    #mod.addDropoutLayer(0.1)
    #mod.addStandardLayer(32)
    #mod.addDropoutLayer(0.1)
    #mod.createModel()
    #mod.trainModel(1, 15)
    #mod.saveModel()

    #mod = MultipleOutputModel.MultipleOutputModel()
    #mod.trainModel()

    mod = SingleCompetenceModel.loadModel(13712, "Testname", "NumberFormatted")
    testLoadedModel(mod)
    



