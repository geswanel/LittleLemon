from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import Group, User
from djoser.serializers import UserSerializer
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet


from .models import (
    Category,
    MenuItem,
    Cart,
    Order,
    OrderItem,
)
from .serializers import (
    CategorySerializer,
    MenuItemSerializer,
    CartSerializer,
    OrderSerializer,
    OrderItemSerializer,
)


# Create your views here.
# User Management
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def managers(request):
    if not request.user.groups.filter(name="Managers").exists():
        return Response({"detail": "Forbidden: not enough priviliges."}, status=status.HTTP_403_FORBIDDEN)
    
    managers_user_set = Group.objects.get(name="Managers").user_set
    
    if request.method == "GET":
        serialized_users = UserSerializer(managers_user_set.all(), many=True)

        return Response(serialized_users.data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        if "id" not in request.data:
            return Response({"detail": "Bad Request: id not presented."}, status=status.HTTP_400_BAD_REQUEST)
        pk = request.data.get("id")
        user = get_object_or_404(User, pk=pk)
        managers_user_set.add(user)
        return Response({"detail": "User assigned to managers."}, status=status.HTTP_201_CREATED)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_manager(request, pk):
    if not request.user.groups.filter(name="Managers").exists():
        return Response({"detail": "Forbidden: not enough priviliges."}, status=status.HTTP_403_FORBIDDEN)

    manager_to_delete = get_object_or_404(User, pk=pk)
    Group.objects.get(name="Managers").user_set.remove(manager_to_delete)
    return Response({"detail": "Success manager deletion."}, status=status.HTTP_200_OK)


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
        if "id" not in request.data:
            return Response({"detail": "Bad Request: id not presented."}, status=status.HTTP_400_BAD_REQUEST)
        pk = request.data.get("id")
        user = get_object_or_404(User, pk=pk)
        delcrew_user_set.add(user)
        return Response({"detail": "User assigned to delivery crew."}, status=status.HTTP_201_CREATED)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_delivery_crew(request, pk):
    if not request.user.groups.filter(name="Managers").exists():
        return Response({"detail": "Forbidden: not enough priviliges."}, status=status.HTTP_403_FORBIDDEN)

    decrew_to_delete = get_object_or_404(User, pk=pk)
    Group.objects.get(name="Delivery crew").user_set.remove(decrew_to_delete)
    return Response({"detail": "Success delivery crew member deletion."}, status=status.HTTP_200_OK)


# Category model viewset - not required for the project - as helper for me
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        if not request.user.groups.filter(name="Managers").exists():
            return Response({"detail": "Forbidden to create categories."}, status=status.HTTP_403_FORBIDDEN)

        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if not request.user.groups.filter(name="Managers").exists():
            return Response({"detail": "Forbidden to update categories."}, status=status.HTTP_403_FORBIDDEN)

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not request.user.groups.filter(name="Managers").exists():
            return Response({"detail": "Forbidden to delete categories."}, status=status.HTTP_403_FORBIDDEN)

        return super().destroy(request, *args, **kwargs)

# Menu Items
class MenuItemsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        items = MenuItem.objects.all()
        serialized_items = MenuItemSerializer(items, many=True)
        return Response(serialized_items.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        if not request.user.groups.filter(name="Managers").exists():
            return Response({"detail": "Forbidden to create a menu item."}, status=status.HTTP_403_FORBIDDEN)
        
        serialized_item = MenuItemSerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response({"detail": "New item created."}, status=status.HTTP_201_CREATED)


class SingleMenuItem(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        menu_item = get_object_or_404(MenuItem, pk=pk)
        serialized_item = MenuItemSerializer(menu_item)
        return Response(serialized_item.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        if not request.user.groups.filter(name="Managers").exists():
            return Response({"detail": "Forbidden to update the menu item."}, status=status.HTTP_403_FORBIDDEN)
        
        item = get_object_or_404(MenuItem, pk=pk)
        serialized_data = MenuItemSerializer(item, data=request.data)
        serialized_data.is_valid(raise_exception=True)
        serialized_data.save()
        return Response({"detail": "The menu item is changed."}, status=status.HTTP_200_OK)
    
    def patch(self, request, pk):
        if not request.user.groups.filter(name="Managers").exists():
            return Response({"detail": "Forbidden to update the menu item."}, status=status.HTTP_403_FORBIDDEN)
        
        item = get_object_or_404(MenuItem, pk=pk)
        serialized_data = MenuItemSerializer(item, data=request.data, partial=True)
        serialized_data.is_valid(raise_exception=True)
        serialized_data.save()
        return Response({"detail": "The menu item is changed."}, status=status.HTTP_200_OK)
    
    def delete(self, request, pk):
        if not request.user.groups.filter(name="Managers").exists():
            return Response({"detail": "Forbidden to delete the menu item."}, status=status.HTTP_403_FORBIDDEN)
        
        menu_item = get_object_or_404(MenuItem, pk=pk)
        menu_item.delete()
        return Response({"detail": "Success deletion of the menu item."}, status=status.HTTP_200_OK)


class CartView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        if request.user.groups.all().exists():
            return Response({"detail": "Forbidden for the staff."}, status=status.HTTP_403_FORBIDDEN)
        
        cart_items = Cart.objects.filter(user=request.user)
        serialized_items = CartSerializer(cart_items, many=True)
        return Response(serialized_items.data, status=status.HTTP_200_OK)

    def post(self, request):
        if request.user.groups.all().exists():
            return Response({"detail": "Forbidden for the staff."}, status=status.HTTP_403_FORBIDDEN)
        
        user = request.user
        try:
            menu_item = MenuItem.objects.get(pk=request.data.get("menu_item_id"))
        except MenuItem.DoesNotExist:
            return Response({
                "menu_item_id": [
                    f"Invalid pk \"{request.data.get('menu_item_id')}\" - object does not exist."
                    ]
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            cart_item = Cart.objects.get(user=user, menu_item=menu_item)
            serialized_data = CartSerializer(cart_item, data=request.data, context={"request": request})
        except Cart.DoesNotExist:
            serialized_data = CartSerializer(data=request.data, context={"request": request})

        serialized_data.is_valid(raise_exception=True)
        serialized_data.save()
        return Response({"detail": "Cart item added."}, status=status.HTTP_201_CREATED)

    def delete(self, request):
        if request.user.groups.all().exists():
            return Response({"detail": "Forbidden for the staff."}, status=status.HTTP_403_FORBIDDEN)
        
        cart_items = Cart.objects.filter(user=request.user)
        cart_items.delete()
        return Response({"detail": "Cart is successfully flushed."}, status=status.HTTP_200_OK)


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
        cart_items = Cart.objects.filter(customer=request.user)
        for item in cart_items:
            order_item = OrderItem(menu_item=item.menu_item, order=order, quantity=item.quantity)
            order_item.save()
        
        cart_items.delete()

        return Response({"detail": "Order created"}, status=status.HTTP_201_CREATED)


class SingleOrderView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        if order.customer != request.user:
            return Response({"detail": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        
        order_items = OrderItem.objects.filter(order=order)
        ser_order_items = OrderItemSerializer(order_items, many=True)
        return Response(ser_order_items.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        if request.user.groups.filter(name="Manager").exists():
            order = get_object_or_404(Order, pk=pk)
            ser_order = OrderSerializer(order, data=request.data, partial=True)
            ser_order.is_valid(raise_exception=True)
            ser_order.save()

            return Response(ser_order.data, status=status.HTTP_200_OK)
    
    def patch(self, request, pk):
        if request.user.groups.all().exists():
            order = get_object_or_404(Order, pk=pk)
            ser_order = OrderSerializer(order, data=request.data, partial=True)
            ser_order.is_valid(raise_exception=True)
            ser_order.save()

            return Response(ser_order.data, status=status.HTTP_200_OK)
