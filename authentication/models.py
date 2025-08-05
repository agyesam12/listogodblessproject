from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=250, null=True)
    email = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.email}"
    

class Product(models.Model):
    name = models.CharField(max_length=220)
    price = models.FloatField()
    digital = models.BooleanField(default=False,null=True,blank=True)
    image = models.ImageField(null=True,blank=True)

    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
         try:
              url = self.image.url
         except:
              url = ''
         return url
    
class Order(models.Model):     
     customer = models.ForeignKey(Customer ,on_delete=models.SET_NULL,null=True,blank=True)
     date_ordered = models.DateTimeField(auto_now_add=True)
     complete = models.BooleanField(default=False)

     @property
     def get_carttotal(self):
          order_items = self.orderitem_set.all()
          total = sum([item.get_total for item in order_items])
          return total

     @property
     def get_cart_items(self):
          order_items = self.orderitem_set.all()
          total = sum([item.quantity for item in order_items])
          return total



     def __str__(self):
            return f"{self.customer.email}"
        

class OrderItem(models.Model):
     product = models.ForeignKey(Product, on_delete=models.SET_NULL,null=True)
     order = models.ForeignKey(Order, on_delete=models.SET_NULL,null=True)
     quantity = models.PositiveIntegerField(default=0,null=True,blank=True)
     date_added = models.DateTimeField(auto_now_add=True)

     @property
     def get_total(self):
         total = self.quantity * self.product.price
         return total

     def __str__(self):
          return self.product.name


class ShippingAddress(models.Model):
     customer =models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)
     order = models.ForeignKey(Order, null=True,blank=True,on_delete=models.SET_NULL)
     address = models.CharField(max_length=220,null=True)
     city = models.CharField(max_length=220,null=True)
     state = models.CharField(max_length=220,null=True)
     zipcode = models.CharField(max_length=220,null=True)
     date_added = models.DateTimeField(auto_now_add=True)


     def  __str__(self):
          return self.address