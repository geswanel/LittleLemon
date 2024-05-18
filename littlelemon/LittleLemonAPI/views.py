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
from datetime import date
from django.db.models import Q


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

def is_staff(user):
    return user.groups.filter(Q(name="Managers") | Q(name="Delivery crew")).exists()

def is_manager(user):
    return user.groups.filter(name="Managers").exists()

def is_delivery(user):
    return user.groups.filter(name="Delivery crew").exists()


# Create your views here.
# User Management
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def managers(request):
    if not is_manager(request.user):
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
    if not is_manager(request.user):
        return Response({"detail": "Forbidden: not enough priviliges."}, status=status.HTTP_403_FORBIDDEN)

    manager_to_delete = get_object_or_404(User, pk=pk)
    Group.objects.get(name="Managers").user_set.remove(manager_to_delete)
    return Response({"detail": "Success manager deletion."}, status=status.HTTP_200_OK)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def delivery_crew(request):
    if not is_manager(request.user):
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
    if not is_manager(request.user):
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
        if not is_manager(request.user):
            return Response({"detail": "Forbidden to create categories."}, status=status.HTTP_403_FORBIDDEN)

        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if not is_manager(request.user):
            return Response({"detail": "Forbidden to update categories."}, status=status.HTTP_403_FORBIDDEN)

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not is_manager(request.user):
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
        if not is_manager(request.user):
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
        if not is_manager(request.user):
            return Response({"detail": "Forbidden to update the menu item."}, status=status.HTTP_403_FORBIDDEN)
        
        item = get_object_or_404(MenuItem, pk=pk)
        serialized_data = MenuItemSerializer(item, data=request.data)
        serialized_data.is_valid(raise_exception=True)
        serialized_data.save()
        return Response({"detail": "The menu item is changed."}, status=status.HTTP_200_OK)
    
    def patch(self, request, pk):
        if not is_manager(request.user):
            return Response({"detail": "Forbidden to update the menu item."}, status=status.HTTP_403_FORBIDDEN)
        
        item = get_object_or_404(MenuItem, pk=pk)
        serialized_data = MenuItemSerializer(item, data=request.data, partial=True)
        serialized_data.is_valid(raise_exception=True)
        serialized_data.save()
        return Response({"detail": "The menu item is changed."}, status=status.HTTP_200_OK)
    
    def delete(self, request, pk):
        if not is_manager(request.user):
            return Response({"detail": "Forbidden to delete the menu item."}, status=status.HTTP_403_FORBIDDEN)
        
        menu_item = get_object_or_404(MenuItem, pk=pk)
        menu_item.delete()
        return Response({"detail": "Success deletion of the menu item."}, status=status.HTTP_200_OK)


class CartView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        if is_staff(request.user):
            return Response({"detail": "Forbidden for the staff."}, status=status.HTTP_403_FORBIDDEN)
        
        cart_items = Cart.objects.filter(user=request.user)
        serialized_items = CartSerializer(cart_items, many=True)
        return Response(serialized_items.data, status=status.HTTP_200_OK)

    def post(self, request):
        if is_staff(request.user):
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
        if is_staff(request.user):
            return Response({"detail": "Forbidden for the staff."}, status=status.HTTP_403_FORBIDDEN)
        
        cart_items = Cart.objects.filter(user=request.user)
        cart_items.delete()
        return Response({"detail": "Cart is successfully flushed."}, status=status.HTTP_200_OK)


class OrderView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        if is_manager(request.user):
            orders = Order.objects.all()
        elif is_delivery(request.user):
            orders = Order.objects.filter(delivery_crew=request.user)
        else:
            orders = Order.objects.filter(user=request.user)
        
        serialized_orders = OrderSerializer(orders, many=True)
        return Response(serialized_orders.data, status=status.HTTP_200_OK)

    def post(self, request):
        if is_staff(request.user):
            return Response({"detail": "Forbidden for the staff."}, status=status.HTTP_403_FORBIDDEN)

        cart_items = Cart.objects.filter(user=request.user)
        if cart_items.count() == 0:
            return Response({"detail": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        order = Order(user=request.user, date=date.today())
        order.total = 0
        order_items = []
        for ci in cart_items:
            oi = OrderItem(
                order=order,
                menu_item=ci.menu_item,
                quantity=ci.quantity,
                unit_price=ci.unit_price,
                price=ci.price,
            )
            order.total += oi.price
            order_items.append(oi)
        
        order.save()
        for oi in order_items:
            oi.save()

        cart_items.delete()
        return Response({"detail": "Order created"}, status=status.HTTP_201_CREATED)


class SingleOrderView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        if not (is_manager(request.user) or \
                is_delivery(request.user) and order.delivery_crew == request.user or \
                    not is_staff(request.user) and order.user == request.user):
            return Response({"detail": "The order is assigned to other user."}, status=status.HTTP_403_FORBIDDEN)
        
        serialized_order = OrderSerializer(order)
        return Response(serialized_order.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        if not is_manager(request.user):
            return Response({"detail": "Not enough priviliges"}, status=status.HTTP_403_FORBIDDEN)
        
        order = get_object_or_404(Order, pk=pk)
        ser_order = OrderSerializer(order, data=request.data)
        ser_order.is_valid(raise_exception=True)
        ser_order.save()

        return Response(ser_order.data, status=status.HTTP_200_OK)
    
    def patch(self, request, pk):
        if not is_staff(request.user):
            return Response({"detail": "Not enough priviliges"}, status=status.HTTP_403_FORBIDDEN)

        order = get_object_or_404(Order, pk=pk)
        if is_delivery(request.user) and "delivery_crew_id" in request.data:
            return Response({"detail": "Not enough priviliges - cannot assign delivery crew for the order"}, status=status.HTTP_403_FORBIDDEN)

        ser_order = OrderSerializer(order, data=request.data, partial=True)
        ser_order.is_valid(raise_exception=True)
        ser_order.save()

        return Response(ser_order.data, status=status.HTTP_200_OK)

    def delete(serf, request, pk):
        if not is_manager(request.user):
            return Response({"detail": "Not enough priviliges"}, status=status.HTTP_403_FORBIDDEN)

        order = get_object_or_404(Order, pk=pk)
        order.delete()
        return Response({"detail": "Order is deleted successfuly"}, status=status.HTTP_200_OK)
