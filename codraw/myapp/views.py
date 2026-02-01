from rest_framework.decorators import api_view  # ignore
from rest_framework.response import Response
from django.views.decorators.csrf import ensure_csrf_cookie
from django_ratelimit.decorators import ratelimit
from uuid import uuid4
from codraw.redis_client import get_redis_client
import json
import os
from . import helpers
from . import database
from . import mail as mailing
from dotenv import load_dotenv
from .metrics import Metrics
from .google import Bucket
load_dotenv()
redis_client = get_redis_client()
bucket = Bucket()


@api_view(['GET', 'POST'])
@ensure_csrf_cookie
@ratelimit(key='ip', rate='30/m', block=True)
def SignUp(request):
    if request.method == 'GET':
        if request.session.get('user_id') is not None:
            return Response({"status": 300, "url": "/codraw"})
        elif request.COOKIES.get('token') is not None:
            encoded = request.COOKIES.get('token')
            mail = database.decode_user(encoded)
            if mail is not None:
                request.session['user_id'] = encoded
                return Response({"status": 300, "url": "/codraw"})
        return Response({"status": 400, "message": "No session found"})
    elif request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        mail = request.data.get('mail')
        if database.add_user(username, mail, password):
            code = database.get_code(mail)
            if code != "":
                mailing.account_creation(mail, code)
                Metrics.signup.inc()
                return Response({"status": 200})
        return Response({"status": 400})


@api_view(['POST'])
@ensure_csrf_cookie
@ratelimit(key='ip', rate='30/m', block=True)
def google_signup(request):
    if request.method == 'POST':
        data = request.data
        token = data.get('token')
        email = data.get('email')
        name = data.get('name')
        if database.add_user(name, email, token):
            response = Response({"status": 200})
            encoded = database.encode_user(email)
            request.session['user_id'] = encoded
            request.session.save()
            response.set_cookie(
                key='token',
                value=encoded,
                httponly=True,
                secure=True,
                samesite='Lax',
            )
            return Response({"status": 300})
        return Response({"status": 400})


@api_view(['POST'])
@ensure_csrf_cookie
@ratelimit(key='ip', rate='3/m', block=True)
def Verify(request):
    code = request.data.get('code')
    mail = request.data.get('mail')
    if database.check_code(mail, code):
        response = Response({"status": 200})
        encoded = database.encode_user(mail)
        request.session['user_id'] = encoded
        request.session.save()
        response.set_cookie(
            key='token',
            value=encoded,
            httponly=True,
            secure=True,
            samesite='Lax',
        )
        return response
    return Response({"status": 400})


@api_view(['GET', 'POST'])
@ensure_csrf_cookie
@ratelimit(key='ip', rate='30/m', block=True)
def SignIn(request):
    if request.method == 'GET':
        if request.session.get('user_id') is not None:
            return Response({"status": 300, "url": "/codraw"})
        elif request.COOKIES.get('token') is not None:
            encoded = request.COOKIES.get('token')
            mail = database.decode_user(encoded)
            if mail is not None:
                request.session['user_id'] = encoded
                return Response({"status": 300, "url": "/codraw"})
        return Response({"status": 400, "message": "No session found"})
    elif request.method == 'POST':
        mail = request.data.get('mail')
        password = request.data.get('password')
        remember = request.data.get('remember', False)
        if database.check_user(mail, password):
            response = Response({"status": 200})
            encoded = database.encode_user(mail)
            request.session['user_id'] = encoded
            if remember:
                response.set_cookie(
                    key='token',
                    value=encoded,
                    httponly=True,
                    secure=True,
                    samesite='Lax',
                )
            Metrics.signup.inc()
            return response
        return Response({"status": 400})


@api_view(['POST'])
@ensure_csrf_cookie
@ratelimit(key='ip', rate='30/m', block=True)
def google_signin(request):
    if request.method == 'POST':
        data = request.data
        token = data.get('token')
        email = data.get('email')
        name = data.get('name')
        if database.google_user_exists(email, name, token)[0]:
            response = Response({"status": 200})
            encoded = database.encode_user(email)
            request.session['user_id'] = encoded
            request.session.save()
            response.set_cookie(
                key='token',
                value=encoded,
                httponly=True,
                secure=True,
                samesite='Lax',
            )
            Metrics.signin.inc()
            return Response({"status": 200})
        elif database.google_user_exists(email, name, token)[1] == 1:
            return Response({"status": 401})
        return Response({"status": 400})


