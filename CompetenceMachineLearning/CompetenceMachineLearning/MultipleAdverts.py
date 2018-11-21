class MultipleAdverts(object):
    #_id = 0
    searchable_body = ""
    kompetence = []

    def __init__(self, searchable_body, kompetence):
        #self._id = _id;
        self.searchable_body = searchable_body;
        self.kompetence = kompetence

    def __str__(self):
        return "searchable_body: " + self.searchable_body + ", Should match?: " + self.kompetence


