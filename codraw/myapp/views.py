from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import ensure_csrf_cookie
from uuid import uuid4
import json
from . import database
from . import mail as mailing
from dotenv import load_dotenv
load_dotenv()

@api_view(['GET','POST'])
@ensure_csrf_cookie
def SignUp(request):
    if request.method == 'GET':
        if request.session.get('user_id') is not None:
            return Response({"status":300,"url":"/codraw"})
        elif request.COOKIES.get('token') is not None:
            encoded = request.COOKIES.get('token')
            mail = database.decode_user(encoded)
            if mail is not None:
                request.session['user_id'] = encoded
                return Response({"status":300,"url":"/codraw"})
        return Response({"status":400,"message":"No session found"})
    elif request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        mail = request.data.get('mail') 
        if database.add_user(username,mail,password):
            code = database.get_code(mail)
            if code!="":
                mailing.account_creation(mail,code)
                return Response({"status":200})
        return Response({"status":400})
    
@api_view(['POST'])
@ensure_csrf_cookie
def Verify(request):
    username = request.data.get('username')
    code=request.data.get('code')
    mail = request.data.get('mail')
    if database.check_code(mail,code):
        response = Response({"status":200})
        response=Response({"status":200})
        encoded=database.encode_user(mail)
        request.session['user_id'] = encoded
        return response
    return Response({"status":400})

@api_view(['GET','POST'])
@ensure_csrf_cookie
def SignIn(request):
    if request.method == 'GET':
        if request.session.get('user_id') is not None:
            return Response({"status":300,"url":"/codraw"})
        elif request.COOKIES.get('token') is not None:
            encoded = request.COOKIES.get('token')
            mail = database.decode_user(encoded)
            if mail is not None:
                request.session['user_id'] = encoded
                return Response({"status":300,"url":"/codraw"})
        return Response({"status":400,"message":"No session found"})
    elif request.method == 'POST':
        mail= request.data.get('mail')
        password = request.data.get('password')
        remember = request.data.get('remember', False)
        if database.check_user(mail,password):
            response=Response({"status":200})
            encoded=database.encode_user(mail)
            request.session['user_id'] = encoded
            if remember:
                response.set_cookie(
                    key='token',
                    value=encoded,
                    httponly=True,
                    secure=True,  # Use True if using HTTPS
                    samesite='Lax',  # Adjust as needed
                )
            return response
        return Response({"status":400})

@api_view(['GET'])
@ensure_csrf_cookie
def home(request):
    if request.session.get('user_id') is not None:
        return Response({"status":300,"url":"/codraw"})
    elif request.COOKIES.get('token') is not None:
        encoded = request.COOKIES.get('token')
        mail = database.decode_user(encoded)
        if mail is not None:
            request.session['user_id'] = encoded
            return Response({"status":300,"url":"/codraw"})
    return Response({"status":400,"message":"No session found"})


@api_view(['GET'])
@ensure_csrf_cookie
def main(request):
    if request.method == 'GET':
        if request.session.get('user_id') is not None:
            return Response({"status":200,"message":"Session found"})
        elif request.COOKIES.get('token') is not None:
            encoded = request.COOKIES.get('token')
            mail = database.decode_user(encoded)
            if mail is not None:
                request.session['user_id'] = encoded
                return Response({"status":200,"message":"Cookie found"})
        return Response({"status":400,"message":"No session found"})

@api_view(['GET','POST'])
def account(request):
    pass

@api_view(['GET'])
@ensure_csrf_cookie
def get_url(request):
    try:
        id=request.session['user_id']
    except KeyError:
        id=request.COOKIES.get('token')
    if id is not None:
        return Response({'status':200,'url':f"/board/{id}/{str(uuid4())}"})
    return Response({'status':400})

@api_view(['POST'])
def load(request):
    if request.method=="POST":
        try:  
            data=json.loads(request.body)
            room=data['project']
            canva,bg=database.get_board_img(room=room)
            return Response({'status':200,"canva":json.loads(canva),"bg":bg})
        except Exception: return Response({'status':404,"canva":""})

@api_view(["POST"])
@ensure_csrf_cookie
def load_board(request):
    if request.method=='POST':
        id=None
        try:
            id=request.session['user_id']
        except KeyError:
            id=request.COOKIES.get('token')
        finally:
            if id is not None:
                data=json.loads(request.body)
                url=f"/board/{id}/{data['room']}"
                database.increase_view_count(data['room'])
                return Response({'status':200,"url":url})
            else:
                return Response({'status':400})

@ensure_csrf_cookie
@api_view(['POST'])
def my_projects(request):
    try:
        id=None
        try:
            id=request.session['user_id']
        except KeyError:
            id=request.COOKIES.get('token')
        finally:
            if id is not None:
                data=json.loads(request.body)
                timezone=data['timezone']
                boards=database.get_boards(id,timezone)
                return Response({'status':200,"boards":boards})
            return Response({'status':400})
    except KeyError:
        return Response({'status':500})

@api_view(['GET','PUT'])
def settings(request):
    pass

@api_view(['GET'])
@ensure_csrf_cookie
def status(request):
    id=None
    try:
        id=request.session['user_id']
    except KeyError:
        id=request.COOKIES.get('token')
    finally:
        print(id)
        if id is not None and database.exists(id):
            return Response({'status':200,"user":True})
        return Response({'status':200,'user':False})

@api_view(['GET'])
@ensure_csrf_cookie
def delete(request,room):
    id=None
    try:
        id=request.session['user_id']
    except KeyError:
        id=request.COOKIES.get('token')
    finally:
        if id is not None:
            if database.delete_board(room):return Response({'status':200})
        return Response({'status':400})


