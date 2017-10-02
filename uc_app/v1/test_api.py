from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from v1.models import User, Item
from django.core import serializers
from django.http import JsonResponse
from django.forms import model_to_dict

class CreateUserTest(TestCase):
    def setUp(self):
        self.c = Client()

    def test_user_insufficient_fields(self):
        response = self.c.post(reverse('create-user'), {"first_name":"John", "last_name":"Smith"})
        self.assertEquals(response.status_code, 500)

    def test_user_get_not_post(self):
        response = self.c.get(reverse('create-user'), {"first_name":"John", "last_name":"Smith", "username":"jsmith", "password":"h$4"})
        self.assertEquals(response.status_code, 500)

    def test_user_valid(self):
        response = self.c.post(reverse('create-user'), {"first_name":"John", "last_name":"Smith", "username":"jsmith", "password":"h$4"})
        self.assertEqual(response.status_code, 200)

class GetUserTest(TestCase):
    def setUp(self):
        self.c = Client()
        usr = User.objects.create(first_name="John", last_name="Smith", username="jsmith", password="h$4")
        self.id = usr.pk

    def test_user_not_found(self):
        response = self.c.get(reverse('get-user', kwargs={'user_id':(self.id+1)}))
        self.assertEquals(response.status_code, 500)

    def test_get_user_post(self):
        response = self.c.post(reverse('get-user', kwargs={'user_id':(self.id)}))
        self.assertEquals(response.status_code, 500)

    def test_get_user_valid(self):
        response = self.c.get(reverse('get-user', kwargs={'user_id':(self.id)}))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, JsonResponse(model_to_dict(User.objects.get(pk=self.id))).content)

class CreateItemTest(TestCase):
    def setUp(self):
        self.c = Client()
        usr = User.objects.create(first_name="John", last_name="Smith", username="jsmith", password="h$4")
        self.id = usr.pk

    def test_item_insufficient_fields(self):
        response = self.c.post(reverse('create-item'), {"item_name":"shirt", "item_price":7.7})
        self.assertEquals(response.status_code, 500)

    def test_item_get_not_post(self):
        response = self.c.get(reverse('create-item'), {"item_name":"shirt", "item_price":20.0, "seller":self.id, "brand":"generic", "description":"blue", "image_url":"http://assets.academy.com/mgen/54/10779854.jpg", "item_size":"L", "item_type":"Top"})
        self.assertEquals(response.status_code, 500)

    def test_item_valid(self):
        response = self.c.post(reverse('create-item'), {"item_name":"shirt", "item_price":20.0, "seller":self.id, "brand":"generic", "description":"blue", "image_url":"http://assets.academy.com/mgen/54/10779854.jpg", "item_size":"L", "item_type":"Top"})
        self.assertEqual(response.status_code, 200)

class GetUserTest(TestCase):
    def setUp(self):
        self.c = Client()
        usr = User.objects.create(first_name="John", last_name="Smith", username="jsmith", password="h$4")
        itm = Item.objects.create(item_name="shirt", item_price=20.0, seller=usr, brand="generic", description="blue", image_url="http://assets.academy.com/mgen/54/10779854.jpg", item_size="L", item_type="Top")
        self.id = itm.pk

    def test_user_not_found(self):
        response = self.c.get(reverse('get-item', kwargs={'item_id':(self.id+1)}))
        self.assertEquals(response.status_code, 500)

    def test_get_user_post(self):
        response = self.c.post(reverse('get-item', kwargs={'item_id':(self.id)}))
        self.assertEquals(response.status_code, 500)

    def test_get_user_valid(self):
        response = self.c.get(reverse('get-item', kwargs={'item_id':(self.id)}))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, JsonResponse(model_to_dict(Item.objects.get(pk=self.id))).content)


# Create your tests here.
