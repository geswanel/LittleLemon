from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import Group, User
from djoser.serializers import UserSerializer
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView


from .models import (
    MenuItem,
    CartItem,
    Order,
    OrderItem,
)
from .serializers import (
    MenuItemSerializer,
    CartItemSerializer,
    OrderSerializer,
)


# Create your views here.
@api_view()
@permission_classes([IsAuthenticated])
def secure_view(request):
    return Response({"message": "success"}, status=status.HTTP_200_OK)

# User Management
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def managers(request):
    if not request.user.groups.filter(name="Managers").exists():
        return Response({"detail": "Forbidden: not enough priviliges"}, status=status.HTTP_403_FORBIDDEN)
    
    managers_user_set = Group.objects.get(name="Managers").user_set
    
    if request.method == "GET":
        serialized_users = UserSerializer(managers_user_set.all(), many=True)

        return Response(serialized_users.data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        if "pk" not in request.data:
            return Response({"detail": "Bad Request: pk not presented"}, status=status.HTTP_400_BAD_REQUEST)
        pk = request.data.get("pk")
        user = get_object_or_404(User, pk=pk)
        managers_user_set.add(user)
        return Response({"detail": "User assigned to managers"}, status=status.HTTP_201_CREATED)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_manager(request, pk):
    if not request.user.groups.filter(name="Managers").exists():
        return Response({"detail": "Forbidden: not enough priviliges"}, status=status.HTTP_403_FORBIDDEN)

    manager_to_delete = get_object_or_404(User, pk=pk)
    Group.objects.get(name="Managers").user_set.remove(manager_to_delete)
    return Response({"detail": "Success"}, status=status.HTTP_200_OK)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def delivery_crew(request):
    if not request.user.groups.filter(name="Managers").exists():
        return Response({"detail": "Forbidden: not enough priviliges"}, status=status.HTTP_403_FORBIDDEN)
    
    delcrew_user_set = Group.objects.get(name="Delivery crew").user_set
    
    if request.method == "GET":
        serialized_users = UserSerializer(delcrew_user_set.all(), many=True)

        return Response(serialized_users.data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        if "pk" not in request.data:
            return Response({"detail": "Bad Request: pk not presented"}, status=status.HTTP_400_BAD_REQUEST)
        pk = request.data.get("pk")
        user = get_object_or_404(User, pk=pk)
        delcrew_user_set.add(user)
        return Response({"detail": "User assigned to delivery crew"}, status=status.HTTP_201_CREATED)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_delivery_crew(request, pk):
    if not request.user.groups.filter(name="Managers").exists():
        return Response({"detail": "Forbidden: not enough priviliges"}, status=status.HTTP_403_FORBIDDEN)

    decrew_to_delete = get_object_or_404(User, pk=pk)
    Group.objects.get(name="Delivery crew").user_set.remove(decrew_to_delete)
    return Response({"detail": "Success"}, status=status.HTTP_200_OK)

# Menu Items
class MenuItemsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        items = MenuItem.objects.all()
        serialized_items = MenuItemSerializer(items, many=True)
        return Response(serialized_items.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        if not request.user.groups.filter(name="Managers").exists():
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        
        serialized_item = MenuItemSerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response({"detail": "Created"}, status=status.HTTP_201_CREATED)


class SingleMenuItem(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        menu_item = get_object_or_404(MenuItem, pk=pk)
        serialized_item = MenuItemSerializer(menu_item)
        return Response(serialized_item.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        if not request.user.groups.filter(name="Managers").exists():
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        
        item = get_object_or_404(MenuItem, pk=pk)
        serialized_data = MenuItemSerializer(item, data=request.data)
        serialized_data.is_valid(raise_exception=True)
        serialized_data.save()
        return Response({"detail": "Menu item is changed"}, status=status.HTTP_200_OK)
    
    def patch(self, request, pk):
        if not request.user.groups.filter(name="Managers").exists():
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        
        item = get_object_or_404(MenuItem, pk=pk)
        serialized_data = MenuItemSerializer(item, data=request.data, partial=True)
        serialized_data.is_valid(raise_exception=True)
        serialized_data.save()
        return Response({"detail": "Menu item is changed"}, status=status.HTTP_200_OK)
    
    def delete(self, request, pk):
        if not request.user.groups.filter(name="Managers").exists():
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        
        menu_item = get_object_or_404(MenuItem, pk=pk)
        menu_item.delete()
        return Response({"detail": "Success deletion"}, status=status.HTTP_200_OK)


class CartView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        cart_items = CartItem.objects.filter(customer=request.user)

        serialized_items = CartItemSerializer(cart_items, many=True)
        return Response(serialized_items.data, status=status.HTTP_200_OK)

    def post(self, request):
        request.data["customer"] = request.user.pk
        serialized_data = CartItemSerializer(data=request.data)
        serialized_data.is_valid(raise_exception=True)
        serialized_data.save()

        return Response({"detail": "New item added"}, status=status.HTTP_201_CREATED)

    def delete(self, request):
        cart_items = CartItem.objects.filter(customer=request.user)
        cart_items.delete()

        return Response({"detail": "Success cart flush"}, status=status.HTTP_200_OK)


class OrderView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        if request.user.groups.filter(name="Managers").exists():
            orders = Order.objects.all()
        elif request.user.groups.filter(name="Managers").exists():
            orders = Order.objects.filter(delivery_crew=request.user)
        else:
            orders = Order.objects.filter(customer=request.user)
        
        serialized_orders = OrderSerializer(orders, many=True)
        return Response(serialized_orders.data, status=status.HTTP_200_OK)

    def post(self, request):
        order = Order(customer=request.user)
        order.save()
        cart_items = CartItem.objects.filter(customer=request.user)
        for item in cart_items:
            order_item = OrderItem(menu_item=item.menu_item, order=order, quantity=item.quantity)
            order_item.save()
        
        cart_items.delete()

        return Response({"detail": "Order created"}, status=status.HTTP_201_CREATED)
