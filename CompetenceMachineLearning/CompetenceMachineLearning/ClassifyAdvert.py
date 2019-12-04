import numpy as np
import tensorflow as tf
from tensorflow import keras
import DBhandler
import keras_preprocessing.text as text
import keras_preprocessing.sequence as sequence
from sklearn.preprocessing import OneHotEncoder


def train_model():
    training, test = DBhandler.DBHandler().load_advert_data_multiple_classes()
    training_data, training_label, test_data, test_label = [], [], [], []

    for advert in training:
        training_data.append(advert.body)
        training_label.append(advert.competence)
    for advert in test:
        test_data.append(advert.body)
        test_label.append(advert.competence)

    # Limit on number of unique words (features) in advert text across all adverts
    max_words = 5000

    max_length = 500

    # Create vocubulary with training data
    tokenizer = text.Tokenizer(num_words=max_words)
    tokenizer.fit_on_texts(training_data)

    # Tokenize training and test data
    x_training = tokenizer.texts_to_sequences(training_data)
    x_test = tokenizer.texts_to_sequences(test_data)

    vocab_size = len(tokenizer.word_index) + 1
    print("vocab_size = " + str(vocab_size))

    # Pad or truncate advert texts
    x_training = sequence.pad_sequences(x_training, maxlen=max_length, padding='post')
    x_test = sequence.pad_sequences(x_test, maxlen=max_length, padding='post')

    # Encode labels
    encoder = OneHotEncoder()

    x_training_label = encoder.fit_transform(np.array(training_label).reshape(-1, 1)).toarray()
    x_test_label = encoder.fit_transform(np.array(test_label).reshape(-1, 1)).toarray()

    num_classes = len(encoder.categories_[0])
    print("Number of classes = " + str(num_classes))

    embedding_dim = 50

    # Build model
    model = tf.keras.Sequential([
        tf.keras.layers.Embedding(input_dim=vocab_size, output_dim=embedding_dim, input_length=max_length),
        tf.keras.layers.GlobalMaxPool1D(),
        tf.keras.layers.Dense(10, activation='relu'),
        tf.keras.layers.Dense(num_classes, activation='softmax')
    ])
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
    history = model.fit(
        x_training,
        x_training_label,
        epochs=5,
        validation_data=(x_test, x_test_label),
        verbose=2,
        batch_size=64)

    plot_model(history)

    return model


