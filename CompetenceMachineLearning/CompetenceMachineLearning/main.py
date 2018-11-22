import DBhandler
from Competence import Competence
from NumberFormatModel import NumberFormatModel
from ASCIIModel import ASCIIModel
from TokenizerModel import TokenizerModel
import MultipleOutputModel
import tensorflow as tf
from tensorflow import keras
import json
import matplotlib.pyplot as plt

def runLoadedModel(model):
    #training, test = db.loadAdvertData(Competence(12562, "engelsk"))
    training, test = db.loadAdvertData(Competence(13712, "Java (Computerprogrammering)"))
    train_data, train_label, test_data, test_label  = [], [], [], []
    for x in training:
        convert = x.numberFormat_body.split(' ')
        train_data.append(convert)
        train_label.append(x.matchCurrentCompetence)
    for x in test:
        convert = x.numberFormat_body.split(' ')
        test_data.append(convert)
        test_label.append(x.matchCurrentCompetence)
    
    train_data = keras.preprocessing.sequence.pad_sequences(train_data,
                                                            value=0,
                                                            padding='post',
                                                            maxlen=1000)
    test_data = keras.preprocessing.sequence.pad_sequences(test_data,
                                                            value=0,
                                                            padding='post',
                                                            maxlen=1000)
 
    model.compile(optimizer=tf.train.AdamOptimizer(), 
                    loss='binary_crossentropy',
                    metrics=['accuracy'])
    
    results = model.evaluate(test_data, test_label)
    
    print('Test accuracy:', results)

if __name__ == '__main__':
    db = DBhandler.DBHandler()

    # Some kompetence ids for testing: 
    # 13712 - Java (computerprogrammering)
    # 12561 - Dansk
    # 12562 - Engelsk
    # 13737 - C#

    mod = TokenizerModel("Testname", 12562)
    mod.addStandardLayer(32)
    mod.addDropoutLayer(0.1)
    mod.addStandardLayer(32)
    mod.addDropoutLayer(0.1)
    mod.createModel()
    mod.trainModel(1, 15)

    #mod = MultipleOutputModel.MultipleOutputModel()
    #mod.trainModel()

    #model = db.loadKerasModel(13712, "Festabe")
    #runLoadedModel(model)
    



