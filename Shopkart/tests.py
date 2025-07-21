from django.test import TestCase
from rest_framework.test import APITestCase,APIClient
from django.urls import reverse
from .models import *
from .views import *
from rest_framework import status
# from django.core.files.uploadedfile import SimpleUploadedFile
# import tempfile


class CatagoryTest(TestCase):
    def Test(self):
        catagory = CatagoryModel.objects.create(name='Notebook',description='something')
        self.assertEqual(catagory.name,'Notebook')
        self.assertEqual(catagory.description ,'something')
        
class ProductViewTest(APITestCase):
    def setUp(self):
        self.client =APIClient()
        self.category = CatagoryModel.objects.create(name="Laptops")
        self.product = ProductModel.objects.create(
            productName="Laptop1",
            catagory=self.category,
            image="ecommerce-website/media/uploads/20250705171534New_DELL_XPS_13_9300_Laptop.webp",
            description="A powerful laptop.",
            originalPrice=100000.00,
            sellingPrice=85000.00
        )
        self.list_url = reverse('product')
        self.detail_url = reverse('product_detail', kwargs={'id': self.product.id})

    def test_list_products(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)

    def test_retrieve_product(self):
        response = self.client.get(self.detail_url,format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.product.productName, "Laptop1")

    def test_create_product(self):
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

    def test_update_product(self):
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

    def test_delete_product(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(ProductModel.objects.filter(id=self.product.id).exists())



        
