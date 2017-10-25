from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from .models import User, Item, Authenticator
from django.core import serializers
from django.http import JsonResponse
from django.forms import model_to_dict
from django.core.exceptions import *
from .forms import UserForm, ItemForm
import json

#unit tests for api methods

class CreateUserTest(TestCase):
    def setUp(self):
        self.c = Client()

    def test_user_insufficient_fields(self):
        response = self.c.post(reverse('create-user'), {"first_name":"John", "last_name":"Smith"})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, JsonResponse({'errors':UserForm({"first_name":"John", "last_name":"Smith"}).errors}).content)

    def test_user_get_not_post(self):
        #Sends a get method instead of a post method
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

    def test_get_user_post_not_get(self):
        response = self.c.post(reverse('get-user', kwargs={'user_id':(self.id)}))
        self.assertEquals(response.status_code, 500)

    def test_get_user_valid(self):
        response = self.c.get(reverse('get-user', kwargs={'user_id':(self.id)}))
        self.assertEquals(response.status_code, 200)
        #Replicates the JSON Response format as the easiest way to verify output validity.
        self.assertEquals(response.content, JsonResponse(model_to_dict(User.objects.get(pk=self.id))).content)

class EditUserTest(TestCase):
    def setUp(self):
        self.c = Client()
        usr = User.objects.create(first_name="John", last_name="Smith", username="jsmith", password="h$4")
        self.id = usr.pk
        self.invalid_data = {"first_name":"John", "last_name":"Smithfo;ghaiehldjoiahrlknfpihaorfavahioejlnfahiojenlfasdiv;ho", "username":"jsmith1", "password":"h$4"}

    def test_edit_user_not_found(self):
        response = self.c.post(reverse('edit-user', kwargs={'user_id':(self.id+1)}), {"first_name":"John", "last_name":"Smith", "username":"jsmith1", "password":"h$4"})
        self.assertEquals(response.status_code, 500)

    def test_edit_user_get_not_post(self):
        response = self.c.get(reverse('edit-user', kwargs={'user_id':(self.id)}), {"first_name":"John", "last_name":"Smith", "username":"jsmith1", "password":"h$4"})
        self.assertEquals(response.status_code, 500)

    def test_edit_user_invalid_change(self):
        response = self.c.post(reverse('edit-user', kwargs={'user_id':(self.id)}), self.invalid_data)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, JsonResponse({'errors':UserForm(self.invalid_data).errors}).content)

    def test_edit_user_valid(self):
        response = self.c.post(reverse('edit-user', kwargs={'user_id':(self.id)}), {"first_name":"John", "last_name":"Smith", "username":"jsmith1", "password":"h$4"})
        self.assertEquals(response.status_code, 200)
        #Double-checks that the ID's match and the field was changed accordingly.
        self.assertEquals(response.content, JsonResponse({'userID':self.id}).content)
        self.assertEquals(User.objects.get(pk=self.id).username, "jsmith1")

class DeleteUserTest(TestCase):
    def setUp(self):
        self.c = Client()
        usr1 = User.objects.create(first_name="John", last_name="Smith", username="jsmith", password="h$4")
        usr2 = User.objects.create(first_name="John", last_name="Rolf", username="jrolf", password="dxdd")
        itm1 = Item.objects.create(item_name="shirt", item_price=20.0, seller=usr1, brand="generic", description="blue", image_url="http://assets.academy.com/mgen/54/10779854.jpg", item_size="L", item_type="Top")
        itm2 = Item.objects.create(item_name="shirt", item_price=20.0, seller=usr2, brand="generic", description="blue", image_url="http://assets.academy.com/mgen/54/10779854.jpg", item_size="L", item_type="Top")
        itm2.buyer = usr1
        self.id = usr1.pk
        self.item_id = itm1.pk
        self.item2_id = itm2.pk
        self.usr2_id = usr2.pk

    def test_del_user_not_found(self):
        response = self.c.post(reverse('delete-user', kwargs={'user_id':(self.id+7)}))
        self.assertEquals(response.status_code, 500)

    def test_del_user_success(self):
        response = self.c.post(reverse('delete-user', kwargs={'user_id':self.id}))
        self.assertEquals(response.status_code, 200)
        #Checks to make sure the user and the objects they were selling were deleted
        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(pk=self.id)
        with self.assertRaises(ObjectDoesNotExist):
            Item.objects.get(pk=self.item_id)
        #Checks that it removes user from seller field on other objects
        self.assertEquals(Item.objects.get(pk=self.item2_id).buyer, None)

