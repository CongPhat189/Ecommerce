from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField



class User(AbstractUser):
    avatar = CloudinaryField('avatar', null=True, blank=True)
    ROLE_CHOICES = [
        ('seller', 'Seller'),
        ('user', 'User'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    is_verified = models.BooleanField(default=False)


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True




class Category(BaseModel):
    name = models.CharField(max_length=100, null=False)


    def __str__(self):
        return self.name



class Shop(BaseModel):
    shop_name = models.CharField(max_length=255, null=False)
    description = RichTextField()
    image = models.ImageField( upload_to='shops/%Y/%m')
    category = models.ForeignKey(Category, on_delete=models.RESTRICT, related_name='shops')
    owner = models.ForeignKey(User,related_name='shops', on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.shop_name

    class Meta:
        permissions = [
            ("manage_shop", "Can manage shop"),
        ]
        unique_together = ('shop_name', 'owner')



class Product(BaseModel):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=False)
    description = RichTextField()
    price = models.DecimalField(max_digits=10, decimal_places=0)
    image = models.ImageField(upload_to='products/%Y/%m')
    tags = models.ManyToManyField('Tag')



    class Meta:
        permissions = [
            ("manage_product", "Can manage product"),
        ]


    def __str__(self):
        return self.name




class Tag(BaseModel):
    name = models.CharField(max_length=50, unique= True)

    def __str__(self):
        return self.name



class Order(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Cash on Delivery'),
        ('momo', 'MoMo'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=0)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)
    created_date = models.DateTimeField(auto_now_add=True)


class Interaction(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null= False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False)


    class Meta:
        abstract = True


class Comment(Interaction):
    content = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.content

class Like(Interaction):
    active = models.BooleanField(default=True)


    class Meta:
        unique_together = ('user', 'product')


class Rating(Interaction):
    rate = models.SmallIntegerField(default=0)






