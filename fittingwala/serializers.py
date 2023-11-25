from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from fittingwala.models import FitUser
from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        authenticate_kwargs = {
            'username': attrs['username'],
            'password': attrs['password'],
        }
        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass

        user = FitUser.objects.filter(Q(username=attrs['username']) | Q(email=attrs['username'])).first()
        if user is None:
            raise serializers.ValidationError('A user with this email/username and password is not found.')
        # if not compare_digest(user.password, (attrs['password'])):
        #     raise serializers.ValidationError('A user with this email/username and password is not found.')
        if not user.is_active:
            raise serializers.ValidationError('This user has been deactivated.')

        return {
            'username': user.username,
            'password': user.password
        }

    @classmethod
    def get_token(cls, user):
        token = RefreshToken.for_user(user)
        return token
