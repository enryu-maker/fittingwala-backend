from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAuthenticated
from fittingwala.serializers import CategorySerializer, SubCategorySerializer, \
    ProductSerializer
from rest_framework.views import APIView
from fittingwala.view_models import FitUserViewModel, AllCombViewModel
from rest_framework.response import Response
from rest_framework import status
from fittingwala.models import FitUser, Category, SubCategory, Product
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Q
from rest_framework.exceptions import ValidationError
from rest_framework import viewsets


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        user = request.data.get('username')
        user = FitUser.objects.filter(Q(username=user) | Q(email=user)).first()
        if user is None:
            raise ValidationError('A user with this email/username and password is not found.')
        if not user.check_password(request.data.get('password')):
            raise ValidationError('A user with this email/username and password is not found.')
        if not user.is_active:
            raise ValidationError('This user has been deactivated.')
        return Response(status=status.HTTP_200_OK, data={
            'access': str(RefreshToken.for_user(user).access_token),
            'refresh': str(RefreshToken.for_user(user)),
            'user': {
                'username': user.username,
                'email': user.email,
                'mobile': user.mobile,
                'is_active': user.is_active
            }
        })


class RegisterFitUserView(APIView):
    permission_classes = (AllowAny,)
    view_model = FitUserViewModel

    def post(self, request):
        data = request.data
        view_object = self.view_model(
            table=FitUser,
            username=data.get('username'),
            email=data.get('email'),
            password=data.get('password'),
            mobile=data.get('mobile')
        )
        view_object.create_user()
        return Response(status=status.HTTP_201_CREATED, data={"message": "User created successfully, Please verify "
                                                                         "your email"})


class VerifyFitUserView(APIView):
    permission_classes = (AllowAny,)
    view_model = FitUserViewModel

    @staticmethod
    def post(request):
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


class AllCombView(APIView):
    permission_classes = (AllowAny,)
    view_model = AllCombViewModel

    def get(self, request):
        view_retrive = self.view_model()
        resp = view_retrive.run_query()
        return Response(
            status=status.HTTP_200_OK,
            data=resp
        )


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class SubCategoryViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = SubCategorySerializer
    queryset = SubCategory.objects.all()


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
