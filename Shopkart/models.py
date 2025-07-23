from django.db import models
import datetime
import os
# Create your models here.
class CatagoryModel(models.Model):
    name = models.CharField(max_length=200,null=False,blank=False,unique=True)
    description = models.TextField(max_length=500,null=False,blank=False)
  
    class Meta:
        ordering =['id']

    def __str__(self):
        return self.name

def getFileName(request,filename):
     nowtime = datetime.datetime.now().strftime("%Y%m%d%H%M%S") 
     newFileName = "%s%s"%(nowtime,filename)
     return os.path.join('uploads/',newFileName)

class ProductModel(models.Model):
    productName =  models.CharField(max_length=200,null=False,blank=False)
    catagory = models.ForeignKey(CatagoryModel,on_delete=models.CASCADE,related_name="Products") 
    image = models.ImageField(upload_to=getFileName,null=True,blank=True)  
    description = models.TextField(max_length=1000,null=False,blank=False)   
    originalPrice =models.DecimalField(max_digits=10,decimal_places=2)
    sellingPrice =models.DecimalField(max_digits=10,decimal_places=2)

    class Meta:
        ordering =['-id']

    def __str__(self):
        return self.productName    
