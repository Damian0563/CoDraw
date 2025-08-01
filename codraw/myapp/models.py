from mongoengine import Document, fields

class User(Document):
    username=fields.StringField(required=True,max_length=30)
    mail=fields.EmailField(unique=True,required=True,max_length=100)
    password=fields.StringField(required=True,max_length=255)
    code=fields.StringField(max_length=5)
    valid=fields.BooleanField(default=False)

class Board(Document):
    owner=fields.EmailField(max_length=100)
    board=fields.StringField(required=True)
    room=fields.StringField(required=True)
    description=fields.StringField(max_length=512)
    title=fields.StringField(required=True,max_length=100)
    visibility=fields.StringField(required=True,max_length=10)
    # background=fields.StringField(required=True)