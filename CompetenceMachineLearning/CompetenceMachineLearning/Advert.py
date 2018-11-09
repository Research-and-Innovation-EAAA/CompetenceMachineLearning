class Advert(object):
    _id = 0
    numberFormat_body = ""
    matchCurrentCompetence = 0

    def __init__(self, _id, numberFormat_body, matchCurrentCompetence):
        self._id = id;
        self.numberFormat_body = numberFormat_body;
        self.matchCurrentCompetence = matchCurrentCompetence

    def __str__(self):
        return "Numberformat: " + self.numberFormat_body + ", ID: " + str(self._id) + ", Should match?: " + matchCurrentCompetence


