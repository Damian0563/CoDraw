from django.shortcuts import render,redirect # type: ignore
import json
from django.urls import reverse #type:ignore
from django.http import JsonResponse # type: ignore
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt # type: ignore
from django.http import HttpResponse # type: ignore
from uuid import uuid4 # type: ignore
import os
from dotenv import load_dotenv
load_dotenv()

def main(request):
    return render(request,"landing.html")
