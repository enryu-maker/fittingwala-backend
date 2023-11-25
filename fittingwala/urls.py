from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from fittingwala.controllers import MyObtainTokenPairView, RegisterFitUserView, VerifyFitUserView, \
    CategoryViewSet, SubCategoryViewSet, ProductViewSet, AllCombView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('category', CategoryViewSet, basename='category')
router.register('subcategory', SubCategoryViewSet, basename='subcategory')
router.register('product', ProductViewSet, basename='product')

urlpatterns = [
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterFitUserView.as_view(), name='register'),
    path('verify/', VerifyFitUserView.as_view(), name='verify'),
    path('get_all/', AllCombView.as_view(), name='get_all'),
    path('', include(router.urls)),
]
