import mysql.connector
from mysql.connector import errorcode
import os
import yaml
from Competence import Competence
from Advert import Advert 
from MultipleAdverts import MultipleAdverts
import random
import json
import tensorflow
from tensorflow import keras
import numpy


class DBHandler:

    def createConnection(self):
        my_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(my_path, "../config.yml")
        config = yaml.safe_load(open(path))
        try:
            cnx = mysql.connector.connect(**config)
        except mysql.connector.Error as err:
             if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                 print("Something is wrong with your user name or password")
             elif err.errno == errorcode.ER_BAD_DB_ERROR:
                 print("Database does not exist")
             else:
                 print(err)
        else:
            return cnx
    
    


    def loadCompetences(self):
        cnx = self.createConnection()
        cursor = cnx.cursor()
        query = "select _id, prefferredLabel from kompetence"
        cursor.execute(query)
        competenceList = []
        for row in cursor:
            competenceList.append(Competence(row[0], row[1]))
        cursor.close()
        cnx.close()
        return competenceList


    def loadAdvertDataNumberFormat(self, competenceID):
        cnx = self.createConnection()
        cursor = cnx.cursor()
        query = "select a._id, a.numberFormat_body from annonce a, annonce_kompetence ak where a._id = ak.annonce_id and ak.kompetence_id = " + str(competenceID) + " and a.numberFormat_body is not NULL"
        cursor.execute(query)
        trainingAdverts = []
        testingAdverts = []
        correctAdverts = list(cursor)
        i = 0
        for row in correctAdverts:
            if i < len(correctAdverts)*(6/10):
                trainingAdverts.append(Advert(row[0], row[1], 1))
            else:
                testingAdverts.append(Advert(row[0], row[1], 1))
            i += 1
        q2 = "select a._id , a.numberFormat_body from annonce a, annonce_kompetence ak where a._id = ak.annonce_id and ak.kompetence_id != " + str(competenceID) + " and a.numberFormat_body is not NULL group by a._id order by a._id desc limit " + str(len(correctAdverts))
        cursor.execute(q2)
        incorrectAdverts = list(cursor)
        cursor.close()
        cnx.close()
        i = 0
        for row in incorrectAdverts:
            if i < len(incorrectAdverts)*(6/10):
                trainingAdverts.append(Advert(row[0], row[1], 0))
            else:
                testingAdverts.append(Advert(row[0], row[1], 0))
            i += 1
        #random.shuffle(trainingAdverts)
        #random.shuffle(testingAdverts)
        return trainingAdverts, testingAdverts

    def loadAdvertDataSearchableBody(self, competenceID):
        cnx = self.createConnection()
        cursor = cnx.cursor()
        query = "select a._id, a.searchable_body from annonce a, annonce_kompetence ak where a._id = ak.annonce_id and ak.kompetence_id = " + str(competenceID) + " and a.searchable_body is not null"
        cursor.execute(query)
        trainingAdverts = []
        testingAdverts = []
        correctAdverts = list(cursor)
        i = 0
        for row in correctAdverts:
            chars = list(row[1])
            numbers = []
            for char in chars:
                numbers.append(str(ord(str(char))))
            if i < len(correctAdverts)*(6/10):
                trainingAdverts.append(Advert(row[0], numbers, 1))
            else:
                testingAdverts.append(Advert(row[0], numbers, 1))
            i += 1
        q2 = "select a._id , a.searchable_body from annonce a, annonce_kompetence ak where a._id = ak.annonce_id and ak.kompetence_id != " + str(competenceID) + " and a.searchable_body is not NULL group by a._id order by a._id desc limit " + str(len(correctAdverts))
        cursor.execute(q2)
        incorrectAdverts = list(cursor)
        cursor.close()
        cnx.close()
        i = 0
        for row in incorrectAdverts:
            chars = list(row[1])
            numbers = []
            for char in chars:
                numbers.append(str(ord(str(char))))
            if i < len(incorrectAdverts)*(6/10):
                trainingAdverts.append(Advert(row[0], numbers, 0))
            else:
                testingAdverts.append(Advert(row[0], numbers, 0))
            i += 1
        random.shuffle(trainingAdverts)
        random.shuffle(testingAdverts)
        return trainingAdverts, testingAdverts


    def storeMatches(self, competenceID, advertIDs, modelName):
        cnx = self.createConnection()
        cursor = cnx.cursor()
        # There is a limit on the values clause, only 1000 rows can be inserted at a time. Making a loop to generate multiple queries as needed.
        # No need to check if the kompetence-annonce match exists already, the unique index on the table should prevent duplicate rows from being added.
        i = 0
        while i < len(advertIDs):
            query = "insert into annonce_kompetence_machine(kompetence_id, annonce_id) values "
            j = 0
            done = False
            while (j < 950) and (not done):
                if i + j < len(advertIDs):
                    if j == 0:
                        query += "(" + competenceID + ", " + advertIDs[i+j] + ")"
                    else:
                        query += ", (" + competenceID + ", " + advertIDs[i+j] + ")"
                else:
                    done = True
                j += 1
            cursor.execute(query)
            i += 950
        cnx.commit()
        cursor.close()
        cnx.close()

    def loadDictionaryLength(self):
        cnx = self.createConnection()
        cursor = cnx.cursor()
        cursor.execute("select count(_id) from machine_word_dictionary")
        return cursor.fetchone()[0]


    def saveModel(self, modelName, modelType, model, competenceID):
        cnx = self.createConnection()
        cursor = cnx.cursor()
        modelJSON = str(model.to_json())
        numArray = model.get_weights()
        listJson = [[]]
        for x in numArray:
            listJson.append(x.tolist())
        weightsJSON = json.dumps(listJson)

        cursor.execute("select name from machine_model where kompetence_id = " + str(competenceID) + " and name = '" + modelName + "' and type = '" + modelType + "'")
        if (len(list(cursor)) == 0):
            cursor.execute("insert into machine_model(kompetence_id, model, weights, name, type) values(" + str(competenceID) + ", '" + modelJSON + "', '" + weightsJSON + "', '" + modelName + "', '" + modelType + "')")
        else:
            cursor.execute("update machine_model set model = '" + modelJSON + "', weights = '" + weightsJSON + "' where kompetence_id = " + str(competenceID) + " and name = '" + modelName + "' and type = '" + modelType + "'")
        cnx.commit()
        cursor.close()
        cnx.close()
        
    def loadCompetencesWithModels(self):
        cnx = self.createConnection()
        cursor = cnx.cursor()
        cursor.execute("select k._id, k.prefferredLabel from kompetence k, machine_model mm where k._id = mm.kompetence_id group_by k._id")
        competences = []
        for row in cursor:
            competences.append(Competence(row[0], row[1]))
        return competences
        
    def loadModelNames(self, competenceID):
        cnx = self.createConnection()
        cursor = cnx.cursor()
        cursor.execute("select name from machine_model where kompetence_id = " + str(competenceID))
        modelNames = []
        for row in cursor:
            modelNames.append(row[0])
        return modelNames

    def loadModel(self, competenceID, name, type):
        cnx = self.createConnection()
        cursor = cnx.cursor()
        cursor.execute("select model, weights from machine_model where name = '" + name + "' and kompetence_id = " + str(competenceID) + "' and type = " + type)
        row = cursor.fetchone()
        modelJSON = row[0]
        weightsJSON = row[1]
        model = keras.models.model_from_json(modelJSON)
        weights = json.loads(weightsJSON)
        tmp = []
        for list in weights:
            tmp.append(numpy.array(list))
        numpyWeights = numpy.array(tmp)
        numpyWeights = numpy.delete(numpyWeights, 0, 0)
        model.set_weights(numpyWeights)
        return model

    def loadAnnounceFromTestCats(self):
        trainingAdverts = []
        testingAdverts = []
        cnx = self.createConnection()
        cursor = cnx.cursor()
        #query1 = "SELECT a.searchable_body, k.prefferredLabel FROM annonce a JOIN annonce_kompetence ak ON a._id = ak.annonce_id JOIN kompetence k ON k._id = ak.kompetence_id WHERE ak.kompetence_id =12551 or ak.kompetence_id = 12562 or ak.kompetence_id = 13727"
        query1 ="SELECT a._id, a.searchable_body FROM annonce a JOIN annonce_kompetence ak ON a._id = ak.annonce_id JOIN kompetence k ON k._id = ak.kompetence_id WHERE ak.kompetence_id =150388 or ak.kompetence_id = 165432 or ak.kompetence_id = 13727"
        cursor.execute(query1)
        searchableBodyCursor = list(cursor)
        #correctAdverts = list(cursor)
        i = 0
        for row in searchableBodyCursor:
            queryCompetencelist ="SELECT k.prefferredLabel FROM annonce_kompetence ak JOIN kompetence k ON k._id = ak.kompetence_id WHERE ak.annonce_id = " + str(row[0])
            cursor.execute(queryCompetencelist)
            competences = list(cursor)
            if i < len(searchableBodyCursor)*(6/10):
                trainingAdverts.append(MultipleAdverts(row[1], competences))
            else:
                testingAdverts.append(MultipleAdverts(row[1], competences))


        #query2 = "SELECT a.searchable_body, k.prefferredLabel FROM annonce a JOIN annonce_kompetence ak ON a._id = ak.annonce_id JOIN kompetence k ON k._id = ak.kompetence_id WHERE ak.kompetence_id !=12551 or ak.kompetence_id != 12562 or ak.kompetence_id != 13727 " + "limit " + str(len(correctAdverts))


        #cursor.execute(query2)
        #incorrectAdverts = list(cursor)
        #i = 0
        #for row in incorrectAdverts:
        #    if i < len(incorrectAdverts)*(6/10):
        #        trainingAdverts.append(MultipleAdverts(row[0], row[1]))
        #    else:
        #        testingAdverts.append(MultipleAdverts(row[0], row[1]))
        #    i += 1
        random.shuffle(trainingAdverts)
        random.shuffle(testingAdverts)
        cursor.close()
        cnx.close()
        return trainingAdverts, testingAdverts

       