from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from cars.api_views import CarViewSet, CommentViewSet


router = routers.DefaultRouter()
router.register(r'cars', CarViewSet, basename='car')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cars.urls')),
    path('api/', include(router.urls)),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]