def train_binary_model(competence_id, save):
    training, test = DBhandler.DBHandler().load_advert_data_binary_classification(competence_id)
    training_data, training_label, test_data, test_label = [], [], [], []

    for advert in training:
        training_data.append(advert.body)
        training_label.append(advert.competence)
    for advert in test:
        test_data.append(advert.body)
        test_label.append(advert.competence)

    training_label = np.array(training_label)
    test_label = np.array(test_label)

    # Limit on number of unique words (features) in advert text across all adverts
    max_words = 2500

    # Create vocubulary with training data
    tokenizer = keras.preprocessing.text.Tokenizer(num_words=max_words)
    tokenizer.fit_on_texts(training_data)

    # Tokenize training and test data
    x_training = tokenizer.texts_to_sequences(training_data)
    x_test = tokenizer.texts_to_sequences(test_data)

    vocab_size = len(tokenizer.word_index) + 1

    max_length = 500

    # Pad or truncate advert texts
    x_training = sequence.pad_sequences(x_training, maxlen=max_length, padding='post')
    x_test = sequence.pad_sequences(x_test, maxlen=max_length, padding='post')

    embedding_dim = 50

    # Build model

    model = tf.keras.Sequential([
        tf.keras.layers.Embedding(input_dim=vocab_size, output_dim=embedding_dim, input_length=max_length),
        tf.keras.layers.GlobalMaxPool1D(),
        tf.keras.layers.Dense(10, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])

    history = model.fit(
        x_training,
        training_label,
        epochs=4,
        validation_data=(x_test, test_label),
        verbose=2,
        batch_size=10)

    if save is True:
        DBhandler.DBHandler().save_model(model=model, competence_id=competence_id, tokenizer=tokenizer)
    else:
        plot_model(history)


def plot_model(history):
    import matplotlib.pyplot as plt
    plt.style.use('ggplot')

    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    x = range(1, len(acc) + 1)

    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(x, acc, 'b', label='Training acc')
    plt.plot(x, val_acc, 'r', label='Validation acc')
    plt.xlabel('Epoch')
    plt.title('Training and validation accuracy')
    plt.legend()
    plt.subplot(1, 2, 2)
    plt.plot(x, loss, 'b', label='Training loss')
    plt.plot(x, val_loss, 'r', label='Validation loss')
    plt.xlabel('Epoch')
    plt.title('Training and validation loss')
    plt.legend()
    plt.show()


def match_competence():
    db = DBhandler.DBHandler()

    # Get model- and competence ids from models
    model_ids, competence_ids = db.load_model_ids()
    print("Loaded " + str(len(model_ids)) + " model(s)")

    for i in range(len(model_ids)):
        print("Predicting with model_id " + str(model_ids[i]) + " containing competence_id " + str(competence_ids[i]))

        # Load model and tokenizer
        model = db.load_model(model_id=model_ids[i])
        tokenizer = db.load_tokenizer(model_id=model_ids[i])

        # Get total number of adverts
        advert_count = db.load_advert_count()

        batch_size = 10000

        # Load adverts in batches of 10000
        for offset in range(0, advert_count, batch_size):

            adverts = db.load_advert_data(batch_size=batch_size, offset=offset)
            advert_ids, advert_bodies = [], []
            for advert in adverts:
                advert_ids.append(advert.advert_id)
                advert_bodies.append(advert.body)

            tokenized_bodies = sequence.pad_sequences(tokenizer.texts_to_sequences(advert_bodies), maxlen=500)
            predictions = model.predict(tokenized_bodies)

            for j in range(len(predictions)):
                if predictions[j] > 0.9:
                    print("Predicted annonce_id " + str(advert_ids[j]) + " to be of kompetence_id " + str(competence_ids[i]))
                    db.insert_advert(competence_id=competence_ids[i], advert_id=advert_ids[j])


def ensemble_prediction():
    db = DBhandler.DBHandler()

    # Get model- and competence ids from models
    model_ids, competence_ids = db.load_model_ids()
    print("Loaded " + str(len(model_ids)) + " model(s)")

    models, tokenizers = [], []
    for model_id in model_ids:
        models.append(db.load_model(model_id=model_id))
        tokenizers.append(db.load_tokenizer(model_id=model_id))

    # Get total number of adverts
    advert_count = db.load_advert_count()

    batch_size = 10000

    print("Model ids " + str(model_ids))
    print("Competence ids " + str(competence_ids))

    # Load adverts in batches of 10000 to avoid timeouts
    for offset in range(0, advert_count, batch_size):

        adverts = db.load_advert_data(batch_size=batch_size, offset=offset)
        advert_ids, advert_bodies = [], []
        for advert in adverts:
            advert_ids.append(advert.advert_id)
            advert_bodies.append(advert.body)
        predictions = []

        for i in range(len(models)):
            tokenized_bodies = sequence.pad_sequences(tokenizers[i].texts_to_sequences(advert_bodies), maxlen=500)
            predictions.append(models[i].predict(tokenized_bodies))

        for i in range(len(predictions[0])):
            prediction = []
            for j in range(len(predictions)):
                prediction.append(predictions[j][i])

            if prediction[np.argmax(prediction)] > 0.9:
                print("Predicted annonce_id " + str(advert_ids[i]) + " to be of kompetence_id " + str(competence_ids[np.argmax(prediction)]))
                db.insert_advert(competence_id=competence_ids[np.argmax(prediction)], advert_id=advert_ids[i])