class CreateItemTest(TestCase):
    def setUp(self):
        self.c = Client()
        usr = User.objects.create(first_name="John", last_name="Smith", username="jsmith", password="h$4")
        self.id = usr.pk

    def test_item_insufficient_fields(self):
        response = self.c.post(reverse('create-item'), {"item_name":"shirt", "item_price":7.7})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, JsonResponse({'errors':ItemForm({"item_name":"shirt", "item_price":7.7}).errors}).content)

    def test_item_get_not_post(self):
        response = self.c.get(reverse('create-item'), {"item_name":"shirt", "item_price":20.0, "seller":self.id, "brand":"generic", "description":"blue", "image_url":"http://assets.academy.com/mgen/54/10779854.jpg", "item_size":"L", "item_type":"Top"})
        self.assertEquals(response.status_code, 500)

    def test_item_valid(self):
        response = self.c.post(reverse('create-item'), {"item_name":"shirt", "item_price":20.0, "seller":self.id, "brand":"generic", "description":"blue", "image_url":"http://assets.academy.com/mgen/54/10779854.jpg", "item_size":"L", "item_type":"Top"})
        self.assertEqual(response.status_code, 200)

class GetItemTest(TestCase):
    def setUp(self):
        self.c = Client()
        usr = User.objects.create(first_name="John", last_name="Smith", username="jsmith", password="h$4")
        itm = Item.objects.create(item_name="shirt", item_price=20.0, seller=usr, brand="generic", description="blue", image_url="http://assets.academy.com/mgen/54/10779854.jpg", item_size="L", item_type="Top")
        self.id = itm.pk

    def test_item_not_found(self):
        response = self.c.get(reverse('get-item', kwargs={'item_id':(self.id+1)}))
        self.assertEquals(response.status_code, 500)

    def test_get_item_post(self):
        response = self.c.post(reverse('get-item', kwargs={'item_id':(self.id)}))
        self.assertEquals(response.status_code, 500)

    def test_get_item_valid(self):
        response = self.c.get(reverse('get-item', kwargs={'item_id':(self.id)}))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, JsonResponse(model_to_dict(Item.objects.get(pk=self.id))).content)

class GetItemByTest(TestCase):
    def setUp(self):
        self.c = Client()
        usr = User.objects.create(first_name="John", last_name="Smith", username="jsmith", password="h$4")
        itm1 = Item.objects.create(item_name="shirt", item_price=20.0, seller=usr, brand="generic", description="blue", image_url="http://assets.academy.com/mgen/54/10779854.jpg", item_size="L", item_type="Top")
        itm2 = Item.objects.create(item_name="shirt", item_price=20.0, seller=usr, brand="generic", description="blue", image_url="http://assets.academy.com/mgen/54/10779854.jpg", item_size="S", item_type="Top")
        itm3 = Item.objects.create(item_name="shirt", item_price=20.0, seller=usr, brand="generic", description="blue", image_url="http://assets.academy.com/mgen/54/10779854.jpg", item_size="S", item_type="Top")

    def test_get_item_post(self):
        response = self.c.post(reverse('get-item-by', kwargs={'field':'item_size', 'criteria':'S'}))
        self.assertEquals(response.status_code, 500)

    def test_get_item_invalid_field(self):
        response = self.c.get(reverse('get-item-by', kwargs={'field':'item_feel', 'criteria':'S'}))
        self.assertEquals(response.status_code, 500)

    def test_get_items_by_valid(self):
        response = self.c.get(reverse('get-item-by', kwargs={'field':'item_size', 'criteria':'S'}))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, bytes(serializers.serialize('json', Item.objects.filter(item_size='S')), 'utf-8'))

class EditItemTest(TestCase):
    def setUp(self):
        self.c = Client()
        usr = User.objects.create(first_name="John", last_name="Smith", username="jsmith", password="h$4")
        itm = Item.objects.create(item_name="shirt", item_price=20.0, seller=usr, brand="generic", description="blue", image_url="http://assets.academy.com/mgen/54/10779854.jpg", item_size="L", item_type="Top")
        self.usr_id = usr.pk
        self.id = itm.pk
        self.invalid_data = {"item_name":"shirt", "item_price":20.0, "seller":self.usr_id, "brand":"generic", "description":"blue", "image_url":"http://assets.academy.com/mgen/54/10779854.jpg", "item_size":"X", "item_type":"Top"}

    def test_edit_item_not_found(self):
        response = self.c.post(reverse('edit-item', kwargs={'item_id':(self.id+1)}), {"item_name":"shirt", "item_price":20.0, "seller":self.usr_id, "brand":"generic", "description":"blue", "image_url":"http://assets.academy.com/mgen/54/10779854.jpg", "item_size":"S", "item_type":"Top"})
        self.assertEquals(response.status_code, 500)

    def test_edit_item_get_not_post(self):
        response = self.c.get(reverse('edit-item', kwargs={'item_id':(self.id)}), {"item_name":"shirt", "item_price":20.0, "seller":self.usr_id, "brand":"generic", "description":"blue", "image_url":"http://assets.academy.com/mgen/54/10779854.jpg", "item_size":"S", "item_type":"Top"})
        self.assertEquals(response.status_code, 500)

    def test_edit_item_invalid_change(self):
        response = self.c.post(reverse('edit-item', kwargs={'item_id':(self.id)}), self.invalid_data)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, JsonResponse({'errors':ItemForm(self.invalid_data).errors}).content)

    def test_edit_item_valid(self):
        response = self.c.post(reverse('edit-item', kwargs={'item_id':(self.id)}), {"item_name":"shirt", "item_price":20.0, "seller":self.usr_id, "brand":"generic", "description":"blue", "image_url":"http://assets.academy.com/mgen/54/10779854.jpg", "item_size":"S", "item_type":"Top"})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, JsonResponse({'itemID':self.id}).content)
        self.assertEquals(Item.objects.get(pk=self.id).item_size, "S")

