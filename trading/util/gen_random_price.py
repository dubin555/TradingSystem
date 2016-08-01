"""For simulate the server, generator a current price between (90% ~ 110%)open price
"""
import random


def simulate_fake_price(open_price):
    return random.randrange(int(0.9*open_price), int(1.1*open_price))