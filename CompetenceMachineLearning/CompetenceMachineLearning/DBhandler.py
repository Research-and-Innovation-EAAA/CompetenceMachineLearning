import mysql.connector
from keras_preprocessing.text import tokenizer_from_json
from mysql.connector import errorcode
import os
from Advert import Advert
import random
import json
from tensorflow import keras


class DBHandler:

    def __create_connection(self):
        try:
            cnx = mysql.connector.connect(user=os.environ['MYSQL_USER'], password=os.environ['MYSQL_PASSWORD'],
                                          host=os.environ['MYSQL_HOST'],
                                          database=os.environ['MYSQL_DATABASE'], port=os.environ['MYSQL_PORT'])
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Database access denied")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            return cnx

    def load_advert_count(self):
        cnx = self.__create_connection()
        cursor = cnx.cursor()

        cursor.execute("SELECT count(*) FROM annonce")
        res = cursor.fetchone()[0]

        cursor.close()
        cnx.close()

        return res

    def insert_advert(self, competence_id, advert_id):
        cnx = self.__create_connection()
        cursor = cnx.cursor()

        query = "INSERT IGNORE INTO annonce_kompetence_machine(annonce_id, kompetence_id) VALUES({0}, {1})".format(advert_id, competence_id)
        print(query)

        cursor.execute(query)
        cnx.commit()

        cursor.close()
        cnx.close()

    def load_advert_data(self, batch_size, offset):
        adverts = []
        cnx = self.__create_connection()
        cursor = cnx.cursor()

        query = 'SELECT a._id, a.searchable_body FROM annonce a LIMIT {0} OFFSET {1}'.format(batch_size, offset)
        print(query)
        cursor.execute(query)
        searchable_body = list(cursor)

        for row in searchable_body:
            adverts.append(Advert(advert_id=row[0], body=row[1], competence=""))

        cursor.close()
        cnx.close()

        return adverts

    def load_advert_data_binary_classification(self, competence_id):
        training_adverts = []
        testing_adverts = []

        # 13712 = Java programmør
        # 146798 = Grafisk Design
        # 32286 = Butiksassistent
        # 43754 = Tømrer

        cnx = self.__create_connection()
        cursor = cnx.cursor()

        query = "select a._id, a.searchable_body from annonce a join annonce_kompetence ak on a._id = ak.annonce_id where ak.kompetence_id = " + str(competence_id)
        print(query)

        cursor.execute(query)
        searchable_body = list(cursor)

        # Split into validation and training sets at ratio of 1:5
        i = 0
        for row in searchable_body:
            if i % 5 == 0:
                testing_adverts.append(Advert(advert_id=row[0], body=row[1], competence=1))
            else:
                training_adverts.append(Advert(advert_id=row[0], body=row[1], competence=1))
            i += 1

        query = "SELECT a._id, a.searchable_body FROM annonce a WHERE a._id NOT IN (SELECT annonce_id FROM annonce_kompetence ak WHERE kompetence_id = " + str(competence_id) + ") ORDER BY a._id DESC LIMIT " + str(len(searchable_body))
        print(query)

        cursor.execute(query)
        searchable_body = list(cursor)

        i = 0
        for row in searchable_body:
            if i % 5 == 0:
                testing_adverts.append(Advert(advert_id=row[0], body=row[1], competence=0))
            else:
                training_adverts.append(Advert(advert_id=row[0], body=row[1], competence=0))
            i += 1

        print("total amount of adverts = " + str((len(testing_adverts) + len(training_adverts))))
        print("test set length = " + str(len(testing_adverts)))
        print("training set length = " + str(len(training_adverts)))

        random.shuffle(training_adverts)
        random.shuffle(testing_adverts)

        cursor.close()
        cnx.close()

        return training_adverts, testing_adverts

    def load_advert_data_multiple_classes(self):
        training_adverts = []
        testing_adverts = []
        cnx = self.__create_connection()
        cursor = cnx.cursor()

        # 13712 = Java programmør
        # 146798 = Grafisk Design
        # 32286 = Butiksassistent
        # 43754 = Tømrer

        competence_ids = [13712, 146798, 32286, 43754]

        for _id in competence_ids:

            query = "SELECT a._id, a.searchable_body, k.prefferredLabel FROM annonce a JOIN annonce_kompetence ak ON a._id = ak.annonce_id JOIN kompetence k ON k._id = ak.kompetence_id WHERE ak.kompetence_id = " + str(_id) + " LIMIT 4000"
            print(query)
            cursor.execute(query)

            searchable_body = list(cursor)

            i = 0
            for row in searchable_body:
                body = str(row[1])

                # Split data into training and test sets.
                if i % 5 == 0:
                    testing_adverts.append(Advert(advert_id=row[0], body=body, competence=row[2]))
                else:
                    training_adverts.append(Advert(advert_id=row[0], body=body, competence=row[2]))
                i = i + 1

        print("total amount of adverts = " + str((len(testing_adverts) + len(training_adverts))))
        print("test set length = " + str(len(testing_adverts)))
        print("training set length = " + str(len(training_adverts)))

        random.shuffle(training_adverts)
        random.shuffle(testing_adverts)

        cursor.close()
        cnx.close()

        return training_adverts, testing_adverts

    def save_model(self, model, competence_id, tokenizer):
        cnx = self.__create_connection()
        cursor = cnx.cursor()

        model_name = "kompetence_" + str(competence_id) + "_model.h5"
        tokenizer_name = "kompetence_" + str(competence_id) + "_tokenizer.json"

        model.save(model_name)
        tokenizer_json = tokenizer.to_json()

        # Save tokenizer to file.
        with open(tokenizer_name, 'w', encoding='utf-8') as f:
            f.write(json.dumps(tokenizer_json, ensure_ascii=False))

        # Insert model and tokenizer file names in database.
        query = "insert into kompetence_machine (kompetence_id, model, tokenizer) values(" + str(competence_id) + ", '" + model_name + "', '" + tokenizer_name + "')"
        print(query)

        cursor.execute(query)
        cnx.commit()

        cursor.close()
        cnx.close()

    def load_model(self, model_id):
        cnx = self.__create_connection()
        cursor = cnx.cursor()

        query = "select model from kompetence_machine where _id = " + str(model_id)
        print(query)

        cursor.execute(query)
        model_name = str(list(cursor)[0][0])

        model = keras.models.load_model(model_name)

        return model

    def load_tokenizer(self, model_id):
        cnx = self.__create_connection()
        cursor = cnx.cursor()

        query = "select tokenizer from kompetence_machine where _id = " + str(model_id)
        print(query)
        cursor.execute(query)

        tokenizer_name = str(list(cursor)[0][0])

        with open(tokenizer_name) as f:
            data = json.load(f)
            tokenizer = tokenizer_from_json(data)

        return tokenizer

    def load_model_ids(self):
        cnx = self.__create_connection()
        cursor = cnx.cursor()

        query = "select _id, kompetence_id from kompetence_machine"
        print(query)

        cursor.execute(query)
        res = list(cursor)

        model_ids, competence_ids = [], []

        for element in res:
            model_ids.append(element[0])
            competence_ids.append(element[1])

        return model_ids, competence_ids

