import DBhandler

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
        db = DBhandler.DBHandler()

    def addStandardLayer(self, units):
        layer = keras.layers.Dense(units, activation=tf.nn.relu)
        self.layerArray.append(layer)

    def addDropoutLayer(self, percentage):
        layer = keras.layers.Dropout(percentage)
        self.layerArray.append(layer)

    #TODO: See how much of trainModel is shared and put it into this superclass somehow.

    def saveModel(self):
        db.saveModel(name, modelType, model, competenceID)
        
    @staticmethod
    def loadModel(competenceID, name, type):
        db = DBhandler.DBHandler()
        from ASCIIModel import ASCIIModel
        from NumberFormatModel import NumberFormatModel
        model = db.loadModel(competenceID, name)
        mod = None
        if type == "ASCII":
            mod = ASCIIModel(name, competenceID)
        elif type == "NumberFormatted":
            mod = NumberFormatModel(name, competenceID)
        elif type == "Tokenized":
            raise Exception("ERROR: WIP, FINISH THE CODE YA DINGUS")
        elif type == "Multi":
            raise Exception("Error: Wrong class, do not load a multipleOutputModel in SingleCompetenceModel.")
        else:
            raise Exception("Error: Unknown Model Type.")

        mod.model = model

        return mod






