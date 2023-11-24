from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from fittingwala.controllers import MyObtainTokenPairView


urlpatterns = [
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/', admin.site.urls),
]
