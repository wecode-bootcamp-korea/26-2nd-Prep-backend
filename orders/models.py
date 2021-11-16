from django.db import models

from core.models import TimeStamp
from products.models import Option
from users.models import User

class OrderItem(TimeStamp):
    order = models.ForeignKey("Order", on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    class Meta:
        db_table = 'order_items'

class Order(TimeStamp):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.ForeignKey("OrderStatus", on_delete=models.CASCADE) 

    class Meta:
        db_table = 'orders'

class OrderStatus(TimeStamp):
    class Status(models.IntegerChoices):
        BEFORE_DEPOSIT   = 1 
        STAND_BY         = 2 
        DEPOSIT_COMPLTED = 3 
        CANCEL           = 4 

    description = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'order_statuses'