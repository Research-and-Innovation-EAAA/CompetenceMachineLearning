import tensorflow as tf
from tensorflow import keras
import numpy as np
import random
import DBhandler
from Competence import Competence
from SingleCompetenceModel import SingleCompetenceModel
from sklearn.preprocessing import LabelBinarizer, LabelEncoder

class TokenizerModel(SingleCompetenceModel): 

    def __init__(self, name, competenceID):
        SingleCompetenceModel.__init__(self, name, competenceID)
        self.modelType = "Tokenized"
        db = DBhandler.DBHandler()

    def createModel(self):
        db = DBhandler.DBHandler()
        vocab_size = db.loadDictionaryLength()
        model = keras.Sequential()
        # Vocab size is increase to prevent a bug where an advert uses the highest id, for some reason this crashed the fitting.
        #model.add(keras.layers.Embedding(vocab_size + 100, 3, input_length=1000))
        #model.add(keras.layers.GlobalAveragePooling1D())
        model.add(keras.layers.Dense(20, input_shape=(1000,), activation=tf.nn.relu))
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
            #convert = x.body.split(' ')
            #train_data.append(convert)
            train_data.append(x.body)
            train_label.append(x.matchCurrentCompetence)
        for x in test:
            #convert = x.body.split(' ')
            #test_data.append(convert)
            test_data.append(x.body)
            test_label.append(x.matchCurrentCompetence)
            
        max_words = 1000
        tokenize = keras.preprocessing.text.Tokenizer(num_words=max_words, char_level=False)
        tokenize.fit_on_texts(train_data) # only fit on train

        x_train = tokenize.texts_to_matrix(train_data)
        x_test = tokenize.texts_to_matrix(test_data)

        #encoder = LabelEncoder()
        #encoder.fit(train_label)
        #y_train = encoder.transform(train_label)
        #y_test = encoder.transform(test_label)
        
        #num_classes = np.max(y_train) + 1

        #y_train = keras.utils.to_categorical(y_train, num_classes)
        #y_test = keras.utils.to_categorical(y_test, num_classes)

        print(len(train_data))

        #train_data = keras.preprocessing.sequence.pad_sequences(train_data,
        #                                                        value=0,
        #                                                        padding='post',
        #                                                        maxlen=1000)

        #test_data = keras.preprocessing.sequence.pad_sequences(test_data,
        #                                                        value=0,
        #                                                        padding='post',
        #                                                        maxlen=1000)

        self.model.compile(optimizer=tf.train.AdamOptimizer(), 
                    loss='binary_crossentropy',
                    metrics=['accuracy'])

        #train_data_1 = int((len(train_data)*(1/10)))
        #train_label_1 = int((len(train_label)*(1/10)))
        

        #x_val = train_data[:train_data_1]
        #partial_x_train = train_data[train_data_1:]

        #y_val = train_label[:train_label_1]
        #partial_y_train = train_label[train_label_1:]

        history = self.model.fit(x_train, train_label, epochs = int(epochs), verbose=int(verboseMod), validation_split=0.1)

        results = self.model.evaluate(x_test, test_label)

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