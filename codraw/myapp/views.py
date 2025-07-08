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


@api_view(['GET','POST'])
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

@api_view(['GET','PUT'])
def settings(request):
    pass

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
@ensure_csrf_cookie
def save(request):
    data=json.loads(request.body)
    room=data.get('project')
    payload=data.get('payload')
    if(database.find_room(room)):
        database.save_project(room,payload)
        return Response({'status':200})
    return Response({'status':400})

@api_view(['POST'])
@ensure_csrf_cookie
def save_new(request):
    data=json.loads(request.body)
    project=data.get('project')
    owner=data.get('owner')
    payload=data.get('payload')
    title=data.get('title')
    description=data.get('description')
    type=data.get('type')
    if database.save_new_project(project,payload,owner,title,description,type):
        return Response({'status':200})
    return Response({'status':500})