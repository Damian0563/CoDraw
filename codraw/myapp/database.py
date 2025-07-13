from . import models
from werkzeug.security import check_password_hash, generate_password_hash
from typing import List, Dict
import random
import base64
from io import BytesIO
from bson import Binary

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
    return models.Board.objects.filter(room=room)

def save_project(room:str,payload:str)->bool:
    try:
        entry = models.Board.objects.get(room=room)
        if payload.startswith("data:"):
            payload = payload.split(",", 1)[1]
        image_data = base64.b64decode(payload)
        file_obj = BytesIO(image_data)
        if entry.board:
            entry.board.replace(file_obj, content_type="image/png")
        else:
            entry.board.put(file_obj, content_type="image/png")
        entry.save()
        return True
    except models.Board.DoesNotExist:
        print(f'[Quick Save] Room "{room}" not found.')
        return False
    except Exception as e:
        print(f'[Quick Save] Error: {e}')
        return False
    
def save_new_project(room:str,payload:str,owner:str,title:str,description:str,type:str)->bool:
    try:
        image_data = base64.b64decode(payload.split(',')[1])
        file_obj = BytesIO(image_data)
        board = models.Board(
            owner=decode_user(owner),
            room=room,
            title=title,
            description=description,
            visibility=type,
        )
        board.board.put(file_obj, content_type='image/png')
        board.save()
        return True
    except Exception as e:
        print(e)
        return False
    
def get_boards(id: str) -> List[Dict[str, str]]:
    try:
        entries = models.Board.objects.filter(owner=decode_user(id))
        res = [
            {
                "room": entry.room,
                "title": entry.title,
                "description": entry.description,
                "visibility": entry.visibility,
            }
            for entry in entries
        ]
        return res
    except models.Board.DoesNotExist:
        return []
    except Exception as e:
        print(e)
        return []
    
def get_board_img(room: str) -> str:
    # try:
    #     entry = models.Board.objects.get(room=room)
    #     if entry.board and entry.board.grid_id:
    #         img_data = entry.board.read()
    #         base64_str = base64.b64encode(img_data).decode('utf-8')
    #         return f'data:image/png;base64,{base64_str}'
    #     else:
    #         return ""
    # except models.Board.DoesNotExist:
    #     return ""
    # except Exception as e:
    #     print(f'[get_board_img] Error: {e}')
    #     return ""
    try:
        entry = models.Board.objects.get(room=room)
        if entry.board and entry.board.name:  # or .path
            with entry.board.open("rb") as f:
                img_data = f.read()
            base64_str = base64.b64encode(img_data).decode("utf-8")
            return f"data:image/png;base64,{base64_str}"
        else:
            return ""
    except models.Board.DoesNotExist:
        return ""
    except Exception as e:
        print(f"[get_board_img] Error: {e}")
        return ""
        