from django.test import TestCase
from django.urls import reverse

from restaurant.models import Menu
from restaurant.serializers import MenuSerializer


class MenuViewTest(TestCase):
    def setUp(self):
        Menu.objects.create(title="Tomato Soup", price=6.99, inventory=10)
        Menu.objects.create(title="Georgian Salad", price=7.99, inventory=5)
        Menu.objects.create(title="Pad Thai", price=12.99, inventory=7)
    
    def test_getall(self):
        response = self.client.get(reverse('menu_items'))
        menu_data = Menu.objects.all()
        serialized_data = MenuSerializer(menu_data, many=True)
        # print(response.data)
        # print(serialized_data.data)
        self.assertEqual(response.data, serialized_data.data)
