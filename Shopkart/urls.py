from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('detail/<int:id>/', detail, name='product_detail'),
    path('show/',show),
    path('product/',ProductView.as_view()),
    path('product/<int:id>/',ProductView.as_view()),
    path('catagory/',CatagoryView.as_view()),
    path('catagory/<int:id>/',CatagoryView.as_view()),
]
