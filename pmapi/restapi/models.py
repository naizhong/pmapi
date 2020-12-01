from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.
class Stock(models.Model):
    tick = models.CharField(max_length=50)
    lastprice = models.DecimalField(max_digits=20, decimal_places=5)
    name = models.CharField(max_length=50)

class Portfolio(models.Model):
    name = models.CharField(max_length=20)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)

class Position(models.Model):
    portfolio = models.ForeignKey(Portfolio, related_name='positions', on_delete=CASCADE)
    stock = models.ForeignKey(Stock, on_delete=CASCADE)
    openprice = models.DecimalField(max_digits=20, decimal_places=5)
    quantity = models.IntegerField()