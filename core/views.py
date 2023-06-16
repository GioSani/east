from rest_framework import exceptions
from rest_framework.permissions import IsAuthenticated,DjangoModelPermissions,AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from core.models import User,UserToken
from .authentication import JWTAuthentication
from .serializers import UserSerializer
import datetime
from rest_framework import status
from .mixins import GroupRequiredMixin


from rest_framework.generics import GenericAPIView
from .serializers import*



from rest_framework.decorators import permission_classes



class RegisterAPIView(APIView):
    def post(self, request):
        data = request.data

        if data['password'] != data['password_confirm']:
            raise exceptions.APIException('Passwords do not match!')

        serializer = UserSerializer(data=data)
        
        serializer.is_valid(raise_exception=True)
      
        serializer.save()
       
        return Response(serializer.data)


class LoginAPIView(APIView):
    def post(self, request):

        email = request.data['email']
        password = request.data['password']
        #scope = request.data['scope']
        user = User.objects.filter(email=email).first()
        
        if user is None:
            raise exceptions.AuthenticationFailed('User not found!')
        
        if not user.check_password(password):
            raise exceptions.AuthenticationFailed('Incorrect Password!')

        # if user.is_ambassador and scope == 'admin':
        #     raise exceptions.AuthenticationFailed('Unauthorized')
        
        token = JWTAuthentication.generate_jwt(user.id)

        UserToken.objects.create(
            user_id=user.id,
            token=token,
            created_at = datetime.datetime.now(),
            expired_at=datetime.datetime.now() + datetime.timedelta(days=1)
        )
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data={
            'jwt':token
        }
        return response
        # print('token====',token)
        # response = Response()
        # response.set_cookie(key='jwt', value=token, httponly=True)
        # response.data = {
        #     'message': 'success'
        # }

        # return response

        # return Response(
        #     {'jwt': token}
        # )

import json
class UserAPIView(GroupRequiredMixin,APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    group_required = ['management']

    def get(self, request):
        
        data = UserSerializer(request.user).data
        print("=================users==========================",request.user)
        
        return Response(data=data)

    
class UsersListAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()


class LogoutAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print('====-====',request.user,UserToken.objects.filter(user_id=request.user.id))
        UserToken.objects.filter(user_id=request.user.id).delete()

        response = Response()

        response.delete_cookie(key='jwt')
        
        response.data = {
            'message': 'success'
        }
        return response


class ProfileInfoAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, pk=None):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ProfilePasswordAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, pk=None):
        user = request.user
        data = request.data

        if data['password'] != data['password_confirm']:
            raise exceptions.APIException('Passwords do not match!')

        user.set_password(data['password'])
        user.save()
        return Response(UserSerializer(user).data)

class UserDeleteAPIView(APIView):
    """
    Delete a User.
    """
    def delete(self, request, pk):
        print('delete== pk==',pk)
        try:
            user = User.objects.get(pk=pk)
            print('delete===',user)
        except User.DoesNotExist:
            return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        user.delete()
        return Response({"message": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)







##############################################################################################33
###################################################################################################3





@permission_classes((AllowAny, ))
class GoogleSocialAuthView(GenericAPIView):

    serializer_class = GoogleSocialAuthSerializer

    def post(self, request):
        """
        POST with "auth_token"
        Send an idtoken as from google to get user information
        """
        print('gmail request=======111==============')
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        print('=====================')
        data = ((serializer.validated_data)['auth_token'])
        print('=====================',data)

        response = Response()
        response.set_cookie(key='jwt', value=data.get('jwt'), httponly=True)
        response.data={
            'jwt':data.get('jwt')
        }
        response.status=status.HTTP_200_OK
        return response
        r#eturn Response(data, status=status.HTTP_200_OK)

