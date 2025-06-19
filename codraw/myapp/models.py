from mongoengine import Document, fields

class User(Document):
    id=fields.ObjectIdField(primary_key=True, auto_create=True)
    username=fields.StringField(required=True,max_length=30)
    mail=fields.EmailField(unique=True,required=True,max_length=100)
    password=fields.StringField(required=True,max_length=255)
    code=fields.StringField(max_length=5)

