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
