import jwt, datetime
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from app import settings
from core.models import User,UserToken


class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        #is_ambassador = 'api/ambassador' in request.path

        token = request.COOKIES.get('jwt')
        print('authorization===',token)

        if not token:
            return None

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('unauthenticated')

        print('author===payload===',payload)

        # if (is_ambassador and payload['scope'] != 'ambassador') or (not is_ambassador and payload['scope'] != 'admin'):
        #     raise exceptions.AuthenticationFailed('Invalid Scope!')

        user = User.objects.get(pk=payload['user_id'])

        if user is None:
            raise exceptions.AuthenticationFailed('User not found!')

        if not UserToken.objects.filter(user_id=user.id,token=token,expired_at__gt=datetime.datetime.utcnow()).exists():
            print('asjdhkjashdkajshd====================================')
            raise exceptions.AuthenticationFailed('unauthenticated')
        print('author===payload===',payload)
        return (user, None)

    @staticmethod
    def generate_jwt(id, scope='1234'):
        payload = {
            'user_id': id,
            'scope': scope,
            'exp': datetime.datetime.now() + datetime.timedelta(days=1),
            'iat': datetime.datetime.now(),
        }

        return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
