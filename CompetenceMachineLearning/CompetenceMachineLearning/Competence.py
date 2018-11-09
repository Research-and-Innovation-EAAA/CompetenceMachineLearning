class Competence(object):
    _id = 0
    prefferredLabel = ""

    def __init__(self, _id, prefferredLabel):
        self._id = id;
        self.prefferredLabel = prefferredLabel;

    def __str__(self):
        return "Name: " + self.prefferredLabel + ", ID: " + str(self._id)


