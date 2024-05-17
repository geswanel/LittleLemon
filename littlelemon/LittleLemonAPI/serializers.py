from rest_framework import serializers
from django.contrib.auth.models import User

from . import models

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]

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
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    menu_item = MenuItemSerializer(read_only=True)
    menu_item_id = serializers.PrimaryKeyRelatedField(queryset=models.MenuItem.objects.all(), source="menu_item", write_only=True)

    class Meta:
        model = models.Cart
        fields = ["user", "menu_item", "menu_item_id", "quantity", "unit_price", "price"]
        extra_kwargs = {
            "unit_price": { "read_only": True },
            "price": { "read_only": True },
        }

    def create(self, validated_data):
        menu_item = validated_data.get("menu_item")

        validated_data["unit_price"] = menu_item.price
        validated_data["price"] = validated_data.get("unit_price") * validated_data.get("quantity")

        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        menu_item = instance.menu_item
        
        validated_data["unit_price"] = menu_item.price
        validated_data["price"] = validated_data.get("unit_price") * validated_data.get("quantity")
        return super().update(instance, validated_data)


class OrderItemSerializer(serializers.ModelSerializer):
    menu_item = MenuItemSerializer()
    class Meta:
        model = models.OrderItem
        fields = ["menu_item", "quantity", "unit_price", "price"]


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(source="orderitem_set", many=True)
    user = UserSerializer()
    class Meta:
        model = models.Order
        fields = "__all__"
