from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['email'] = user.email
        token['firstname'] = user.first_name
        token['lastname'] = user.last_name
        token['super_user'] = user.is_superuser
        token['staff'] = user.is_staff

        return token