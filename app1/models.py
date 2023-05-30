from django.db import models

# Create your models here.

class user(models.Model):
    username=models.CharField(max_length=20)
    password=models.CharField(max_length=20)
    email=models.EmailField(max_length=50)
    phone=models.CharField(max_length=20)
    
    def __str__(self)->str:
        return self.username
    
class Category(models.Model):
    name=models.CharField(max_length=20)
    img=models.ImageField(upload_to='category',default=None)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self)->str:
        return self.name

class Product(models.Model):
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    productimage=models.ImageField(upload_to='product')
    price=models.IntegerField()
    productdescription=models.TextField(default="")
    productquantity=models.IntegerField(null=True)
   

    def __str__(self)->str:
        return self.name

class Ordermodel(models.Model):
    productid=models.IntegerField(),
    productqty=models.IntegerField(),
    userid=models.CharField(max_length=200),
    username=models.CharField(max_length=200),
    useremail=models.CharField(max_length=200),
    usercontact=models.CharField(max_length=200),
    address=models.CharField(max_length=200),
    orderamount=models.IntegerField(),
    paymentMethod=models.CharField(max_length=200),
    transcationId=models.CharField(max_length=200),
    orderdate=models.DateTimeField(auto_created=True,auto_now=True)

    def __str__(self):
        return self.username

