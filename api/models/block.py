import mongoengine
from transactions import Transaction


class Block(mongoengine.Document):
    index = mongoengine.IntField()
    timestamp = mongoengine.FloatField()
    transactions = mongoengine.ListField(mongoengine.ReferenceField(Transaction))
    proof = mongoengine.IntField()
    previous_hash = mongoengine.StringField
