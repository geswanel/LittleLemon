from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views


urlpatterns = [
    path("", views.index, name="home"),
    path("api-token-auth", obtain_auth_token),
    path("items", views.MenuItemView.as_view(), name="menu_items"),
    path("items/<int:pk>", views.SingleMenuItemView.as_view(), name="menu_single_item"),
]
