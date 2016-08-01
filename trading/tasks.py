from celery import task
from .models import OrderId
import time
from .util.make_possible_deal import make_possible_deal


@task
def try_make_deals():
    """ A background task, which try to make deal for all the orders.
    Run with the celery manager.
    Use django mysql database as the celery broker for test propose. Use Rabbitmq or redis in production.
    """
    make_possible_deal()