from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import database
from . import mail as mailing
from dotenv import load_dotenv
load_dotenv()

@api_view(['POST'])
def SignUp(request):
    username = request.data.get('username')
    password = request.data.get('password')
    mail = request.data.get('mail') 
    if database.add_user(username,mail,password):
        code = database.get_code(username,mail)
        if code!="":
            mailing.account_creation(mail,code)
            return Response({"status":200})
    return Response({"status":400})
    
@api_view(['POST'])
def Verify(request):
    username = request.data.get('username')
    code=request.data.get('code')
    mail = request.data.get('mail')
    if database.check_code(username,mail,code):
        response = Response({"status":200})
        return response
    return Response({"status":400})

@api_view(['GET','POST'])
def SignIn(request):
    if request.method == 'GET':
        if request.session.get('user_id') is not None:
            return Response({"status":300,"url":"/codraw"})
        elif request.COOKIES.get('token') is not None:
            encoded = request.COOKIES.get('token')
            mail = database.decode_user(encoded)
            if mail is not None:
                request.session['user_id'] = encoded
                return Response({"status":200,"url":"/codraw"})
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

@api_view(['POST'])
def home(request):
    if request.user.is_authenticated:
        return Response({"status":200,"message":"token is valid"})
    return Response({"status":400,"message":"invalid token"})


@api_view(['GET','POST'])
def main(request):
    return Response({"status":200,"message":"Welcome to CoDraw API"})