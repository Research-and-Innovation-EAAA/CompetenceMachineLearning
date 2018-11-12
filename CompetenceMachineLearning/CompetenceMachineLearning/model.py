import tensorflow as tf
from tensorflow import keras
import numpy as np
import random
import DBhandler
from Competence import Competence

class Model:

    layerArray = []

    def addStandardLayer(self, units):
        layer = keras.layers.Dense(units, activation=tf.nn.relu)
        self.layerArray.append(layer)

    def createModel(self):
        db = DBhandler.DBHandler()
        training, test = db.loadAdvertData(Competence(13712, "Java (Computerprogrammering)"))
        train_data, train_label, test_data, test_label  = [], [], [], []
        for x in training:
            convert = x.numberFormat_body.split(' ')
            while len(convert) < 1000:
                convert.append(0)
            train_data.append(convert[:1000])
            train_label.append(x.matchCurrentCompetence)
        for x in test:
            convert = x.numberFormat_body.split(' ')
            while len(convert) < 1000:
                convert.append(0)
            test_data.append(convert[:1000])
            test_label.append(x.matchCurrentCompetence)
        #trainingSet = []
        #trainingLabels = []
        #testSet = []
        #testLabels = []

        #for i in range(50000):
        #    x = random.randint(0, 1)
        #    y = random.randint(0, 1)
        #    trainingSet.append([x, y])
        #    if (x == 1 & y == 0) | (x == 0 & y == 1):
        #        trainingLabels.append(1)
        #    else:
        #        trainingLabels.append(0)
        #for i in range(1000):
        #    x = random.randint(0, 1)
        #    y = random.randint(0, 1)
        #    testSet.append([x, y])
        #    if (x == 1 & y == 0) | (x == 0 & y == 1):
        #        testLabels.append(1)
        #    else:
        #        testLabels.append(0)
        #trainingSet = np.array(trainingSet)
        #trainingLabels = np.array(trainingLabels)
        #testSet = np.array(testSet)
        #testLabels = np.array(testLabels)
        print(len(test_data))
        print(len(test_label))
        
        train_data = keras.preprocessing.sequence.pad_sequences(train_data,
                                                                value=0,
                                                                padding='post',
                                                                maxlen=256)

        test_data = keras.preprocessing.sequence.pad_sequences(test_data,
                                                                value=0,
                                                                padding='post',
                                                                maxlen=256)
        train_data = np.array(train_data)
        train_label = np.array(train_label)
        test_data = np.array(test_data)
        test_label = np.array(test_label)

        vocab_size = 1000000
        model = keras.Sequential()
        model.add(keras.layers.Embedding(vocab_size, 3))
        model.add(keras.layers.GlobalAveragePooling1D())
        if len(self.layerArray) != 0:
            for x in self.layerArray:
                model.add(x)
        model.add(keras.layers.Dense(10, activation=tf.nn.sigmoid))
        model.summary()

        model.compile(optimizer=tf.train.AdamOptimizer(), 
                    loss='sparse_categorical_crossentropy',
                    metrics=['accuracy'])

        model.fit(train_data, train_label, epochs = 20)
        print(len(test_data))
        print(len(test_label))


      

        results = model.evaluate(test_data, test_label)

        print('Test accuracy:', results)
