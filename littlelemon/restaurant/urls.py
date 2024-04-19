from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("menu/items", views.MenuItemView.as_view(), name="menu_items"),
    path("menu/items/<int:pk>", views.SingleMenuItemView.as_view(), name="menu_single_item"),
]
