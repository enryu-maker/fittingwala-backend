from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from fittingwala.models import FitUser


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        token['username'] = user.username
        return token
