from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAuthenticated
from fittingwala.serializers import MyTokenObtainPairSerializer
from rest_framework.views import APIView
from fittingwala.view_models import FitUserViewModel
from rest_framework.response import Response
from rest_framework import status
from fittingwala.models import FitUser

class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class RegisterFitUserView(APIView):
    permission_classes = (AllowAny,)
    view_model = FitUserViewModel

    def post(self, request):
        data = request.data
        view_object = self.view_model(**data)
        user = view_object.create_user()
        return Response(status=status.HTTP_201_CREATED, data={"message": "User created successfully, Please verify "
                                                                         "your email"})


class VerifyFitUserView(APIView):
    permission_classes = (AllowAny,)
    view_model = FitUserViewModel

    @staticmethod
    def post(self, request):
        code = request.data.get('code')
        user = request.data.get('email')

        if not code:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "Verification code is required"})
        if not user:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "User is required"})
        if user := FitUser.objects.filter(email=user).first():
            if user.verification_code != code:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "Invalid verification code"})
            user.is_active = True
            user.save()

        return Response(status=status.HTTP_201_CREATED, data={"message": "User verified successfully"})

