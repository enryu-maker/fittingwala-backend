from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from fittingwala.controllers import MyObtainTokenPairView, RegisterFitUserView, VerifyFitUserView


urlpatterns = [
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterFitUserView.as_view(), name='register'),
    path('verify/', VerifyFitUserView.as_view(), name='verify'),
    path('admin/', admin.site.urls),
]
