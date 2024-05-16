from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter(trailing_slash=False)
router.register("categories", views.CategoryViewSet)

app_name = "littlelemon"
urlpatterns = [
    path("", include("djoser.urls")),
    path("", include("djoser.urls.authtoken")),
    path("groups/manager/users", views.managers, name="managers"),
    path("groups/manager/users/<int:pk>", views.delete_manager, name="delete_manager"),
    path("groups/delivery-crew/users", views.delivery_crew, name="delivery_crew"),
    path("groups/delivery-crew/users/<int:pk>", views.delete_delivery_crew, name="delete_delivery_crew"),
    path("menu-items", views.MenuItemsView.as_view(), name="menu_items"),
    path("menu-items/<int:pk>", views.SingleMenuItem.as_view(), name="single_menu_item"),
    path("cart/menu-items", views.CartView.as_view(), name="cart"),
    path("orders", views.OrderView.as_view(), name="order"),
    path("orders/<int:pk>", views.SingleOrderView.as_view(), name="single-order"),
    path("menu-items/", include(router.urls)),
    # path('', include('djoser.urls.authtoken')),
]
