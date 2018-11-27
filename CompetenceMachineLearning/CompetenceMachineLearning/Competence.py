class Competence(object):
    _id = 0
    preferredLabel = ""

    def __init__(self, _id, preferredLabel):
        self._id = _id;
        self.preferredLabel = preferredLabel;

    def __str__(self):
        return "Name: " + self.preferredLabel + ", ID: " + str(self._id)


