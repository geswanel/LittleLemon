from rest_framework import serializers
from djoser.serializers import UserSerializer

from . import models

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = "__all__"


class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=models.Category.objects.all(), source="category", write_only=True)
    class Meta:
        model = models.MenuItem
        fields = ["id", "title", "price", "featured", "category", "category_id"]


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cart
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderItem
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    order_items = serializers.SerializerMethodField(method_name="get_items", read_only=True)
    class Meta:
        model = models.Order
        fields = "__all__"
    
    def get_items(self, order):
        order_items = models.OrderItem.objects.filter(order=order)
        serialized_items = OrderItemSerializer(order_items, many=True)

        return serialized_items.data
