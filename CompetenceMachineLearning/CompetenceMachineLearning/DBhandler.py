import mysql.connector
from mysql.connector import errorcode
import os
import yaml
from Competence import Competence
import random


class DBHandler:

    my_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(my_path, "../config.yml")
    config = yaml.safe_load(open(path))
    
    
    def loadCompetences(self):
        try:
            cnx = mysql.connector.connect(**self.config)
        except mysql.connector.Error as err:
             if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                 print("Something is wrong with your user name or password")
             elif err.errno == errorcode.ER_BAD_DB_ERROR:
                 print("Database does not exist")
             else:
                 print(err)
        else:
            cursor = cnx.cursor()
            query = "select _id, prefferredLabel from kompetence"
            cursor.execute(query)
            competenceList = []
            for row in cursor:
                competenceList.append(Competence(row[0], row[1]))
            cursor.close()
            cnx.close()
            return competenceList


    def loadAdvertData(self, _id):
        try:
            cnx = mysql.connector.connect(**self.config)
        except mysql.connector.Error as err:
             if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                 print("Something is wrong with your user name or password")
             elif err.errno == errorcode.ER_BAD_DB_ERROR:
                 print("Database does not exist")
             else:
                 print(err)
        else:
            cursor = cnx.cursor()
            query = "select a._id, a.numberFormat_body from annonce a, annonce_kompetence ak where a._id = ak.annonce_id and ak.kompetence_id = " + str(_id)
            cursor.execute(query)

            trainingContainer = []
            testContainer = []

            i = cursor.rowcount
            for row in cursor:
                if i < cursor.rowcount*(6/10):
                    trainingContainer.append(row)
                else:
                    testContainer.append(row)

            cursor.close()
            cnx.close()

            #random.shuffle(array)

            #SQL order_by RAND()     - Could be used to get kompetence-less annoncer from all over?

            
            trainingData = []
            trainingLabels = []
            testData = []
            testLabels = []

            return trainingData, trainingLabels, testData, testLabels


    def retrive(self):
        try:
            cnx = mysql.connector.connect(**self.config)
        except mysql.connector.Error as err:
             if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                 print("Something is wrong with your user name or password")
             elif err.errno == errorcode.ER_BAD_DB_ERROR:
                 print("Database does not exist")
             else:
                 print(err)
        else:
            fetchcursor = cnx.cursor()
            query = ("SELECT name FROM region")
            fetchcursor.execute(query)
            for(name) in fetchcursor:
                print("Regions Navn: " + name[0])
            fetchcursor.close()
            cnx.close()

