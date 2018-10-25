import mongoengine


class Transaction(mongoengine.Document):
    sender = mongoengine.StringField()
    recipient = mongoengine.StringField()
    amount = mongoengine.StringField()
