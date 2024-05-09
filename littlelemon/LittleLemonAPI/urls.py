from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

app_name = "littlelemon"
urlpatterns = [
    path('secure', views.secure_view),
]