from . import models
from werkzeug.security import check_password_hash, generate_password_hash
import random

def generate_code()->str:
    code=""
    for i in range(5):
        code+=str(random.randint(0,9))
    return code


def encode_user(mail:str)->str | None:
    try:
        user = models.User.objects.get(mail=mail)
        return str(user.id)
    except models.User.DoesNotExist:
        return None
    except Exception as e:
        print(f"Error encoding user: {e}")
        return None
    
def decode_user(encoded:models.User.id)->str | None:
    try:
        return models.User.objects.get(id=encoded).mail
    except models.User.DoesNotExist:
        return None



def delete_user(mail:str)->None:
    try:
        user = models.User.objects.get(mail=mail)
        user.delete()
    except Exception as e:
        print(f"Error deleting user: {e}")

def add_user(username:str,mail:str,password:str)->bool:
    if models.User.objects.filter(mail=mail, valid=True).count() > 0:
        return False
    if models.User.objects.filter(mail=mail, valid=False).count() > 0:
        existing_user = models.User.objects.get(mail=mail, valid=False)
        existing_user.username = username
        existing_user.password = generate_password_hash(password) 
        existing_user.code = generate_code()
        existing_user.save()  
        return True
    hashed_password = generate_password_hash(password)
    models.User.objects.create(username=username, mail=mail, password=hashed_password, code=generate_code(),valid=False)
    return True


def check_code(mail:str,code:str)->bool:
    try:
        entry = models.User.objects.get(mail=mail)
        if code == entry.code:
            entry.valid = True
            entry.save()
            return True
        return False
    except models.User.DoesNotExist:
        return False

def check_user(mail:str,password:str)->bool:
    try:
        user = models.User.objects.get(mail=mail)
        return (check_password_hash(user.password, password) and user.valid)
    except models.User.DoesNotExist:
        return False
    except Exception as e:
        print(f"Error checking user: {e}")
        return False

def get_user(mail:str)-> models.User | None:
    try:
        model = models.User.objects.get(mail=mail)
        return model
    except models.User.DoesNotExist:
        return None
    except Exception as e:
        print(f"Error retrieving user: {e}")
        return None
    
def get_code(mail:str)->str:
    try:
        entry = models.User.objects.get(mail=mail)
        return entry.code
    except models.User.DoesNotExist:
        return ""
    except Exception as e:
        print(f"Error retrieving code: {e}")
        return ""
    

def find_room(room:str)->bool:
    return models.Board.objects.filter(room=room)==0

def save_project(room:str,payload:str)->bool:
    try:
        entry=models.Board.objects.get(room=room)
        entry.board=payload
        entry.save()
        return True
    except models.Board.DoesNotExist:
        print('quick save object does not exist')
    except Exception as e:
        print(e)
    finally:
        return False