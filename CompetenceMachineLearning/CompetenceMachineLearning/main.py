import DBhandler
import model

if __name__ == '__main__':
    mod = model.Model()
    mod.addStandardLayer(22)
    mod.addStandardLayer(244)
    mod.addStandardLayer(21)
    #app = DBhandler.DBHandler()
    #app.retrive()
    mod.createModel()
