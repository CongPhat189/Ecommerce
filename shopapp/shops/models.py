from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField

class User(AbstractUser):
    pass


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
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.shop_name

    class Meta:
        unique_together = ('shop_name', 'owner')


class Product(BaseModel):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=False)
    description = RichTextField()
    price = models.DecimalField(max_digits=10, decimal_places=0)
    image = models.ImageField(upload_to='products/%Y/%m')
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.name




class Tag(BaseModel):
    name = models.CharField(max_length=50, unique= True)

    def __str__(self):
        return self.name




