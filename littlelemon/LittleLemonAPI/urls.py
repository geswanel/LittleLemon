from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from . import views

app_name = "littlelemon"
urlpatterns = [
    path("secure", views.secure_view),
    path("", include("djoser.urls")),
    path("groups/manager/users", views.managers, name="managers"),
    path("groups/manager/users/<int:pk>", views.delete_manager, name="delete_manager"),
    path("groups/delivery-crew/users", views.delivery_crew, name="delivery_crew"),
    path("groups/delivery-crew/users/<int:pk>", views.delete_delivery_crew, name="delete_delivery_crew"),
    # path('', include('djoser.urls.authtoken')),
]