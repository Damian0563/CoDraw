from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json
from dotenv import load_dotenv
load_dotenv()

@api_view(['POST'])
def SignUp(request):
    username = request.data.get('username')
    password = request.data.get('password')
    mail = request.data.get('mail')
    print(username, mail, password)
    return Response({"status":200})
