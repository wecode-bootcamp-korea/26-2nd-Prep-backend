from django.db import models

from core.models import TimeStamp

class Category(TimeStamp):
    name = models.CharField(max_length=50)
    image_url = models.CharField(max_length=500)

    class Meta:
        db_table = 'categories'

class SubCategory(TimeStamp):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        db_table = 'sub_categories'

class Product(TimeStamp):
    name = models.CharField(max_length=100)
    sub_category = models.ForeignKey('SubCategory', on_delete=models.CASCADE)
    address = models.ForeignKey('ProductAddress', on_delete=models.CASCADE)
    expiration_date = models.ForeignKey('ExpirationDate', on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag', related_name = 'products', through='ProductTag')
    description = models.TextField()

    class Meta:
        db_table = 'products'

class ProductAddress(TimeStamp):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'product_address'

class Option(TimeStamp):
    date = models.DateTimeField()
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=3)
    discount_rate = models.DecimalField(max_digits=5, decimal_places=3)
    limited_quantity = models.IntegerField(default=0)

    class Meta:
        db_table = 'options'

class ProductImage(TimeStamp):
    image_url = models.CharField(max_length=500)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)

    class Meta:
        db_table = 'products_images'

class ProductTag(TimeStamp):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE)

    class Meta:
        db_table = 'products_tags'

class Tag(TimeStamp):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'tags'

class ExpirationDate(TimeStamp):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'expiration_dates'

class MainImage(TimeStamp):
    image_url = models.CharField(max_length=500)

    class Meta:
        db_table = 'main_images'