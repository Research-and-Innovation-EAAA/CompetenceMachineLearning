import DBhandler
from Competence import Competence
import model
import tensorflow as tf
from tensorflow import keras

def runLoadedModel(model):
    #training, test = db.loadAdvertData(Competence(12562, "engelsk"))
    training, test = db.loadAdvertData(Competence(13712, "Java (Computerprogrammering)"))
    train_data, train_label, test_data, test_label  = [], [], [], []
    for x in training:
        convert = x.numberFormat_body.split(' ')
        train_data.append(convert)
        train_label.append(x.matchCurrentCompetence)
    for x in test:
        convert = x.numberFormat_body.split(' ')
        test_data.append(convert)
        test_label.append(x.matchCurrentCompetence)
    
    train_data = keras.preprocessing.sequence.pad_sequences(train_data,
                                                            value=0,
                                                            padding='post',
                                                            maxlen=1000)
    test_data = keras.preprocessing.sequence.pad_sequences(test_data,
                                                            value=0,
                                                            padding='post',
                                                            maxlen=1000)
 
    model.compile(optimizer=tf.train.AdamOptimizer(), 
                    loss='binary_crossentropy',
                    metrics=['accuracy'])
    
    results = model.evaluate(test_data, test_label)
    
    print('Test accuracy:', results)

if __name__ == '__main__':
    db = DBhandler.DBHandler()

    #training, test = db.loadAdvertData(Competence(13712, "Java (Computerprogrammering)"))
    #train_data, train_label, test_data, test_label  = [], [], [], []
    #con = 'Dette er en splittet streng'
    #erLigeMed10 = '1 2 3 4 5 6 7 8 9 10'
    #over10 = '1 2 3 4 5 6 7 8 9 10 11 12 13 14 15'
    #splitCon = con.split(' ')
    #while len(splitCon) < 10:
    #    splitCon.append('add')
    #splitCon = splitCon[:10]

    #print(splitCon)
    #print(len(splitCon))
    #for x in training:
    #        convert = x.numberFormat_body.split(' ')
    #        #while len(convert) < 1000:
    #        #    convert.append(0)
    #        train_data.append(convert[:4])
    #        train_label.append(x.matchCurrentCompetence)
  
    #print(len(training))
    #print(train_data[0])
    #print(training[0])
    #print(train_data[2])
    #print(training[2])
    #print(train_data[5])
    #print(training[5])
    #print(training[1]._id)
    #for x in training:
    #    train_data.append(x.numberFormat_body)
    #    train_label.append(x.matchCurrentCompetence)
    #for x in test:
    #    test_data.append(x.numberFormat_body)
    #    test_label.append(x.matchCurrentCompetence)

    #print('Trainings Data lenght: '+str(len(test_data)))
    #print('Trainings label lenght: '+ str(len(test_label)))

    #mod = model.Model()
    #mod.addStandardLayer(2)
    #mod.createModel()


    model = db.loadModel(13712, "Festabe")
    runLoadedModel(model)
    

