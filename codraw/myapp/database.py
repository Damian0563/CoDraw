from . import models
from werkzeug.security import check_password_hash, generate_password_hash
from typing import List, Dict
import random, json
import time
from zoneinfo import ZoneInfo
from datetime import datetime, timezone
import nltk
from nltk.stem import WordNetLemmatizer
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

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
    

def find_room(room:str,owner:str)->bool:
    return models.Board.objects.filter(room=room)
    #return models.Board.objects.filter(room=room,owner=decode_user(owner))


def edit(room:str,title:str,description:str,timezone:str)->None:
    try:
        client_tz = ZoneInfo(timezone)
        entry=models.Board.objects.get(room=room)
        entry.title=title
        entry.description=description
        entry.last_edit=str(time.time())
        concat=str(str(title)+". "+str(description))
        tokenized=nltk.word_tokenize(concat)
        tags=nltk.pos_tag(tokenized)
        lemmatizer=WordNetLemmatizer()
        result=[]
        for instance in tags:
            word,word_type=instance[0],instance[1]
            word=word.lower()
            if word_type.startswith("NN"): result.append(lemmatizer.lemmatize(word,"n"))
            elif word_type.startswith("V"): result.append(lemmatizer.lemmatize(word,"v"))
            elif word_type.startswith("JJ"): result.append(lemmatizer.lemmatize(word,"a"))
        entry.summary=json.dumps(list(set(result)))
        entry.save()
    except models.Board.DoesNotExist:
        pass

def delete_board(room:str)->bool:
    try:
        board=models.Board.objects.get(room=room)
        board.delete()
        return True
    except models.Board.DoesNotExist:
        return False

def get_boards(id: str,timezone:str) -> List[Dict[str, str]]:
    try:
        client_tz = ZoneInfo(timezone)
        entries=models.Board.objects.filter(owner=decode_user(id))
        res=[
            {
                "room": entry.room,
                "title": entry.title,
                "description": entry.description,
                "visibility": entry.visibility,
                "views":entry.views,
                "modified":(datetime.fromtimestamp(float(entry.last_edit))).astimezone(client_tz).strftime("%H:%M    %d/%m/%Y")
            }
            for entry in entries
        ]
        return res
    except models.Board.DoesNotExist:
        return []
    # except Exception as e:
    #     print(e)
    #     return []

def get_mail_by_username(username:str)->str:
    try:
        print(username)
        entry=models.User.objects.get(username=username)
        return entry.mail
    except models.User.DoesNotExist:
        return ""

def get_boards_of_username(timezone:str,username:str)->list[dict]:
    try:
        client_tz = ZoneInfo(timezone)
        mail=get_mail_by_username(username)
        print(mail)
        entries=models.Board.objects.filter(owner=mail)
        res=[
            {
                "room": entry.room,
                "title": entry.title,
                "description": entry.description,
                "visibility": entry.visibility,
                "views":entry.views,
                "modified":(datetime.fromtimestamp(float(entry.last_edit))).astimezone(client_tz).strftime("%H:%M    %d/%m/%Y")
            }
            for entry in entries
        ]
        return res
    except models.Board.DoesNotExist:
        return []

def add_bookmark()->None:
    pass

def check_bookmark(room:str,id:str)->bool:
    mail=decode_user(id)
    return room in models.User.objects.get(mail=mail).bookmarks

def exists(id: str) -> bool:
    return models.User.objects.filter(id=id).count() > 0

def check_ownership(mail:str,room:str)->bool:
    return models.Board.objects.filter(owner=mail,room=room).count()>0

def get_username(email:str)->str:
    try:
        entry=models.User.objects.get(mail=email)
        return entry.username
    except Exception: pass


