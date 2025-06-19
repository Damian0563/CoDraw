from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken    
from . import database
from . import mail as mailing
from .auth import CookieJWTAuthentication
from dotenv import load_dotenv
load_dotenv()

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
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
@authentication_classes([])
@permission_classes([AllowAny])
def Verify(request):
    username = request.data.get('username')
    code=request.data.get('code')
    mail = request.data.get('mail')
    if database.check_code(username,mail,code):
        refresh = RefreshToken.for_user(database.get_user(mail))
        response = Response({"status":200})
        response.set_cookie(
            key='jwt',
            value=str(refresh.access_token),
            httponly=True,
            secure=True,  # Set to True if using HTTPS
            max_age=3600  # Cookie expiration time in seconds
        )
        return response
    database.delete_user(mail)
    return Response({"status":400})

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def SignIn(request):
    mail= request.data.get('mail')
    password = request.data.get('password')
    remember = request.data.get('remember', False)
    if database.check_user(mail,password):
        refresh = RefreshToken.for_user(database.get_user(mail))
        #print(refresh.access_token)
        response=Response({"status":200})
        if remember:
            response.set_cookie(
                key='jwt',
                value=str(refresh.access_token),
                httponly=True,
                secure=True,
                max_age=3600*120 
            )
            return response
        else:
            response.set_cookie(
                key='jwt',
                value=str(refresh.access_token),
                httponly=True,  
                secure=True,
                max_age=3600 
            )
            return response
    return Response({"status":400})

@api_view(['POST'])
@authentication_classes([CookieJWTAuthentication])
@permission_classes([AllowAny])
def home(request):
    print(request.user)
    if request.user.is_authenticated:
        return Response({"status":200,"message":"token is valid"})
    return Response({"status":400,"message":"invalid token"})


@api_view(['POST'])
@authentication_classes([CookieJWTAuthentication])
@permission_classes([IsAuthenticated])
def main(request):
    return Response({"status":200,"message":"Welcome to CoDraw API"})