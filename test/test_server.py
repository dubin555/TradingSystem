"""Random post some requests to the server to test the source file
"""

import requests
import time
import random
import os
import json


def remove_previous_logs():
    """Remove the old logfiles
    """
    try:
        os.remove("../trading/logs/order.log")
        os.remove("../trading/logs/trade.log")
    except Exception as e:
        pass


def _send_order_random(types, symbol, url):
    """Generate a random request order,
    @:param type: random choice of types,
    @:param url: target url
    """
    order_type = random.choice(types)
    order_amount = random.randrange(1,100)
    # if type is "buy" or "sell", generate a price for order
    order_price = random.randrange(90, 110) if order_type in ["buy", "sell"] else None
    data = {
        'symbol': symbol,
        'type': order_type,
        'price': order_price,
        'amount': order_amount,
    }
    headers = {'content-type': 'application/json'}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    print (r.text)


def send_orders_random(types, symbol, url, times):
    """Generate a target amount of orders for post request
    """
    counter = 0
    while counter < times:
        time.sleep(0.25)
        _send_order_random(types, symbol, url)
        counter += 1


def cancel_orders(symbol, order_id, url):
    """Generate a cancel order request
    """
    data = {
        'symbol': symbol,
        'order_id': order_id,
    }
    headers = {'content-type': 'application/json'}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    print (r.text)


types = ["buy", "sell", "buy_market", "sell_market"]
url = "http://localhost:8000/trading/trade.do/"
cancel_url = "http://localhost:8000/trading/cancel_order.do/"


if __name__ == "__main__":
    #remove_previous_logs()
    send_orders_random(types, "WSCN", url, 100)
    #cancel_orders("WSCN", 201607311320431930 ,cancel_url)
    #cancel_orders("WSCN", 201607311320845395,cancel_url)
