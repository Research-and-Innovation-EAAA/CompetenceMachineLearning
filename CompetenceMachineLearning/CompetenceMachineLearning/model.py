import tensorflow as tf
from tensorflow import keras
import numpy as np
import random

class Model:

    layerArray = []

    def addStandardLayer(self, units):
        layer = keras.layers.Dense(units, activation=tf.nn.relu)
        self.layerArray.append(layer)

    def createModel(self):
        train_data = []
        train_label = []
        test_data = []
        test_label = []
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
        train_data = keras.preprocessing.sequence.pad_sequences(train_data,
                                                                value='index for padding is writte here, should come from dictionary',
                                                                padding='post',
                                                                maxlen=256)

        test_data = keras.preprocessing.sequence.pad_sequences(train_data,
                                                                value='index for padding is writte here, should come from dictionary',
                                                                padding='post',
                                                                maxlen=256)

        vocab_size = 1000
        model = keras.Sequential()
        model.add(keras.layers.Embedding(vocab_size, 3))
        model.add(keras.layers.GlobalAveragePooling1D())
        #model.add(keras.layers.Dense(1, input_shape=(2,), activation=tf.nn.relu))
        if len(self.layerArray) != 0:
            for x in self.layerArray:
                model.add(x)
        model.add(keras.layers.Dense(10, activation=tf.nn.sigmoid))
        model.summary()

        model.compile(optimizer=tf.train.AdamOptimizer(), 
                    loss='sparse_categorical_crossentropy',
                    metrics=['accuracy'])

        #model.fit(trainingSet, trainingLabels, epochs = 20)

        #results = model.evaluate(testSet, testLabels)

        print('Test accuracy:', results)
