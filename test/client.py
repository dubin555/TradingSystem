# -*- coding: utf-8 -*-
"""
A simple test request to trade.do to post a order
"""
import requests
import json

url = "http://localhost:8000/trading/trade.do/"
data = {
    'symbol': 'IBM',
    'type': 'sell',
    'price': 50.00,
    'amount': 100
}
headers = {'content-type': 'application/json'}
r = requests.post(url, data=json.dumps(data), headers=headers)
print (r.text)

