from django.test import TestCase
from django.urls import reverse
from .models import FoodItem, Order

class FoodOrderSystemTests(TestCase):

    def setUp(self):
        self.food_item = FoodItem.objects.create(
            name="Pizza",
            description="Delicious pizza with cheese and toppings",
            price=12.99
        )

    # FoodItem Tests
    def test_food_list_view(self):
        response = self.client.get(reverse('food_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pizza")
        self.assertTemplateUsed(response, 'food/food_list.html')

    def test_food_detail_view(self):
        response = self.client.get(reverse('food_detail', args=[self.food_item.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pizza")
        self.assertTemplateUsed(response, 'food/food_detail.html')

    def test_food_create_view(self):
        response = self.client.post(reverse('food_create'), {
            'name': 'Burger',
            'description': 'Juicy beef burger with lettuce and tomato',
            'price': '9.99'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(FoodItem.objects.last().name, 'Burger')

    def test_food_update_view(self):
        response = self.client.post(reverse('food_update', args=[self.food_item.pk]), {
            'name': 'Pizza Margherita',
            'description': 'Classic pizza with mozzarella and basil',
            'price': '11.99'
        })
        self.assertEqual(response.status_code, 302)
        self.food_item.refresh_from_db()
        self.assertEqual(self.food_item.name, 'Pizza Margherita')

    def test_food_delete_view(self):
        response = self.client.post(reverse('food_delete', args=[self.food_item.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(FoodItem.objects.count(), 0)

    # Order Tests
    def test_order_list_view(self):
        response = self.client.get(reverse('order_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'food/order_list.html')

    def test_order_detail_view(self):
        order = Order.objects.create(
            customer_name="John Doe",
            customer_email="john.doe@example.com",
            total_price=25.99
        )
        order.food_items.add(self.food_item)
        response = self.client.get(reverse('order_detail', args=[order.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "John Doe")
        self.assertTemplateUsed(response, 'food/order_detail.html')

    def test_order_create_view(self):
        response = self.client.post(reverse('order_create'), {
            'customer_name': 'Jane Smith',
            'customer_email': 'jane.smith@example.com',
            'food_items': [self.food_item.pk],
            'total_price': '12.99'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.last().customer_name, 'Jane Smith')

    def test_order_delete_view(self):
        order = Order.objects.create(
            customer_name="Jane Doe",
            customer_email="jane.doe@example.com",
            total_price=15.99
        )
        response = self.client.post(reverse('order_delete', args=[order.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.count(), 0)
