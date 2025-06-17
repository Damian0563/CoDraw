from . import models
from werkzeug.security import check_password_hash, generate_password_hash
import random

def generate_code()->str:
    code=""
    for i in range(5):
        code+=str(random.randint(0,9))
    print(code)
    return code

def delete_user(mail:str)->None:
    try:
        user = models.User.objects.get(mail=mail)
        user.delete()
    except Exception as e:
        print(f"Error deleting user: {e}")

def add_user(username:str,mail:str,password:str)->bool:
    if models.User.objects.filter(mail=mail).count() > 0:
        return False
    hashed_password = generate_password_hash(password)
    models.User.objects.create(username=username, mail=mail, password=hashed_password, code=generate_code())
    return True


def check_code(username:str,mail:str,code:str)->bool:
    try:
        entry = models.User.objects.get(username=username, mail=mail)
        if code == entry.code:
            return True
        return False
    except models.User.DoesNotExist:
        return False

def check_user(name_or_mail:str,password:str)->bool:
    return True