from mongoengine import Document, fields

class User(Document):
    username=fields.StringField(required=True,max_length=30)
    mail=fields.EmailField(unique=True,required=True,max_length=100)
    password=fields.StringField(required=True,max_length=255)
    code=fields.StringField(max_length=5)
    valid=fields.BooleanField(default=False)

class Visitior(Document):
    pass
