
from rest_framework import exceptions
import jwt, datetime

def create_access_token(username):
    return jwt.encode({
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow()
    },'access_secret',algorithm='HS256')

def decode_access_token(token):
    try:
        payload = jwt.decode(token,'access_secret',algorithms='HS256')
        return payload['username']
    except:
        return 401
        # raise exceptions.AuthenticationFailed('unauthenticated')


