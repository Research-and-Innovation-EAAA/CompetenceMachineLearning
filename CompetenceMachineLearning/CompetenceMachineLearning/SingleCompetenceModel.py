import DBhandler
import tensorflow as tf
from tensorflow import keras

class SingleCompetenceModel(object):
    layerArray = []
    model = None
    name = ""
    modelType = None
    competenceID = 0
    db = None

    def __init__(self, name, competenceID):
        self.name = name
        self.competenceID = competenceID
        self.db = DBhandler.DBHandler()

    def addStandardLayer(self, units):
        layer = keras.layers.Dense(units, activation=tf.nn.relu)
        self.layerArray.append(layer)

    def addDropoutLayer(self, percentage):
        layer = keras.layers.Dropout(percentage)
        self.layerArray.append(layer)

    #TODO: See how much of trainModel is shared and put it into this superclass somehow.

    def saveModel(self):
        self.db.saveModel(self.name, self.modelType, self.model, self.competenceID)
        
    @staticmethod
    def loadModel(competenceID, name, type):
        if type == "Multi":
            raise Exception("Error: Wrong class, do not load a multipleOutputModel in SingleCompetenceModel.")
        db = DBhandler.DBHandler()
        from ASCIIModel import ASCIIModel
        from NumberFormatModel import NumberFormatModel
        from TokenizerModel import TokenizerModel
        model = db.loadModel(competenceID, name, type)
        mod = None
        if type == "ASCII":
            mod = ASCIIModel(name, competenceID)
        elif type == "NumberFormatted":
            mod = NumberFormatModel(name, competenceID)
        elif type == "Tokenized":
            mod = TokenizerModel(name, competenceID)
        else:
            raise Exception("Error: Unknown Model Type.")

        model.compile(optimizer=tf.train.AdamOptimizer(), 
                    loss='binary_crossentropy',
                    metrics=['accuracy'])
        mod.model = model
        return mod






