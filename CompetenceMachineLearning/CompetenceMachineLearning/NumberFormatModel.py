import tensorflow as tf
from tensorflow import keras
import numpy as np
import random
import DBhandler
from Competence import Competence
from SingleCompetenceModel import SingleCompetenceModel

class NumberFormatModel(SingleCompetenceModel):

    def __init__(self, name, competenceID):
        SingleCompetenceModel.__init__(self, name, competenceID)
        self.modelType = "NumberFormatted"
        db = DBhandler.DBHandler()

    def createModel(self):
        db = DBhandler.DBHandler()
        vocab_size = db.loadDictionaryLength()
        model = keras.Sequential()
        # Vocab size is increase to prevent a bug where an advert uses the highest id, for some reason this crashed the fitting.
        model.add(keras.layers.Embedding(vocab_size + 100, 3, input_length=1000))
        model.add(keras.layers.GlobalAveragePooling1D())
        if len(self.layerArray) != 0:
            for x in self.layerArray:
                model.add(x)
        model.add(keras.layers.Dense(1, activation=tf.nn.sigmoid))
        model.summary()
        self.model = model

    def trainModel(self, verboseMod, epochs):
        training, test = self.db.loadAdvertDataNumberFormat(self.competenceID)
        train_data, train_label, test_data, test_label  = [], [], [], []
        for x in training:
            convert = x.numberFormat_body.split(' ')
            train_data.append(convert)
            train_label.append(x.matchCurrentCompetence)
        for x in test:
            convert = x.numberFormat_body.split(' ')
            test_data.append(convert)
            test_label.append(x.matchCurrentCompetence)
        
        print(len(train_data))

        train_data = keras.preprocessing.sequence.pad_sequences(train_data,
                                                                value=0,
                                                                padding='post',
                                                                maxlen=1000)

        test_data = keras.preprocessing.sequence.pad_sequences(test_data,
                                                                value=0,
                                                                padding='post',
                                                                maxlen=1000)

        self.model.compile(optimizer=tf.train.AdamOptimizer(), 
                    loss='binary_crossentropy',
                    metrics=['accuracy'])

        train_data_1 = int((len(train_data)*(1/10)))
        train_label_1 = int((len(train_label)*(1/10)))
        

        x_val = train_data[:train_data_1]
        partial_x_train = train_data[train_data_1:]

        y_val = train_label[:train_label_1]
        partial_y_train = train_label[train_label_1:]

        history = self.model.fit(partial_x_train, partial_y_train, epochs = int(epochs), verbose=int(verboseMod), validation_data=(x_val, y_val))

        results = self.model.evaluate(test_data, test_label)

        print('Test accuracy:', results)

        #db.saveModel("BananFlue1337", self.model, 12562)

        history_dict = history.history
        history_dict.keys()

        import matplotlib.pyplot as plt
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
        acc_values = history_dict['acc']
        val_acc_values = history_dict['val_acc']

        plt.plot(epochs, acc, 'bo', label='Training acc')
        plt.plot(epochs, val_acc, 'b', label='Validation acc')
        plt.title('Training and validation accuracy')
        plt.xlabel('Epochs')
        plt.ylabel('Accuracy')
        plt.legend()

        plt.show()


