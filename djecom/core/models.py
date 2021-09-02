from django.conf import settings
from django.db import models
import datetime

class Customer(models.Model):
        first_name = models.CharField(max_length=100)
        last_name = models.CharField(max_length=100)
        phone = models.IntegerField()
        email = models.EmailField(max_length=50)
        password = models.CharField(max_length=20)
        
        def register(self):
            self.save()
            
        @staticmethod
        def get_customer_by_email(email):
            try:
                return Customer.objects.get(email = email)
            except:
                return False
            
        # Check if email already exists
        def isExists(self):
            if Customer.objects.filter(email=self.email):
                return True
            return False

class Category(models.Model):
    name = models.CharField(max_length=50)
    
    @staticmethod 
    def get_all_categories():
        return Category.objects.all()
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category,on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=200,default='',null=True,blank=True)
    image = models.ImageField(upload_to='media/products')
    
    @staticmethod
    def get_product_by_id(ids):
        return Product.objects.filter(id__in=ids)
    
    @staticmethod
    def get_all_products():
        return Product.objects.all()
    
    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Product.objects.filter(category=category_id)
        else:
            return Product.get_all_products();
    
class Orders(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField(max_length=100,default='',blank=True)
    phone = models.CharField(max_length=10,default='',blank=True)
    date = models.DateField(default=datetime.datetime.today)
    
    def placeOrder(self):
        self.save()
    