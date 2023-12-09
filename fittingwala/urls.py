from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from fittingwala.controllers import MyObtainTokenPairView, RegisterFitUserView, VerifyFitUserView, \
    CategoryViewSet, SubCategoryViewSet, ProductViewSet, AllCombView
from rest_framework.routers import DefaultRouter
from fittingwala.models import FitUser, Category, SubCategory, Product

admin.autodiscover()
# title
admin.site.site_header = 'Fitting Wala'
admin.site.register(FitUser)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product)


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
    path('admin/', admin.site.urls),
]
