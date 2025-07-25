from django.test import TestCase
from rest_framework.test import APITestCase,APIClient
from django.urls import reverse
from .models import *
from .views import *
from rest_framework import status
# from django.core.files.uploadedfile import SimpleUploadedFile
# import tempfile
import pytest
from django.contrib.auth import get_user_model
User =get_user_model()

# @pytest.mark.django_db
# class CatagoryTest(TestCase):
#     def setUp(self):
#         self.client =APIClient()
#         self.catagory = CatagoryModel.objects.create(name='Notebook',description='something about notebook')
#         user = User.objects.create_user(username='sara',password='2006')
#         self.client.force_authenticate(user=user)
#         self.list_url = reverse('catagory')
#     def test_list(self):
#         response = self.client.get(self.list_url)
#         self.assertEqual(response.status_code,status.HTTP_200_OK)
#         self.assertGreaterEqual(len(response.data['results']),1)
#     def test_create(self):
#         data = { "name": "dress","description":"something about dressess"}
#         response = self.client.post(self.list_url,data)
#         self.assertEqual(response.status_code,status.HTTP_200_OK)
#         self.assertEqual(CatagoryModel.objects.count(),2)
 

@pytest.mark.django_db
class ProductViewTest(APITestCase):
    def setUp(self):     
        self.client =APIClient()
        user = User.objects.create_user(username='sara',password='2006')
        self.client.force_authenticate(user=user)
        self.category = CatagoryModel.objects.create(name="Laptops")
        self.product = ProductModel.objects.create(
            productName="Laptop1",
            catagory=self.category,
            image = "ecommerce-website/media/uploads/20250705171534New_DELL_XPS_13_9300_Laptop.webp",
            originalPrice=100000.00,
            sellingPrice=85000.00
        )
    def test_list(self):
        self.list_url = 'http://127.0.0.1:8000/product/'
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)

    def test_retrieve(self):
        self.detail_url =reverse('product_detail',kwargs={'id':self.product.id})
        self.list_url = f'/product/{self.product.id}/'
        response = self.client.get(self.detail_url,format='json')
        response_api = self.client.get(self.list_url,format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_api.status_code,status.HTTP_200_OK)
        self.assertEqual(self.product.productName, "Laptop1")

    def test_create(self):
        self.list_url = 'http://127.0.0.1:8000/product/'
        data = {
            "productName": "Mouse",
            "catagory": self.category.id,
            "image":"ecommerce-website/media/uploads/20250705171534New_DELL_XPS_13_9300_Laptop.webp",
            "description": "Wireless mouse",
            "originalPrice": "1000.00",
            "sellingPrice": "800.00"
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ProductModel.objects.count(), 1)
    def test_update(self):
        self.detail_url =reverse('product_detail',kwargs={'id':self.product.id})
        data = {
            "productName": "Laptop1",
            "catagory": self.category.id,
            "image":"ecommerce-website/media/uploads/20250705171534New_DELL_XPS_13_9300_Laptop.webp",
            "description": "Updated description",
            "originalPrice": "120000.00",
            "sellingPrice": "95000.00"
        }
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.productName, "Laptop1")

    def test_delete(self):
        self.detail_url =reverse('product_detail',kwargs={'id':self.product.id})
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(ProductModel.objects.filter(id=self.product.id).exists())