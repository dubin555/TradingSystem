from django.db import models
from .util.gen_random_price import simulate_fake_price
# Create your models here.


class Order(models.Model):
    order_id = models.BigIntegerField(primary_key=True)
    symbol = models.CharField(max_length=10)
    type = models.CharField(max_length=12)
    amount = models.IntegerField()
    done_amount = models.IntegerField(default=0, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    valid = models.BooleanField(default=True)

    def __unicode__(self):
        return "%s %s %s" %(self.symbol, self.type, str(self.amount))


class OrderId(models.Model):
    order_id = models.BigIntegerField(primary_key=True)


class Stock(models.Model):
    symbol = models.CharField(primary_key=True, max_length=10)
    open_price = models.DecimalField(max_digits=8, decimal_places=2)


class StockOrder(models.Model):
    order_item = models.ForeignKey(Order)
    type = models.CharField(max_length=12)
    amount = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True)


class WSCN(StockOrder):
    pass


class IBM(StockOrder):
    pass


class APPLE(StockOrder):
    pass


StockTable = {
    "WSCN": WSCN,
    "IBM": IBM,
    "APPLE": APPLE,
}

StockMessageQueue = {
    "WSCN": {
        "open_price": 100,
        "current_price": simulate_fake_price(100),
    },
    "IBM": {
        "open_price": 50,
        "current_price": simulate_fake_price(50),
    },
    "APPLE": {
        "open_price": 80,
        "current_price": simulate_fake_price(80),
    },
}
