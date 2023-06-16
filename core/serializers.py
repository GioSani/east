from rest_framework import serializers
from django.contrib.auth.models import Group

from .authentication import JWTAuthentication
from django.conf import settings
from rest_framework import serializers
from .google import Google
from .register import register_social_user
from rest_framework.exceptions import AuthenticationFailed
import datetime
from core.models import User,UserToken

{
"first_name": "gio",
"last_name": "sani",
"email": "g@g.com",
"password": "123",
"password_confirm": "123"

}

class RelatedModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')


class UserSerializer(serializers.ModelSerializer):

    #groups = RelatedModelSerializer(many=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'is_ambassador']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance




class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()
    # user_id = serializers.CharField()
    # email = serializers.CharField()
    # name = serializers.CharField()
    # provider = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = Google.validate(auth_token)
        #print('serialize validated authtoken data======',user_data)
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )
        
        if user_data['aud'] != settings.GOOGLE_CLIENT_ID:

            raise AuthenticationFailed('oops, who are you?')

        user_id = user_data['sub']
        email = user_data['email']
        name = user_data['name']
        provider = 'google'

        filtered_user_by_email = User.objects.filter(email=email)

        if filtered_user_by_email.exists():

            token = JWTAuthentication.generate_jwt(filtered_user_by_email[0].id)

            UserToken.objects.create(
            user_id=filtered_user_by_email[0].id,
            token=token,
            created_at = datetime.datetime.now(),
            expired_at=datetime.datetime.now() + datetime.timedelta(days=1)
        )


        return {
                
                'jwt': token,
                
                }

        # return register_social_user(
        #     provider=provider, user_id=user_id, email=email, name=name)

    
