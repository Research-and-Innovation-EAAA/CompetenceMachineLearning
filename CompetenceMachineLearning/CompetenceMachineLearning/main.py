import DBhandler
from Competence import Competence
import model

if __name__ == '__main__':
    db = DBhandler.DBHandler()



    mod = model.Model()
    mod.addStandardLayer(22)
    mod.addStandardLayer(244)
    mod.addStandardLayer(21)
    mod.createModel()
