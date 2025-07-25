import pytest
from .models import *
from django.core.files.uploadedfile import SimpleUploadedFile
from  django.test import Client
from rest_framework import status
from django.urls import reverse
# from django.contrib.auth.models import User
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
User = get_user_model()


client = APIClient()
@pytest.mark.django_db
def test_product():
    product =ProductModel.objects.create(
            productName="Laptop1",
            catagory = CatagoryModel.objects.create(name = 'Laptops'),
            image = SimpleUploadedFile("ecommerce-website/media/uploads/20250705171534New_DELL_XPS_13_9300_Laptop.webp",
                                        b"file_content", content_type="image/jpeg"),
            description="A powerful laptop.",
            originalPrice=100000.00,
            sellingPrice=85000.00
    )
    assert product.productName == "Laptop1"
    assert product.catagory.name == 'Laptops'
    assert product.description == 'A powerful laptop.'
    assert product.originalPrice == 100000.00
    assert product.sellingPrice == 85000.00

@pytest.mark.django_db
def test_api():
    url ='http://127.0.0.1:8000/product/'
    user = User.objects.create_user(username='sara',password='2006')
    client.force_authenticate(user=user)
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db    
def test_authentication():
    url =reverse("product")
    user = User.objects.create_user(username='sara',password='2006')
    client.force_authenticate(user=user)
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
