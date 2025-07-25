from django.shortcuts import render, get_object_or_404
from .models import *
from .serializers import *
from rest_framework.generics import GenericAPIView
from rest_framework import mixins
from rest_framework.response import Response
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .pagination import *
from rest_framework.permissions import IsAuthenticated
from django.contrib import messages

def home(request):
    # catagory = CatagoryModel.objects.prefetch_related('Products')
    product =ProductModel.objects.all()
    pagination = Paginator(product,8)
    count = ProductModel.objects.aggregate(Count('id'))
    tpage = count['id__count']
    totalPageNo = int(tpage/8)
    numbers = range(1,totalPageNo+2)
    pageno = request.GET.get('page')
    
    try:
        page_obj = pagination.get_page(pageno)  
    except PageNotAnInteger:
        page_obj = pagination.page(1)
    except EmptyPage:
        page_obj = pagination.page(pagination.num_pages)

    print(pagination.page(1))
    print(pagination.page(pagination.num_pages))
    data={
    #'catagories' : catagory,
     'products':page_obj,
     'numbers':numbers
    }    
    return render(request, 'home.html', data)

def detail(request, id):
    product = get_object_or_404(ProductModel.objects.select_related('catagory'),id=id)
    return render(request, 'detail.html', {'product': product})

def show(request):
    query = request.GET('filterproduct')
    if len(query) > 100:
      allproducts = ProductModel.objects.none()
    else :
       allproductstitle = ProductModel.objects.filter(productName__icontains = query)
       allproductscatagory = ProductModel.objects.filter(catagory__icontains = query)   
       allproducts = allproductstitle.union(allproductscatagory)
    if allproducts.count() == 0:
        messages.warning(request,'No serach results') 
    data ={
        "query": query,
        "allproducts":allproducts
    }  
    return render(request,'show.html',data) 


    
class ProductView(GenericAPIView,mixins.CreateModelMixin,mixins.DestroyModelMixin,mixins.ListModelMixin,
                  mixins.UpdateModelMixin,mixins.RetrieveModelMixin):
    permission_classes =[IsAuthenticated]
    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'
    pagination_class= Pagination
    
    def get(self,request,id=None):
        if id :
           return self.retrieve(request,id=id) 
        return self.list(request)
    def post(self,request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Product added!")
        return Response(serializer.errors,status=200)
    def put(self,request,id=None):
        instance = self.get_object()
        serializer = ProductSerializer(instance,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Product updated!")
        return Response(serializer.errors,status=200)
    def delete(self,request,id=None):
        self.destroy(request)
        return Response("Product deleted!")
    
class CatagoryView(GenericAPIView,mixins.CreateModelMixin,mixins.ListModelMixin,mixins.RetrieveModelMixin,
              mixins.UpdateModelMixin,mixins.DestroyModelMixin):
    queryset = CatagoryModel.objects.all() 
    serializer_class = CategorySerializer
    lookup_field ='id'
    def get(self,request,id=None):
        if id:
            return self.retrieve(request,id=id)
        return self.list(request)
    def post(self,request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Catagory added!")
        return Response(serializer.errors,status=200)
    def put(self,request,id=None):
        instance = self.get_object()
        serializer = CategorySerializer(instance,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Catagory updated!")
        return Response(serializer.errors,status=200)
    def delete(self,request,id=None):
        self.destroy(request)
        return Response("Catagory deleted!")
   




#    def show(request):
#     count = ProductModel.objects.aggregate(Count('id'))
#     product =ProductModel.objects.only('productName','description','sellingPrice')
#     values = ProductModel.objects.values('description')
#     print(count)
    # return render(request,'show.html',{'products': product,'values':values,'count':count}) 
