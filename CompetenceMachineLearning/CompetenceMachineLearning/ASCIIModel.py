import numpy
import random
import DBhandler
from Competence import Competence
import matplotlib.pyplot as plt
from SingleCompetenceModel import SingleCompetenceModel
import tensorflow as tf
from tensorflow import keras
import os


class ASCIIModel(SingleCompetenceModel):

    
    def __init__(self, name, competenceID):
        SingleCompetenceModel.__init__(self, name, competenceID)
        self.modelType = "ASCII"

    def createModel(self):
        model = keras.Sequential()
        model.add(keras.layers.Embedding(256, 3, input_length=2500))
        model.add(keras.layers.GlobalAveragePooling1D())
        if len(self.layerArray) != 0:
            for x in self.layerArray:
                model.add(x)
        model.add(keras.layers.Dense(1, activation=tf.nn.sigmoid))
        model.summary()
        self.model = model

    def trainModel(self, verboseMod, epoch ):
        training, test = self.db.loadAdvertDataASCII(self.competenceID)

        train_data, train_label, test_data, test_label  = [], [], [], []
        for x in training:
            train_data.append(x.body)
            train_label.append(x.matchCurrentCompetence)
        for x in test:
            test_data.append(x.body)
            test_label.append(x.matchCurrentCompetence)
        

        train_data = keras.preprocessing.sequence.pad_sequences(train_data,
                                                            value=32,
                                                            padding='post',
                                                            maxlen=2500)

        test_data = keras.preprocessing.sequence.pad_sequences(test_data,
                                                            value=32,
                                                            padding='post',
                                                            maxlen=2500)


        self.model.compile(optimizer=tf.train.AdamOptimizer(),
                  loss='binary_crossentropy',
                  metrics=['accuracy'])

        train_data_1 = int((len(train_data)*(1/10)))
        train_label_1 = int((len(train_label)*(1/10)))
      

        x_val = train_data[:train_data_1]
        partial_x_train = train_data[train_data_1:]
    
        y_val = train_label[:train_label_1]
        partial_y_train = train_label[train_label_1:]

        history = self.model.fit(partial_x_train, 
                            partial_y_train, 
                            epochs = epoch, 
                            verbose= verboseMod,
                            validation_data=(x_val, y_val))

        results = self.model.evaluate(test_data, test_label)
        print(results)

        acc = history.history['acc']
        val_acc = history.history['val_acc']
        loss = history.history['loss']
        val_loss = history.history['val_loss']
        epochs = range(1, len(acc) + 1)
    
        # "bo" is for "blue dot"
        plt.plot(epochs, loss, 'bo', label='Training loss')
    
        # b is for "solid blue line"
        plt.plot(epochs, val_loss, 'b', label='Validation loss')
        plt.title('Training and validation loss')
        plt.xlabel('Epochs')
        plt.ylabel('Loss')
        plt.legend()

        plt.show()

        plt.clf()   # clear figure

        plt.plot(epochs, acc, 'bo', label='Training acc')
        plt.plot(epochs, val_acc, 'b', label='Validation acc')
        plt.title('Training and validation accuracy')
        plt.xlabel('Epochs')
        plt.ylabel('Accuracy')
        plt.legend()

        plt.show()