@api_view(['GET'])
@ensure_csrf_cookie
@ratelimit(key='ip', rate='30/m', block=True)
def home(request):
    Metrics.visit_site.inc()
    if request.session.get('user_id') is not None:
        return Response({"status": 300, "url": "/codraw"})
    elif request.COOKIES.get('token') is not None:
        encoded = request.COOKIES.get('token')
        mail = database.decode_user(encoded)
        if mail is not None:
            request.session['user_id'] = encoded
            return Response({"status": 300, "url": "/codraw"})
    return Response({"status": 400, "message": "No session found"})


@api_view(['GET'])
@ensure_csrf_cookie
@ratelimit(key='ip', rate='30/m', block=True)
def main(request):
    if request.method == 'GET':
        Metrics.active_users.inc()
        if request.session.get('user_id') is not None:
            return Response({"status": 200, "message": "Session found"})
        elif request.COOKIES.get('token') is not None:
            encoded = request.COOKIES.get('token')
            mail = database.decode_user(encoded)
            if mail is not None:
                request.session['user_id'] = encoded
                return Response({"status": 200, "message": "Cookie found"})
        return Response({"status": 400, "message": "No session found"})


@api_view(['GET'])
@ensure_csrf_cookie
@ratelimit(key='ip', rate='30/m', block=True)
def get_url(request):
    id = helpers.validate_request(request)
    Metrics.create_board.inc()
    if id is not None:
        return Response({'status': 200, 'url': f"/board/{id}/{str(uuid4())}"})
    return Response({'status': 400})


@api_view(['POST'])
@ratelimit(key='ip', rate='30/m', block=True)
def load(request):
    if request.method == "POST":
        try:
            data = request.data
            room = data['project']
            if redis_client.get(f"board:{room}") and redis_client.get(f"bg:{room}"):
                canva = redis_client.get(f"board:{room}")
                bg = redis_client.get(f"bg:{room}")
                last_access = redis_client.get(f"last_access:{room}")
            else:
                canva, bg, last_access = database.get_board_img(room=room)
                redis_client.setex(f"last_access:{room}", 60*5, last_access)
                redis_client.setex(f"board:{room}", 60*5, canva)
                redis_client.setex(f"bg:{room}", 60*5, bg)
            return Response({'status': 200, "canva": json.loads(canva), "bg": bg, "last": last_access})
        except Exception:
            return Response({'status': 404, "canva": ""})


@api_view(["POST"])
@ensure_csrf_cookie
@ratelimit(key='ip', rate='30/m', block=True)
def load_board(request):
    if request.method == 'POST':
        id = helpers.validate_request(request)
        if id is not None:
            data = request.data
            url = f"/board/{id}/{data['room']}"
            database.increase_view_count(data['room'])
            return Response({'status': 200, "url": url})
        else:
            return Response({'status': 400})


@ensure_csrf_cookie
@api_view(['POST'])
@ratelimit(key='ip', rate='30/m', block=True)
def my_projects(request):
    try:
        id = helpers.validate_request(request)
        if id is not None:
            data = request.data
            timezone = data['timezone']
            if redis_client.get(f"boards:{id}"):
                boards = json.loads(redis_client.get(
                    f"boards:{id}"))
                images = redis_client.get(f"images:{id}")
            else:
                boards = database.get_boards(id, timezone)
                images = bucket.get_images([board['room'] for board in boards])
            return Response({'status': 200, "boards": boards, "images": images})
        return Response({'status': 400})
    except KeyError:
        return Response({'status': 500})


@api_view(['GET'])
@ensure_csrf_cookie
@ratelimit(key='ip', rate='30/m', block=True)
def status(request):
    id = helpers.validate_request(request)
    if id is not None and database.exists(id):
        return Response({'status': 200, "user": True})
    return Response({'status': 200, 'user': False})


@api_view(['GET'])
@ensure_csrf_cookie
@ratelimit(key='ip', rate='30/m', block=True)
def delete(request, room):
    id = helpers.validate_request(request)
    if id is not None:
        if database.delete_board(room):
            redis_client.delete(f"boards:{id}")
            return Response({'status': 200})
    return Response({'status': 400})


