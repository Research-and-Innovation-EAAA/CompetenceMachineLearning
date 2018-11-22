class Advert(object):
    _id = 0
    body = ""
    matchCurrentCompetence = 0

    def __init__(self, _id, body, matchCurrentCompetence):
        self._id = _id;
        self.body = body;
        self.matchCurrentCompetence = matchCurrentCompetence

    def __str__(self):
        return "Body: " + self.body + ", ID: " + str(self._id) + ", Should match?: " + str(self.matchCurrentCompetence)


