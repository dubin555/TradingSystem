"""
Generate unique order id, use current time, and 6 digits of random numbers.
"""
from django.db import transaction
from datetime import datetime
from random import randrange
from trading.models import OrderId


class GenOrderIdError(Exception):
    pass


def _gen_temp_order_id(max_num=1000000):
    """Generate an unique order_id as a backup plan.
    """
    now = datetime.now()
    ran = str(randrange(max_num))
    max_length = len(str(max_num)) - 1

    order_id = int(now.strftime("%Y%m%d%H%M") + "0" * (max_length - len(ran)) + ran)
    return order_id


@transaction.atomic
def gen_unique_order_id(max_tries=5):
    """Try to use the unique order_id, if there exist duplications,
    try max_tries times for different order_id. Still not succeed, raise a GenOrderIdError for this BUG!
    """
    order_id = _gen_temp_order_id()
    try_times = 1
    while try_times < max_tries:
        if not OrderId.objects.filter(order_id=order_id):
            order = OrderId(order_id=order_id)
            order.save()
            return order_id
        order_id = _gen_temp_order_id()
        try_times += 1
    raise GenOrderIdError("After try max_tries times, still cannot find an unique order_id.")