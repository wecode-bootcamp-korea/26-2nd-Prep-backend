from django.db import models

from core.models import TimeStamp
from users.models import User
from products.models import Option

class Review(TimeStamp):
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    star_rate = models.DecimalField(max_digits=2, decimal_places=1)
    comment = models.CharField(max_length=500)

    class Meta:
        db_table = 'reviews'

class ReviewImage(TimeStamp):
    review = models.ForeignKey("Review", on_delete=models.CASCADE)
    storage_path = models.CharField(max_length=100)
    image_url = models.CharField(max_length=100)

    class Meta:
        db_table = 'reviews_images'

class Like(TimeStamp):
    review = models.ForeignKey("Review", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'likes'