class DeleteItemTest(TestCase):
    def setUp(self):
        self.c = Client()
        usr = User.objects.create(first_name="John", last_name="Smith", username="jsmith", password="h$4")
        itm = Item.objects.create(item_name="shirt", item_price=20.0, seller=usr, brand="generic", description="blue", image_url="http://assets.academy.com/mgen/54/10779854.jpg", item_size="L", item_type="Top")
        self.usr_id = usr.pk
        self.id = itm.pk

    def test_del_item_not_found(self):
        response = self.c.post(reverse('delete-item', kwargs={'item_id':(self.id+1)}))
        self.assertEquals(response.status_code, 500)

    def test_del_item_success(self):
        response = self.c.post(reverse('delete-item', kwargs={'item_id':(self.id)}))
        self.assertEquals(response.status_code, 200)
        with self.assertRaises(ObjectDoesNotExist):
            Item.objects.get(pk=self.id)

class LogInTest(TestCase):
    def setUp(self):
        self.c = Client()
        self.c.post(reverse('create-user'), {'first_name':"John", 'last_name':"Smith", 'username':"jsmith", 'password':"h$4"})

    def test_bad_username(self):
        response = self.c.post(reverse('login'), {"username": "smitty", "password":"34322"})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, JsonResponse({'errors':{'username':"Username didn't match any exisiting users in our databse"}}).content)

    def test_bad_password(self):
        response = self.c.post(reverse('login'), {"username": "jsmith", "password":"34322"})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, JsonResponse({'errors':{'password':"Password is incorrect for the user jsmith"}}).content)

    def test_valid_login(self):
        response = self.c.post(reverse('login'), {"username": "jsmith", "password":"h$4"})
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'auth_id')

    def test_get_not_post(self):
        response = self.c.get(reverse('login'), {"username": "jsmith", "password":"h$4"})
        self.assertEquals(response.status_code, 500)

class AuthenticateTest(TestCase):
    def setUp(self):
        self.c = Client()
        #You hae to re-engineer urls because the password only hashes when created through the website
        self.c.post(reverse('create-user'), {'first_name':"John", 'last_name':"Smith", 'username':"jsmith", 'password':"h$4"})
        resp = self.c.post(reverse('login'), {'username':'jsmith', 'password':'h$4'})
        self.auth_resp = json.loads(str(resp.content, 'utf-8'))

    def test_post_not_get(self):
        response = self.c.post(reverse('auth', kwargs={'auth_id':self.auth_resp['auth_id']}))
        self.assertEquals(response.status_code, 500)

    def test_nonexistent_auth(self):
        response = self.c.get(reverse('auth', kwargs={'auth_id':'ks4'}))
        self.assertEquals(response.content, JsonResponse({'logged_in':False}).content)

    def test_valid_auth(self):
        response = self.c.get(reverse('auth', kwargs={'auth_id':self.auth_resp['auth_id']}))
        self.assertContains(response, 'username')

class LogoutTest(TestCase):
    def setUp(self):
        self.c = Client()
        #You hae to re-engineer urls because the password only hashes when created through the website
        self.c.post(reverse('create-user'), {'first_name':"John", 'last_name':"Smith", 'username':"jsmith", 'password':"h$4"})
        resp = self.c.post(reverse('login'), {'username':'jsmith', 'password':'h$4'})
        self.auth_resp = json.loads(str(resp.content, 'utf-8'))

    def test_valid_logout(self):
        response = self.c.post(reverse('logout', kwargs={'auth_id':self.auth_resp['auth_id']}))
        self.assertContains(response, 'success')
        with self.assertRaises(ObjectDoesNotExist):
            Authenticator.objects.get(authenticator=self.auth_resp['auth_id'])

    def test_logout_get_not_post(self):
        response = self.c.get(reverse('logout', kwargs={'auth_id':self.auth_resp['auth_id']}))
        self.assertEquals(response.status_code, 500)

    def test_bad_authenticator(self):
        response = self.c.post(reverse('logout', kwargs={'auth_id':'q333s'}))
        self.assertEquals(response.content, JsonResponse({'errors': "Authenticator does not exist in our database!"}).content)
# Create your tests here.