def get_trending(id:str,timezone:str)->list[Dict[str,str]]:
    try:
        client_tz = ZoneInfo(timezone)
        entries=models.Board.objects.filter(owner__ne=decode_user(id), visibility='Public').order_by('-views')[:9]
        res=[
            {
                "room": entry.room,
                "title": entry.title,
                "description": entry.description,
                "views": entry.views,
                "owner":get_username(entry.owner),
                "modified":(datetime.fromtimestamp(float(entry.last_edit))).astimezone(client_tz).strftime("%H:%M    %d/%m/%Y")
            }
            for entry in entries
        ]
        return res
    except models.Board.DoesNotExist:
        return []
    except Exception as e:
        print(e)
        return []

def increase_view_count(room:str)->None:
    try:
        entry=models.Board.objects.get(room=room)
        entry.views+=1
        entry.save()
    except Exception: pass

def get_matches(sentence:str,timezone:str)->list:
    try:
        tokenized=nltk.word_tokenize(sentence)
        tags=nltk.pos_tag(tokenized)
        lemmatizer=WordNetLemmatizer()
        result=[]
        for entry in tags:
            word,word_type=entry[0],entry[1]
            word=word.lower()
            if word_type.startswith("NN"): result.append(lemmatizer.lemmatize(word,"n"))
            elif word_type.startswith("V"): result.append(lemmatizer.lemmatize(word,"v"))
            elif word_type.startswith("JJ"): result.append(lemmatizer.lemmatize(word,"a"))
        keywords=list(set(result))
        if len(keywords)==0: return []
        matches=models.Board.objects.filter(summary__icontains=keywords[0]) if keywords else models.Board.objects.none()
        def match_count(board):
            try:
                board_keywords = set(json.loads(board.summary))
            except (TypeError, json.JSONDecodeError):
                board_keywords = set()
            #print(len(set(keywords) & board_keywords))
            return len(set(keywords) & board_keywords)
        client_tz=ZoneInfo(timezone)
        sorted_boards = sorted(matches, key=match_count, reverse=True)
        boards_list = [
            {
                "room": board.room,
                "title": board.title,
                "description": board.description,
                "visibility": board.visibility,
                "summary": board.summary,
                "views": board.views,
                "modified":(datetime.fromtimestamp(float(board.last_edit))).astimezone(client_tz).strftime("%H:%M    %d/%m/%Y")
            }
            for board in sorted_boards
        ]
        return json.dumps(boards_list)
    except Exception as e:
        print(e)
        return []

def save_project(room:str,payload:str,bg:str)->bool:
    try:
        entry=models.Board.objects.get(room=room)
        entry.board=payload
        entry.background=bg
        entry.last_edit=str(time.time())
        entry.save()  
        return True
    except Exception as e:
        print(payload)
        print('quick save error: ',e)
        return False
    
def save_new_project(room: str, payload: str, owner: str, title: str, description: str, type: str,bg:str) -> bool:
    try:
        summary=str(str(title)+". "+str(description))
        tokenized=nltk.word_tokenize(summary)
        tags=nltk.pos_tag(tokenized)
        lemmatizer=WordNetLemmatizer()
        result=[]
        for entry in tags:
            word,word_type=entry[0],entry[1]
            word=word.lower()
            if word_type.startswith("NN"): result.append(lemmatizer.lemmatize(word,"n"))
            elif word_type.startswith("V"): result.append(lemmatizer.lemmatize(word,"v"))
            elif word_type.startswith("JJ"): result.append(lemmatizer.lemmatize(word,"a"))
        result=json.dumps(list(set(result)))
        entry=models.Board.objects.create(
            owner=decode_user(owner),
            board=payload,
            room=room,
            description=description,
            visibility=type,
            title=title,
            summary=result,
            background=bg,
            views=1,
            last_edit=str(time.time())
        )
        entry.save()
        return True
    except Exception as e:
        print('save new project error: ',e)
        return False

def get_board_img(room: str)->list|str:
    try:
        entry=models.Board.objects.get(room=room)
        return [entry.board,entry.background]
    except Exception as e:
        print("Error in fetching image: ",e)
        return ""
    




    


        