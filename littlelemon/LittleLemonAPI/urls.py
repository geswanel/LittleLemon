from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from . import views

app_name = "littlelemon"
urlpatterns = [
    path('secure', views.secure_view),
    path('', include('djoser.urls')),
    # path('', include('djoser.urls.authtoken')),
]