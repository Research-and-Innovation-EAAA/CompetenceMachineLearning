class Competence(object):
    name = ""
    id = 0

    def __init__(self, id, name):
        self.id = id;
        self.name = name;

    def __str__(self):
        return "Name: " + self.name + ", ID: " + str(self.id)