@api_view(['GET'])
@ensure_csrf_cookie
@ratelimit(key='ip', rate='5/m', block=True)
def restore_password(request, mail):
    if request.method == "GET":
        if helpers.valid_email(mail) and database.get_user(mail) is not None:
            code = str(uuid4())[:20]
            link = f"{os.getenv('FRONTEND_URL')}/recover/{code}"
            mailing.restore_password(mail, link)
            redis_client.setex(f"restore_password:{code}", 300, mail)
            return Response({'status': 200})
        return Response({'status': 404})
    return Response({'status': 200})


@ ensure_csrf_cookie
@ api_view(['GET', 'POST'])
@ratelimit(key='ip', rate='5/m', block=True)
def edit_password(request, code):
    if request.method == "GET":
        mail = redis_client.get(f"restore_password:{code}")
        if mail is not None:
            return Response({'status': 200})
        return Response({'status': 404})
    elif request.method == "POST":
        mail = redis_client.get(f"restore_password:{code}")
        if mail is not None:
            data = request.data
            new_password = data['new_password']
            database.update_password(mail, new_password)
            redis_client.delete(f"restore_password:{code}")
            return Response({'status': 200})
        return Response({'status': 404})


@ api_view(['GET'])
@ ensure_csrf_cookie
@ratelimit(key='ip', rate='30/m', block=True)
def username(request):
    id = helpers.validate_request(request)
    if id is not None:
        mail = database.decode_user(id)
        if mail is not None:
            username = database.get_username(mail)
            return Response({'status': 200, 'username': username})
    return Response({'status': 404})


@ api_view(['POST'])
@ ensure_csrf_cookie
@ratelimit(key='ip', rate='30/m', block=True)
def edit(request, room):
    id = helpers.validate_request(request)
    if id is not None:
        data = request.data
        title = data['title']
        description = data['description']
        timezone = data['timezone']
        database.edit(room, title, description, timezone)
    return Response({'status': 400})


@ api_view(['POST'])
@ ensure_csrf_cookie
@ratelimit(key='ip', rate='30/m', block=True)
def logout(request):
    request.session.flush()
    response = Response({"status": 200, "message": "Logged out successfully"})
    response.delete_cookie('token')
    return response


@ api_view(['GET', 'POST'])
@ ensure_csrf_cookie
def board(request, id, room):
    return Response({'status': 200})


@ api_view(['GET', 'POST'])
@ratelimit(key='ip', rate='30/m', block=True)
def save(request):
    id = helpers.validate_request(request)
    room = request.POST.get('project')
    if database.find_room(room, id):
        bg = request.POST.get('bg')
        payload = request.POST.get('payload')
        preview = request.FILES.get('preview')
        if payload is not None:
            database.save_project(room, payload, bg)
            if preview is not None:
                bucket.save(room, preview)
            redis_client.delete(f"boards:{id}")
            redis_client.delete(f"board:{room}")
            redis_client.delete(f"bg:{room}")
            redis_client.delete(f"last_access:{room}")
        return Response({'status': 200})
    return Response({'status': 400})


@api_view(['POST'])
@ensure_csrf_cookie
@ratelimit(key='ip', rate='30/m', block=True)
def load_project(request):
    data = request.data
    id = helpers.validate_request(request)
    room = data.get('project')
    if database.find_room(room, id):
        return Response({'status': 200})
    return Response({'status': 400})


@ api_view(['POST'])
@ ensure_csrf_cookie
@ratelimit(key='ip', rate='30/m', block=True)
def boards_user(request, username):
    id = helpers.validate_request(request)
    if id is not None:
        data = request.data
        timezone = data['timezone']
        user_id = database.encode_user(database.get_mail_by_username(username))
        if redis_client.get(f"boards_user:{user_id}"):
            boards = json.loads(redis_client.get(
                f"boards:{user_id}"))
        else:
            boards = database.get_boards_of_username(timezone, username)
            redis_client.setex(
                f"boards:{user_id}", 60*5, json.dumps(boards))
        return Response({'status': 200, "boards": boards})
    return Response({'status': 400, 'boards': []})


@ api_view(['POST'])
@ ensure_csrf_cookie
@ratelimit(key='ip', rate='10/m', block=True)
def save_new(request):
    project = request.POST.get('project')
    payload = request.POST.get('payload')
    title = request.POST.get('title')
    description = request.POST.get('description')
    type = request.POST.get('type')
    background = request.POST.get('bg')
    preview = request.FILES.get('preview')
    id = helpers.validate_request(request)
    if id is not None and database.save_new_project(project, payload, id, title, description, type, background):
        if preview is not None:
            bucket.save(project, preview)
        redis_client.delete(f"boards:{id}")
        redis_client.delete(f"board:{project}")
        redis_client.delete(f"bg:{project}")
        redis_client.delete(f"last_access:{project}")
        return Response({'status': 200})
    return Response({'status': 400})


