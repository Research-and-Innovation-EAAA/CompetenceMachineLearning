import DBhandler
from Competence import Competence
import model

if __name__ == '__main__':
    db = DBhandler.DBHandler()

    test, test2 = db.loadAdvertData(Competence(13712, "Java (Computerprogrammering)"))
    print(test[0])


    mod = model.Model()
    mod.addStandardLayer(22)
    mod.addStandardLayer(244)
    mod.addStandardLayer(21)
    #mod.createModel()
