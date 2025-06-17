from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json
from . import database
from dotenv import load_dotenv
load_dotenv()

@api_view(['POST'])
def SignUp(request):
    username = request.data.get('username')
    password = request.data.get('password')
    mail = request.data.get('mail')
    if database.add_user(username,mail,password):
        return Response({"status":200})
    else:
        return Response({"status":400})
    
@api_view(['POST'])
def Verify(request):
    username = request.data.get('username')
    code=request.data.get('code')
    mail = request.data.get('mail')
    if database.check_code(username,mail,code):
        jwt=""
        return Response({"status":200,"jwt":jwt})
    database.delete_user(mail)
    return Response({"status":400})

@api_view(['POST'])
def SignIn(request):
    name_or_mail = request.data.get('username')
    password = request.data.get('password')
    if database.check_user(name_or_mail,password):
        jwt=""
        return Response({"status":200,"jwt":jwt})
    return Response({"status":400})