@api_view(['POST'])
@ensure_csrf_cookie
@ratelimit(key='ip', rate='30/m', block=True)
def check_saved(request):
    data = request.data
    project = data['project']
    owner = data['owner']
    return Response({'saved': database.check_saved(project, owner)})


@ api_view(['POST'])
@ ensure_csrf_cookie
@ratelimit(key='ip', rate='30/m', block=True)
def check_owner(request):
    data = request.data
    owner = data['owner']
    room = data['room']
    id = helpers.validate_request(request)
    if id == owner and database.check_ownership(database.decode_user(owner), room):
        return Response({'status': 200})
    return Response({'status': 400})


@ api_view(['POST'])
@ ensure_csrf_cookie
@ratelimit(key='ip', rate='30/m', block=True)
def check_bookmark(request, room):
    id = helpers.validate_request(request)
    if id is not None and database.check_bookmark(room, id):
        return Response({'status': 200, "bookmarked": True})
    return Response({'status': 403, 'bookmarked': False})


@ api_view(['POST'])
@ ensure_csrf_cookie
@ratelimit(key='ip', rate='30/m', block=True)
def bookmark(request, room):
    id = helpers.validate_request(request)
    if id is not None:
        data = request.data
        me = data['user']
        curr_bookmark = data['status']
        if database.modify_bookmark(me, curr_bookmark, room):
            redis_client.delete(f"bookmarks:{me}")
            if curr_bookmark:
                return Response({'status': 200, 'bookmarked': False})
            else:
                return Response({'status': 200, 'bookmarked': True})
        return Response({'status': 200, 'bookmarked': False})
    return Response({'status': 400})


@ api_view(['POST'])
@ ensure_csrf_cookie
@ratelimit(key='ip', rate='30/m', block=True)
def get_bookmarks(request, username):
    id = helpers.validate_request(request)
    if id is not None:
        data = request.data
        timezone = data['timezone']
        encoded = database.encode_user(username)
        if redis_client.get(f"bookmarks:{encoded}"):
            bookmarks = json.loads(redis_client.get(
                f"bookmarks:{encoded}"))
        else:
            bookmarks = database.get_bookmarks(username, timezone)
            redis_client.setex(
                f"bookmarks:{encoded}", 60*5, json.dumps(bookmarks))
        return Response({'status': 200, 'bookmarks': bookmarks})
    return Response({'status': 400, 'bookmarks': []})


@ api_view(['GET'])
@ ensure_csrf_cookie
@ratelimit(key='ip', rate='30/m', block=True)
def delete_bookmark(request, room):
    id = helpers.validate_request(request)
    if id is not None and database.delete_bookmark(id, room):
        if redis_client.get(f"bookmarks:{id}"):
            redis_client.delete(f"bookmarks:{id}")
        return Response({'status': 200})
    return Response({'status': 400})


@ api_view(['POST'])
@ ensure_csrf_cookie
@ratelimit(key='ip', rate='30/m', block=True)
def trending(request):
    id = helpers.validate_request(request)
    if id is not None:
        data = request.data
        timezone = data['timezone']
        if redis_client.get(f"trending:{id}:{timezone}"):
            boards = json.loads(redis_client.get(f"trending:{id}:{timezone}"))
        else:
            boards = database.get_trending(id, timezone)
            redis_client.setex(
                f"trending:{id}:{timezone}", 60*10, json.dumps(boards))
        return Response({'status': 200, 'boards': boards})
    return Response({'status': 400, 'boards': ''})


@ api_view(['POST'])
@ ensure_csrf_cookie
@ratelimit(key='ip', rate='30/m', block=True)
def search(request):
    id = helpers.validate_request(request)
    if id is not None:
        Metrics.search.inc()
        data = request.data
        query = data['query']
        timezone = data['timezone']
        if redis_client.get(f"search:{query}:{timezone}"):
            result = json.loads(redis_client.get(f"search:{query}:{timezone}"))
        else:
            result = database.get_matches(query, timezone)
            redis_client.setex(f"search:{query}:{
                               timezone}", 60*5, json.dumps(result))
        return Response({"status": 200, "boards": result})
    return Response({"status": 400})
