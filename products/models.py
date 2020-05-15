from django.db import models
from django.contrib.auth import get_user_model
from django_countries.fields import CountryField
from django.db.models.signals import post_save
from PIL import Image
from ckeditor.fields import RichTextField

# Create your models here.

LABEL_COLOR = (
    ('P','primary'),
    ('D','danger'),
    ('S','secondary')
)

ADDRESS_TYPES = (
    ('S','Shipping'),
    ('B','Billing'),
)

user = get_user_model()

class Category (models.Model):
    name = models.CharField(max_length=200)
    pramry_category = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Product(models.Model):
    main_image = models.ImageField(upload_to='products_images', null=True, blank=True)
    name = models.CharField(max_length=300)
    sub_name = models.CharField(max_length=300)
    descraption = RichTextField()
    price = models.FloatField()
    descount_price = models.FloatField()
    label = models.CharField(choices=LABEL_COLOR, max_length=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE ,null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return self.slug

    

class Cart(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE )
    quantity = models.IntegerField(default=1)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.quantity} of {self.item.name}'

    def get_item_total(self):
        return self.item.price * self.quantity

class Coupon(models.Model):
    code = models.CharField(max_length=30)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    amount = models.IntegerField(default=0)
    active = models.BooleanField()
    
    def __str__(self):
        return self.code

class Order(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE )
    number = models.CharField(max_length=20, null=True, blank=True)
    order_items = models.ManyToManyField(Cart)
    ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    billing_adress = models.ForeignKey('Adresse' ,related_name='Billing' ,on_delete=models.SET_NULL , null = True, blank = True)
    shipping_adress = models.ForeignKey('Adresse' ,related_name='Shipping' ,on_delete=models.SET_NULL , null = True, blank = True)
    payment = models.ForeignKey('Payment' , on_delete=models.SET_NULL , null = True, blank = True)
    coupon = models.ForeignKey('Coupon' , on_delete=models.CASCADE, null=True, blank=True)
    refunded_requested = models.BooleanField(default=False)
    refund_accepted = models.BooleanField(default=False)
    been_deliverd = models.BooleanField(default=False)
    arrived = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username
    
    def get_total(self):
        order = 0
        for order_price in self.order_items.all():
            order += order_price.get_item_total()
        if self.coupon is not None :
             return order - self.coupon.amount
        else:
            return order


class Adresse(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE )
    email = models.ImageField()
    adress1 = models.CharField(max_length=300)
    adress2 = models.CharField(max_length=300)
    country = CountryField()
    zip_code = models.CharField(max_length=20)
    adresse_type = models.CharField(max_length=1,choices=ADDRESS_TYPES)
    defualt = models.BooleanField(null=True)
    def __str__(self):
        return self.user.username

class Payment(models.Model):
    user = models.ForeignKey(user, on_delete=models.SET_NULL, null=True, blank=True )
    amount = models.FloatField()
    datestamp = models.DateTimeField(auto_now_add=True)
    strip_charg_id = models.CharField(max_length=50)
    def __str__(self):
        return self.user.username

class User_profile(models.Model):
    user = models.OneToOneField(user, on_delete=models.CASCADE)
    stripi_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purshase = models.BooleanField(default=False) 

    def __str__(self):
        return f'{self.user.username} profile'

def creat_profile(sender, **kwargs):
    if kwargs['created']:
        User_profile.objects.create(user=kwargs['instance'])

post_save.connect(creat_profile ,sender=user )

class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    email = models.EmailField()
    reson = models.TextField()
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.order.user} asks for refund "


