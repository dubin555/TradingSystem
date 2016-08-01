import logging


def get_logger(name, logfile):
    logger = logging.getLogger(name)
    logger.addHandler(logging.FileHandler(logfile))
    logger.setLevel(logging.INFO)
    return logger


logger_trade = get_logger("trade", "./trading/logs/trade.log")
logger_order = get_logger("order", "./trading/logs/order.log")