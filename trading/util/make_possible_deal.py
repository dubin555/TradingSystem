"""
Try to make possible deal for buying and selling orders.
"""
from django.db import transaction
from trading.models import Order, StockMessageQueue, StockTable, WSCN, IBM, APPLE
from itertools import chain
from trading.config import logger_trade, logger_order
from datetime import datetime


def _deal_price_from_orders(buy_order, sell_order):
    """Try to find whether buy order and sell order can make a deal.
    if buy order price >= sell order price, they can make the deal.
    The deal price is base on the current price, buy order price, sell order price
    @:return can_make_deal_or_not, the-price-for-this-deal
    """
    current_price = StockMessageQueue[buy_order.order_item.symbol]["current_price"]
    can_make_deal = True
    deal_price = None
    if buy_order.type == "buy_market" and sell_order.type == "sell_market":
        deal_price = current_price
    elif buy_order.type == "buy_market" and sell_order.type == "sell":
        # The buy order doesn't care the price, deal price take the max price
        deal_price = max(current_price, sell_order.price)
    elif buy_order.type == "buy" and sell_order.type == "sell_market":
        # The sell order doesn't care the price, deal price take the min price
        deal_price = min(buy_order.price, current_price)
    else:
        if buy_order.price < sell_order.price:
            can_make_deal = False
        else:
            deal_price = sell_order.price
    return can_make_deal, deal_price


def _deal_amount_from_orders(buy_order, sell_order):
    """Make deal for buy order and sell order with the best price and maximum amount
    Should be done in one transaction!!!!!!!!!
    """
    # Maybe enum is better
    BUYSTATUS, SELLSTATUS = u"全部成交", "全部成交"
    deal_amount = min(buy_order.amount, sell_order.amount)
    buy_order_item = buy_order.order_item
    sell_order_item = sell_order.order_item
    if sell_order.amount > buy_order.amount:
        sell_order.amount -= buy_order.amount
        buy_order.amount = 0
    elif sell_order.amount == buy_order.amount:
        sell_order.amount, buy_order.amount = 0, 0
    else:
        buy_order.amount -= sell_order.amount
        sell_order.amount = 0
    buy_order_item.done_amount += deal_amount
    sell_order_item.done_amount += deal_amount

    # Compare the amount and done_amount for judge the BUYSTATUS and SELLSTATUS!
    if buy_order_item.amount > buy_order_item.done_amount:
        BUYSTATUS = "部分成交"
    elif buy_order_item.amount == buy_order_item.done_amount:
        buy_order_item.valid = False
    if sell_order_item.amount > sell_order_item.done_amount:
        SELLSTATUS = "部分成交"
    elif sell_order_item.amount == sell_order_item.done_amount:
        sell_order_item.valid = False

    # Done in one unique transaction!
    buy_order.save()
    sell_order.save()
    buy_order_item.save()
    sell_order_item.save()
    return BUYSTATUS, SELLSTATUS, deal_amount


def make_possible_deal():
    """Try to make deal done for all the active orders in every Stock.
    Use two Queue, one for buy order queue from the easiest to buy,
    one for sell order queuq from eaiest to sell.
    if find two orders can make deal done, set the transaction on, add lock for the two orders until it's done!
    """
    stock_tables = StockTable.values()
    while True:
        # loop all the existing stock
        for stock in stock_tables:
            # buy_market is the easiest to buy
            want_buy = stock.objects.filter(type="buy_market")
            want_buy_market = stock.objects.filter(type="buy").order_by("-price")
            buy_queue = list(chain(want_buy, want_buy_market))
            # sell_market is the easiest to sell
            want_sell = stock.objects.filter(type="sell_market")
            want_sell_market = stock.objects.filter(type="sell").order_by("price")
            sell_queue = list(chain(want_sell, want_sell_market))
            if not buy_queue or not sell_queue:
                continue
            buy_order = buy_queue.pop(0)
            sell_order = sell_queue.pop(0)
            while buy_order and sell_order:
                can_make_deal, deal_price = _deal_price_from_orders(buy_order, sell_order)
                if not can_make_deal:
                    break

                # Buy order and sell order can make a deal, start a transaction and lock the two orders!
                # All operation in one transaction
                with transaction.atomic():
                    buy_order = stock.objects.select_for_update().get(order_item=buy_order.order_item)
                    sell_order = stock.objects.select_for_update().get(order_item=sell_order.order_item)

                    # Double check for the sell order and buy order in case of canceling order before!!!
                    if not buy_order or not sell_order:
                        break
                    can_make_deal, deal_price = _deal_price_from_orders(buy_order, sell_order)
                    if not can_make_deal:
                        break
                    # Double check done!!!

                    buy_status, sell_status, deal_amount = _deal_amount_from_orders(buy_order, sell_order)

                    # Log all the information of the deal.
                    # If this take too much times, define a task, then send the log job to the worker queue.
                    now = datetime.now().strftime("%Y-%m-%d:%H:%M")
                    logger_trade.info("%s, %s , %s" %(now, deal_price, deal_amount))
                    logger_order.info("%s, %s, %s, %s, %s, %s"
                                      %(
                                        now,
                                        buy_order.order_item.order_id,
                                        buy_order.order_item.type,
                                        deal_price,
                                        deal_amount,
                                        buy_status
                                        ))
                    logger_order.info("%s, %s, %s, %s, %s, %s"
                                      %(
                                        now,
                                        sell_order.order_item.order_id,
                                        sell_order.order_item.type,
                                        deal_price,
                                        deal_amount,
                                        sell_status
                                        ))
                    if buy_order.amount == 0:
                        buy_order.delete()
                        buy_order = buy_queue.pop(0) if len(buy_queue) >= 1 else None
                    if sell_order.amount == 0:
                        sell_order.delete()
                        sell_order = sell_queue.pop(0) if len(sell_queue) >= 1 else None









