class Advert(object):
    _id = 0
    body = ""
    competence = 0

    def __init__(self, advert_id, body, competence):
        self.advert_id = advert_id
        self.body = body
        self.competence = competence


