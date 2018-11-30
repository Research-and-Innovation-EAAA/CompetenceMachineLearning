import itertools
import os

#%matplotlib inline
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf
import DBhandler
import random




from sklearn.preprocessing import MultiLabelBinarizer, LabelEncoder
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics import confusion_matrix

from tensorflow import keras
#from keras.models import Sequential
#from keras.layers import Dense, Activation, Dropout
#from keras.preprocessing import text, sequence
#from keras import utils

# This code was tested with TensorFlow v1.4
#print("You have TensorFlow version", tf.__version__)
class MultipleOutputModel:
    def trainModel(self):
        db = DBhandler.DBHandler()
        training, test = db.loadAdvertDataMulti()
        train_data, train_label, test_data, test_label  = [], [], [], []
        y_train, y_test =[], []
        num_classes_array = []

        for x in training:
            #convert = x.numberFormat_body.split(' ')
            #train_data.append(convert)
            train_data.append(x.searchable_body)

            train_label.append(x.kompetence)
        for x in test:
            #convert = x.numberFormat_body.split(' ')
            #test_data.append(convert)
            #searchable_body
            test_data.append(x.searchable_body)
            test_label.append(x.kompetence)

        max_words = 10000
        tokenize = keras.preprocessing.text.Tokenizer(num_words=max_words, char_level=False)

        tokenize.fit_on_texts(train_data) # only fit on train
        #print(tokenize.word_index)
        x_train = tokenize.texts_to_matrix(train_data)
        x_test = tokenize.texts_to_matrix(test_data)
        #print(train_label)

        # Use sklearn utility to convert label strings to numbered index
        #encoder = LabelEncoder()
        #for x in train_label:
        #    encoder.fit(x)
        #    y_train.append(encoder.transform(x))
        #for x in test_label:
        #    y_test.append(encoder.transform(x))
        #    #y_train = encoder.transform(train_label)
        #    #y_test = encoder.transform(test_label)


        #encoder.fit(train_label)


        df = pd.DataFrame(train_label)
        #df.drop(index='NONE')
        encoder = LabelEncoder()
        encoder.fit(df)
        y_train = encoder.transform(df)
        y_test = encoder.transform(test_label)
        print("Shape of y: " + str(list(df.iloc[0])))
        #print("Shape of y_train: " + str(set(y_train.iloc[500])))


        #v = DictVectorizer(sparse=False)
        #v.fit(train_label)
        #y_train = v.transform(train_label)
        #y_test = v.transform(test_label)

        #print('Number of classes: ', y_train)


        # Converts the labels to a one-hot representation
        #num_classes_array = set(list(itertools.chain.from_iterable(y_train)))

        #num_classes_array = list(itertools.chain.from_iterable(y_train))
        #print(len(num_classes_array))
        num_classes = np.max(y_train) + 1
        y_train = keras.utils.to_categorical(y_train, num_classes)
        y_test = keras.utils.to_categorical(y_test, num_classes)

        # Inspect the dimenstions of our training and test data (this is helpful to debug)
        print('x_train shape:', x_train.shape)
        print('x_test shape:', x_test.shape)
        print('y_train shape:', y_train.shape)
        print('y_test shape:', y_test.shape)
        print("Train data lenght: " + str(len(x_train)))
        test=[]
        for x in y_train:
            test.extend(x)
        print("Train label lenght: " + str(len(test)))

        model = keras.Sequential()
        model.add(keras.layers.Dense(3, input_shape=(max_words,), activation=tf.nn.relu))
        #model.add(Activation('relu'))
        model.add(keras.layers.Dense(12, activation=tf.nn.relu))
        model.add(keras.layers.Dropout(0.5))
        model.add(keras.layers.Dense(num_classes, activation=tf.nn.softmax))
        #model.add(Activation('softmax'))

        #model.compile(loss='categorical_crossentropy',
        #              optimizer='adam',
        #              metrics=['accuracy'])

        model.compile(optimizer=tf.train.AdamOptimizer(), 
                    loss='categorical_crossentropy',
                    metrics=['accuracy'])

        checkpoint_path = "training_1/cp.ckpt"
        checkpoint_dir = os.path.dirname(checkpoint_path)

        # Create checkpoint callback
        cp_callback = tf.keras.callbacks.ModelCheckpoint(checkpoint_path, 
                                                         save_weights_only=True,
                                                         verbose=1)

        history = model.fit(x_train, y_train,
                    epochs=3,
                    verbose=1,
                    validation_split=0.1,
                    callbacks = [cp_callback])


        score = model.evaluate(x_test, y_test, verbose=1)
        print('Test score:', score[0])
        print('Test accuracy:', score[1])
        # Here's how to generate a prediction on individual examples
        text_labels = encoder.classes_ 
        #x_test_random = random.shuffle(x_test)

        for i in range(100):
            prediction = model.predict(np.array([x_test[i]]))
            predicted_label = text_labels[np.argmax(prediction)]
            #print(test_data[i][:50] + "...")
            print('Actual label:' + str(test_label[i]))
            print("Predicted label: " + predicted_label + "\n")

        y_softmax = model.predict(x_test)

        y_test_1d = []
        y_pred_1d = []

        for i in range(len(y_test)):
            probs = y_test[i]
            index_arr = np.nonzero(probs)
            one_hot_index = index_arr[0].item(0)
            y_test_1d.append(one_hot_index)

        for i in range(0, len(y_softmax)):
            probs = y_softmax[i]
            predicted_index = np.argmax(probs)
            y_pred_1d.append(predicted_index)
