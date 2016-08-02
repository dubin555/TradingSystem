###简单的模拟交易服务器
#####需求
>支持下单接口
http://server/trade.do
撤单接口
http://server/cancel_order.do


>每次撮合交易成功，打印交易记录到trade.log, 格式如下
time 成交价格 成交数量

>每笔订单交易成功，或者被撤销，打印交易记录到order.log， 格式如下
time 订单号 订单类型 成交价格 成交数量 状态（全部成交｜部分成交，全部撤销，部分撤销）


#####此例(Django 框架)
对于每笔订单，由当前时间和六位随机数生成一个随机order_id，所有order_id保存到OrderId表中，确保每笔订单都有唯一的order_id。
Database(mysql)
**Order表**

| order_id        | symbol           | type  |amount| done_amount | price|valid|
| ------------- |:-------------:| -----:|------|------|--------|-----|
| id      | 股票名 | 订单类型 |数量|已完成数量| 价格|可操作|


**StockOrder表**
*维护同一种股票下活跃的交易订单。


| order_item       | type           | amount  |price |
| ------------- |:-------------:| -----:|------|
| 外键Order     | 订单类型 |数量|价格|
在撮合交易过程和取消订单中，在更改数据库状态时，使用事务来提交，并对操作的纪录上锁（此例是悲观锁，也可以是乐观锁，但需要更改Database）
使用两个队列试图撮合交易，队列一为买单队列，顺序由最容易到最困难，价格由高到低。
队列二为卖单队列，顺序由最容易到最困难，价格由低到高。
始终有task来轮询所有活跃的股票列表和队列。
#####测试(python3)
```bash
# 开启celery
python3 manage.py celery worker --loglevel=info
```
```python
# 注册异步任务
python3 manage.py shell
>>from trading.tasks import *
>>try_make_deals.delay()
```
```bash
# 开启Django服务器
python3 manage.py runserver
```
```bash
＃ 产生随机订单
python3 test/test_server.py
```
