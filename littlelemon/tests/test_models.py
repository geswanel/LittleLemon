from django.test import TestCase
from restaurant.models import Menu

class MenuTest(TestCase):
    def test_instance(self):
        item = Menu.objects.create(title="Pizza Margherita", price=10.00, inventory=10)

        self.assertEqual(str(item), "Pizza Margherita : 10.0")
