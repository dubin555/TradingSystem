"""
Helper function to deal with the user json input.
Put data into mysql database from trade.do view and cancel_order.do.
"""
from django.db import transaction
from .gen_order_id import gen_unique_order_id
from trading.models import OrderId, Order, StockTable, StockMessageQueue
from trading.config import logger_order
from datetime import datetime


def _get_order_symbol_class(stock_table, stock_name):
    return stock_table.get(stock_name, None)


def get_valid_order_input_from(received_json_body):
    """Get valid input from trade.do post request.
    If all json data valid, put into database. return true and an unique order_id,
    else return False and an unique order_id
    """
    order_id = gen_unique_order_id()
    symbol = received_json_body.get("symbol", None)
    type = received_json_body.get("type", None)
    price = received_json_body.get("price", None)
    amount = received_json_body.get("amount", None)
    StockSymbol = _get_order_symbol_class(StockTable, symbol)

    # Check the json input valid or not
    if (symbol is None) \
            or (type not in ("buy", "sell", "buy_market", "sell_market")) \
            or (amount is None or amount <= 0) \
            or (StockSymbol is None)\
            or (price is not None and price > 1.1 * StockMessageQueue[symbol]["open_price"])\
            or (price is not None and price < 0.9 * StockMessageQueue[symbol]["open_price"]):
        return False, order_id, None

    if price is not None:
        # type order is "buy" or "sell" with a target price
        if type not in ('buy', 'sell'):
            return False, order_id, None
        order_item = Order(
            order_id=order_id,
            symbol=symbol,
            type=type,
            price=price,
            amount=amount
        )
        stock_item = StockSymbol(
            order_item=order_item,
            type=type,
            amount=amount,
            price=price
        )
    else:
        if type not in ('buy_market', "sell_market"):
            return False, order_id, None
        order_item = Order(
            order_id=order_id,
            symbol=symbol,
            type=type,
            amount=amount
        )
        stock_item = StockSymbol(
            order_item=order_item,
            type=type,
            amount=amount
        )

    # Need to be in one transaction!
    with transaction.atomic():
        order_item.save()
        stock_item.save()
    return True, order_id, order_item


@transaction.atomic
def _cancel_order_in_tables(order_id, symbol):
    """Cancel an order base on the order_id and symbol.
    If order_id and symbol all valid, delete record in the StockOrder, make attribute "valid" False in Order Table.
    Also be done in one transaction!
    """
    result = False
    try:
        order_items = Order.objects.select_for_update().filter(order_id=order_id)
        if len(order_items) > 1:
            raise RuntimeError("Two order items have the same order_id !!!")
        if order_items:
            order_item = order_items[0]
            if symbol != order_item.symbol or not order_item.valid:
                result = False
            else:
                order_item.valid = False
                result = True
            order_item.save()
            # remove the order from the active stock table
            for table in StockTable.values():
                table.objects.select_for_update().filter(order_item=order_item).delete()
    except:
        result = False
    if result:
        CANCELSTATUS = u"被撤销" if order_item.done_amount == 0 else u"剩余被撤销"
        now = datetime.now().strftime("%Y-%m-%d:%H:%M")
        logger_order.info(
                    "%s, %s, %s, %s, %s, %s" %(
                    now,
                    order_item.order_id,
                    order_item.type,
                    order_item.price,
                    order_item.amount - order_item.done_amount,
                    CANCELSTATUS
                    )
        )
    return result


def cancel_order_base_on(received_json_body):
    """Cancel order function.
    """
    order_id = received_json_body.get("order_id", None)
    symbol = received_json_body.get("symbol", None)
    result = _cancel_order_in_tables(order_id, symbol)
    return result, order_id
