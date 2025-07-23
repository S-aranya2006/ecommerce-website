import pytest
from .models import *
from django.core.files.uploadedfile import SimpleUploadedFile
from  django.test import Client


client = Client()
@pytest.mark.django_db
def test_product():
    product =ProductModel.objects.create(
            productName="Laptop1",
            catagory = CatagoryModel.objects.create(name = 'Laptops'),
            image = SimpleUploadedFile("ecommerce-website/media/uploads/20250705171534New_DELL_XPS_13_9300_Laptop.webp", b"file_content", content_type="image/jpeg"),
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
    url ='http://127.0.0.1:8000/show/'
    response = client.get(url)
    assert response.status_code == 200
    
@pytest.mark.django_db
def test_api2():
    url ='http://127.0.0.1:8000/catagory/'  
    response = client.get(url)
    assert response.status_code == 200