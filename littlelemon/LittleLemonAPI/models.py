from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=255)


class MenuItem(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=1000)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT)


class CartItem(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)


class Order(models.Model):
    class Status(models.IntegerChoices):
        PROCESSING = 0
        DELIVERED = 1

    customer = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="orders")
    delivery_crew = models.ForeignKey(User, default=None, null=True,
                                      on_delete=models.DO_NOTHING,
                                      related_name="to_deliver")
    status = models.IntegerField(default=Status.PROCESSING, choices=Status)


class OrderItem(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.PROTECT)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField()

