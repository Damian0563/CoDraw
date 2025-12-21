import random
import re

def generate_code()->str:
    code=""
    for i in range(5):
        code+=str(random.randint(0,9))
    return code

def validate_request(request)->str:
    try:
        id=request.session['user_id']
    except KeyError:
        id=request.COOKIES.get('token')
    return id

def valid_email(email: str) -> bool:
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None