@api_view(['GET'])
@ensure_csrf_cookie
def username(request):
    id=None
    try:
        id=request.session['user_id']
    except KeyError:
        id=request.COOKIES.get('token')
    finally:
        if id is not None:
            mail=database.decode_user(id)
            username=database.get_username(mail)
            return Response({'status':200,'username':username})
        return Response({'status':404})

@api_view(['POST'])
@ensure_csrf_cookie
def edit(request,room):
    id=None
    try:
        id=request.session['user_id']
    except KeyError:
        id=request.COOKIES.get('token')
    finally:
        if id is not None:
            data=json.loads(request.body)
            title=data['title']
            description=data['description']
            timezone=data['timezone']
            database.edit(room,title,description,timezone)
        return Response({'status':400})

@api_view(['POST'])
@ensure_csrf_cookie
def logout(request):
    request.session.flush()
    response = Response({"status":200,"message":"Logged out successfully"})
    response.delete_cookie('token')
    return response

@api_view(['GET','POST'])
@ensure_csrf_cookie
def board(request,id,room):
    return Response({'status':200})

@api_view(['GET','POST'])
def save(request):
    data=json.loads(request.body)
    owner=None
    try:
        owner=request.session['user_id']
    except KeyError:
        owner=request.COOKIES.get('token')
    room=data.get('project')
    if database.find_room(room,owner):
        bg=data.get('bg')
        payload=data.get('payload')
        if payload is not None:
            database.save_project(room,payload,bg)
        return Response({'status':200})
    return Response({'status':400})

@api_view(['POST'])
@ensure_csrf_cookie
def boards_user(request,username):
    id=None
    try:
        id=request.session['user_id']
    except KeyError:
        id=request.COOKIES.get('token')
    finally:
        if id is not None:
            data=json.loads(request.body)
            timezone=data['timezone']
            boards=database.get_boards_of_username(timezone,username)
            return Response({'status':200,"boards":boards})
        return Response({'status':400,'boards':[]})

@api_view(['POST'])
@ensure_csrf_cookie
def save_new(request):
    data=json.loads(request.body)
    project=data.get('project')
    payload=data.get('payload')
    title=data.get('title')
    description=data.get('description')
    type=data.get('type') 
    background=data.get('bg')
    owner=None
    try:
        owner=request.session['user_id']
    except KeyError:
        owner=request.COOKIES.get('token')
    finally:
        if owner is not None and database.save_new_project(project,payload,owner,title,description,type,background):
            return Response({'status':200})
        return Response({'status':400})

@api_view(['POST'])
@ensure_csrf_cookie
def check_owner(request):
    data=json.loads(request.body)
    owner=data['owner']
    room=data['room']
    id=None
    try:
        id=request.session['user_id']
    except KeyError:
        id=request.COOKIES.get('token')
    finally:
        if id==owner and database.check_ownership(database.decode_user(owner),room):
            return Response({'status':200})
        return Response({'status':400})
    
@api_view(['POST'])
@ensure_csrf_cookie
def check_bookmark(request,room):
    id=None
    try:
        id=request.session['user_id']
    except KeyError:
        id=request.COOKIES.get('token')
    finally:
        if id is not None and database.check_bookmark(room,id): return Response({'status':200,"bookmarked":True})
        return Response({'status':403,'bookmarked':False})

@api_view(['POST'])
@ensure_csrf_cookie
def bookmark(request,room):
    id=None
    try:
        id=request.session['user_id']
    except KeyError:
        id=request.COOKIES.get('token')
    finally:
        if id is not None:
            data=json.loads(request.body)
            me=data['user']
            curr_bookmark=data['status']
            if database.modify_bookmark(me,curr_bookmark,room):
                if curr_bookmark: return Response({'status':200,'bookmarked':False})
                else: return Response({'status':200,'bookmarked':True})
            return Response({'status':200,'bookmarked':False})
        return Response({'status':400})

@api_view(['POST'])
@ensure_csrf_cookie
def get_bookmarks(request,username):
    id=None
    try:
        id=request.session['user_id']
    except KeyError:
        id=request.COOKIES.get('token')
    finally:
        if id is not None:
            data=json.loads(request.body)
            timezone=data['timezone']
            bookmarks=database.get_bookmarks(username,timezone)
            #print(bookmarks)
            return Response({'status':200,'bookmarks':bookmarks})
        return Response({'status':400,'bookmarks':[]})

@api_view(['GET'])
@ensure_csrf_cookie
def delete_bookmark(request,room):
    id=None
    try:
        id=request.session['user_id']
    except KeyError:
        id=request.COOKIES.get('token')
    finally:
        if id is not None and database.delete_bookmark(id,room):
            return Response({'status':200})
        return Response({'status':400})

@api_view(['POST'])
@ensure_csrf_cookie
def trending(request):
    id=None
    try:
        id=request.session['user_id']
    except KeyError:
        id=request.COOKIES.get('token')
    finally:
        if id is not None:
            data=json.loads(request.body)
            timezone=data['timezone']  
            boards=database.get_trending(id,timezone)  
            return Response({'status':200,'boards':boards})
        return Response({'status':400,'boards':''})
    
@api_view(['POST'])
@ensure_csrf_cookie
def search(request):
    id=None
    try:
        id=request.session['user_id']
    except KeyError:
        id=request.COOKIES.get('token')
    finally:
        if id is not None:
            data=json.loads(request.body)
            query=data['query']
            timezone=data['timezone']
            result=database.get_matches(query,timezone)
            #print(result)
            return Response({"status":200,"boards":result})
        return Response({"status":400})