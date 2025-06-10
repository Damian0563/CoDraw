from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from dotenv import load_dotenv
load_dotenv()

@api_view(['POST'])
def main(req):
    return Response("Hello")
