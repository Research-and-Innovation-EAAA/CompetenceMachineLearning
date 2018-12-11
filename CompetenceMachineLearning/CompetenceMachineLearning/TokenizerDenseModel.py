import tensorflow as tf
from tensorflow import keras
import numpy as np
import random
import DBhandler
import os

from Competence import Competence
from SingleCompetenceModel import SingleCompetenceModel
from sklearn.preprocessing import LabelBinarizer, LabelEncoder

class TokenizerDenseModel(SingleCompetenceModel): 

    def __init__(self, name, competenceID):
        SingleCompetenceModel.__init__(self, name, competenceID)
        self.modelType = "Tokenized"
        db = DBhandler.DBHandler()

    def createModel(self):
        model = keras.Sequential()
        model.add(keras.layers.Dense(4, input_shape=(1000,), activation=tf.nn.relu))
        if len(self.layerArray) != 0:
            for x in self.layerArray:
                model.add(x)
        model.add(keras.layers.Dense(1, activation=tf.nn.sigmoid))
        model.summary()
        self.model = model

    def trainModel(self, verboseMod, epochs):
        training, test = self.db.loadAdvertDataTokenizer(self.competenceID)
        train_data, train_label, test_data, test_label  = [], [], [], []


        for x in training:
            train_data.append(x.body)
            train_label.append(x.matchCurrentCompetence)
        for x in test:
            test_data.append(x.body)
            test_label.append(x.matchCurrentCompetence)
            
        max_words = 1000
        tokenize = keras.preprocessing.text.Tokenizer(num_words=max_words, char_level=False)
        tokenize.fit_on_texts(train_data) # only fit on train

        x_train = tokenize.texts_to_matrix(train_data)
        x_test = tokenize.texts_to_matrix(test_data)
        
        print(len(train_data))
        self.model.compile(optimizer=tf.train.AdamOptimizer(), 
                    loss='binary_crossentropy',
                    metrics=['accuracy'])

        train_data_1 = int((len(x_train)*(1/10)))
        train_label_1 = int((len(train_label)*(1/10)))

        x_val = x_train[:train_data_1]
        partial_x_train = x_train[train_data_1:]

        y_val = train_label[:train_label_1]
        partial_y_train = train_label[train_label_1:]

        checkpoint_path = "training_1/cp.ckpt"
        checkpoint_dir = os.path.dirname(checkpoint_path)

        # Create checkpoint callback
        cp_callback = tf.keras.callbacks.ModelCheckpoint(checkpoint_path, 
                                                 save_weights_only=True,
                                                 verbose=1)
        history = self.model.fit(partial_x_train, partial_y_train, epochs = int(epochs), verbose=int(verboseMod), validation_data=(x_val, y_val), callbacks = [cp_callback])

        results = self.model.evaluate(x_test, test_label)

        print('Test accuracy:', results)


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

        plt.plot(epochs, acc, 'bo', label='Training acc')
        plt.plot(epochs, val_acc, 'b', label='Validation acc')
        plt.title('Training and validation accuracy')
        plt.xlabel('Epochs')
        plt.ylabel('Accuracy')
        plt.legend()

        plt.show()