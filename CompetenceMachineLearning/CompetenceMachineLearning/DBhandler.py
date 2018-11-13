import mysql.connector
from mysql.connector import errorcode
import os
import yaml
from Competence import Competence
from Advert import Advert 
import random
import json



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


    def loadAdvertData(self, competence):
        cnx = self.createConnection()
        cursor = cnx.cursor()
        query = "select a._id, a.numberFormat_body from annonce a, annonce_kompetence ak where a._id = ak.annonce_id and ak.kompetence_id = " + str(competence._id)
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
        q2 = "select a._id , a.numberFormat_body from annonce a, annonce_kompetence ak where a._id = ak.annonce_id and ak.kompetence_id != " + str(competence._id) + " and a.numberFormat_body is not NULL group by a._id order by a._id desc limit " + str(len(correctAdverts))
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
        random.shuffle(trainingAdverts)
        random.shuffle(testingAdverts)
        return trainingAdverts, testingAdverts


    def storeMatches(self, competenceID, advertIDs):
        cnx = self.createConnection()
        cursor = cnx.cursor()
        # There is a limit on the values clause, only 1000 rows can be inserted at a time. Making a loop to generate multiple queries as needed.
        # No need to check if the kompetence-annonce match exists already, the unique indexon the table should prevent duplicate rows from being added.
        # A seperate method may be desired to clear all matches of a competence, but it's not this one.
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
        cursor.close()
        cnx.close()

    def loadDictionaryLength(self):
        cnx = self.createConnection()
        cursor = cnx.cursor()
        cursor.execute("select count(_id) from machine_word_dictionary")
        return cursor.fetchone()[0]


    def saveModel(self, modelName, model, competenceID):
        cnx = self.createConnection()
        cursor = cnx.cursor()
        modelJSON = str(model.to_json())
        weightsJSON = str(json.dumps(model.get_weights().tolist()))
        cursor.execute("select name from machine_model where kompetence_id = " + str(competenceID) + "name = " + modelName)
        if (len(list(cursor)) > 0):
            cursor.execute("insert into machine_model(kompetence_id, model, weights, name) values(" + str(competenceID) + ", " + modelJSON + ", " + weightsJSON + ", " + modelName + ")")
        else:
            cursor.execute("update machine_model set model = " + modelJSON + ", weights = " + weightsJSON + " where kompetence_id = " + str(competenceID) + " and name = " + modelName)
        cursor.close()
        cnx.close()
        
    def loadCompetencesWithModels(self):
        cnx = self.createConnection()
        cursor = cnx.cursor()
        cursor.execute("")
        #select all ids & preflabels from kompetence where kompetence id = model kompetence id
        raise Exception("Error: This method hasn't been programmed yet!")
        
    def loadModelNames(self, competenceID):
        #select all model names where kompetence id = kompetence id
        raise Exception("Error: This method hasn't been programmed yet!")

    def loadModel(self, name, competenceID):
        #load model data for specified name/id pair
        #Figure out how to restore weights from JSON (Note: Quite important.)
        raise Exception("Error: This method hasn't been programmed yet!")