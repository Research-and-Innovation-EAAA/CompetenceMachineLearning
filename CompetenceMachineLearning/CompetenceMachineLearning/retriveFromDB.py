import mysql.connector
from mysql.connector import errorcode
import os
import yaml


class RetriveFromDB:
    def retrive(self):

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
            fetchcursor = cnx.cursor()
            query = ("SELECT name FROM region")
            fetchcursor.execute(query)
            for(name) in fetchcursor:
                print("Regions Navn: " + name[0])

            fetchcursor.close()
            cnx.close()

