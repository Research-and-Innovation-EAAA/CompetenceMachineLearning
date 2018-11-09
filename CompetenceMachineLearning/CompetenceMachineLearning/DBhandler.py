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


    def loadAdvertData(self, competence):
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
            query = "a._id, a.numberFormat_body from annonce a, annonce_kompetence ak where a._id = ak.annonce_id and ak.kompetence_id = " + str(competence._id)
            cursor.execute(query)

            trainingAdverts = [[]]
            testingAdverts = [[]]

            i = 0
            for row in cursor:
                if i < cursor.rowcount*(6/10):
                    trainingContainer.append(Advert(row[0], row[1], 1))
                else:
                    testContainer.append(Advert(row[0], row[1], 1))
                i += 1

            q2 = "FIGURE ME OUT" #Testing queries in workbench. Problem: They take far too long to get the desired data. (More than 10 min)
            cursor.execute(q2)

            i = 0
            for row in cursor:
                if i < cursor.rowcount*(6/10):
                    trainingContainer.append(Advert(row[0], row[1], 0))
                else:
                    testContainer.append(Advert(row[0], row[1], 0))
                i += 1
            
            cursor.close()
            cnx.close()

            random.shuffle(trainingContainer)
            random.shuffle(testContainer)
            
            return trainingAdverts, testingAdverts


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

