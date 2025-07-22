from django.test import TestCase
from rest_framework.test import APITestCase,APIClient
from django.urls import reverse
from .models import *
from .views import *
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
# import tempfile


class CatagoryTest(TestCase):
    def setUp(self):
        self.client =APIClient()
        self.catagory = ProductModel.objects.create(name='Notebook',description='something about notebook')
        self.list_url = reverse('catagory')
    def list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']),1)
    def create(self):
        data = { "name": "dress","description":"something about dressess"}
        response = self.client.post(self.list_url,data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(CatagoryModel.objects.count(),1)
    def update(self):
        data =  { "name": "dressess","description":"something about dressess"}
        response = self.client.put(self.list_url,data)
        self.catagory.refresh_from_db()
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(self.catagory.name,'dressess')
    def delete(self):
        response = self.client.delete(self.list_url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertTrue(CatagoryModel.objects.filter(id=self.catagory.id).exists())
  

class ProductViewTest(APITestCase):
    def setUp(self):
        self.client =APIClient()
        self.category = CatagoryModel.objects.create(name="Laptops")
        self.product = ProductModel.objects.create(
            productName="Laptop1",
            catagory=self.category,
            image = SimpleUploadedFile("ecommerce-website/media/uploads/20250705171534New_DELL_XPS_13_9300_Laptop.webp", b"file_content", content_type="image/jpeg"),
            description="A powerful laptop.",
            originalPrice=100000.00,
            sellingPrice=85000.00
        )
        self.list_url = reverse('product')
        self.detail_url = reverse('product_detail', kwargs={'id': self.product.id})

    def test_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)

    def test_retrieve(self):
        response = self.client.get(self.detail_url,format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.product.productName, "Laptop1")


    def test_create(self):
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
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(ProductModel.objects.filter(id=self.product.id).exists())