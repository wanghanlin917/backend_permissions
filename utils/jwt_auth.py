import jwt
import datetime
from jwt import exceptions
from django.conf import settings


def create_token(payload, timeout=10):
    headers = {
        'type': 'jwt',
        'alg': 'HS256'
    }
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(hours=timeout)
    result = jwt.encode(payload=payload, key=settings.SECRET_KEY.encode('utf-8'), algorithm="HS256", headers=headers)
    return result


def parse_payload(token):
    try:
        verified_payload = jwt.decode(token, settings.SECRET_KEY.encode('utf-8'), algorithms=["HS256"])
        return True, verified_payload
    except exceptions.ExpiredSignatureError:
        error = 'token已失效'
    except jwt.DecodeError:
        error = 'token认证失败'
    except jwt.InvalidTokenError:
        error = '非法的token'
    return False, error
