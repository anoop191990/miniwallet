from rest_framework.authentication import get_authorization_header, BaseAuthentication
from wallet.models import *
import jwt
from rest_framework.response import Response
from rest_framework import HTTP_HEADER_ENCODING, exceptions

class ClientTokenAuthentication(BaseAuthentication):
    model = None

    def get_model(self):
        return User

    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        print(auth)

        if not auth or auth[0].lower() != b'token':
            return None

        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:

            msg = 'Invalid token header'
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1]
            if token == "null":
                msg = 'Null token not allowed'
                raise exceptions.AuthenticationFailed(msg)
        except UnicodeError:
            msg = 'Invalid token header. Token string should not contain invalid characters.'
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, token):
        model = self.get_model()

        try:
            payload = jwt.decode(token, "SECRET")
            print(payload)
            email = payload['email']
            userid = payload['id']
            first_name = payload['first_name']
            print(email)

        except:
            raise exceptions.AuthenticationFailed('Token has invalid')

        msg = {'Error': "Token mismatch", 'status': "401"}
        try:

            user = User.objects.get(
                email=email,
            )

            if not user:
                raise exceptions.AuthenticationFailed(msg)

        except jwt.ExpiredSignature or jwt.DecodeError or jwt.InvalidTokenError:
            return Response({'Error': "Token is invalid"}, status="403")
        except User.DoesNotExist:
            return Response({'Error': "Internal server error"}, status="200")
        except Exception as e:
            return Response({'Error': "Token is invalid"}, status="403")

        return (user, token)

    def authenticate_header(self, request):
        return 'Token'
