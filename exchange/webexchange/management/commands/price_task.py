from django.core.management.commands.runserver import Command as RunserverCommand
from django.core.management.base import BaseCommand
import threading
import time

class Order:
    def __init__(self, order_type, order_id, stock_name, price, quantity):
        self.order_type = order_type  # 订单类型，buy 或 sell
        self.order_id = order_id  # 订单编号
        self.stock_name = stock_name  # 股票名称
        self.price = price  # 订单价格
        self.quantity = quantity  # 订单数量


class OrderManager:
    def __init__(self):
        self.buy_orders = []  # 存储买单
        self.sell_orders = []  # 存储卖单
        self.lock = threading.Lock() # 添加线程锁

    def add_order(self, order):
        with self.lock: # 对临界区代码添加线程锁
            if order.order_type == 'buy':
                self.buy_orders.append(order)
            elif order.order_type == 'sell':
                self.sell_orders.append(order)

    def match_orders(self):
        with self.lock: # 对临界区代码添加线程锁
            while len(self.buy_orders) > 0 and len(self.sell_orders) > 0:
                buy_order = self.buy_orders[0]
                sell_order = self.sell_orders[0]
                if buy_order.price >= sell_order.price:
                    trade_quantity = min(buy_order.quantity, sell_order.quantity)
                    print(f"成交：{buy_order.order_id} 买入 {sell_order.stock_name} {trade_quantity} 股，单价 {sell_order.price}")
                    print(f"成交：{sell_order.order_id} 卖出 {sell_order.stock_name} {trade_quantity} 股，单价 {sell_order.price}")
                    print("-----------")
                    buy_order.quantity -= trade_quantity
                    sell_order.quantity -= trade_quantity
                    if buy_order.quantity == 0:
                        self.buy_orders.pop(0)
                    if sell_order.quantity == 0:
                        self.sell_orders.pop(0)
                else:
                    break
            return None


class OrderProducer(threading.Thread):
    def __init__(self, order_manager, order_type, stock_name, price, quantity):
        super().__init__()
        self.order_manager = order_manager
        self.order_type = order_type
        self.stock_name = stock_name
        self.price = price
        self.quantity = quantity

    def run(self):
        order = Order(self.order_type, threading.current_thread().name, self.stock_name, self.price, self.quantity)
        self.order_manager.add_order(order)
        print(f"提交订单：{order.order_id} {order.order_type} {order.stock_name} {order.quantity} 股，单价 {order.price}")


class OrderConsumer(threading.Thread):
    def __init__(self, order_manager):
        super().__init__()
        self.order_manager = order_manager

    def run(self):
        while self.order_manager.match_orders() is not None:
            time.sleep(0.1)

class Command(RunserverCommand):
    help = 'Starts the development server with a task.'

    def inner_run(self, *args, **options):
        .start() # 启动任务
        super().inner_run(*args, **options)


class Commad(BaseCommand):
    help = "Price Matching Task"

    def handle(self, *args, **option):
        order_manager = OrderManager()
        while True:
            producer1 = OrderProducer(order_manager, 'buy', 'ABC', 10, 100)
            producer2 = OrderProducer(order_manager, 'buy', 'ABC', 11, 200)
            producer3 = OrderProducer(order_manager, 'sell', 'ABC', 12, 150)
            producer4 = OrderProducer(order_manager, 'sell', 'ABC', 9, 50)

            consumer = OrderConsumer(order_manager)

            producer1.start()
            producer2.start()
            producer3.start()
            producer4.start()

            consumer.start()

            producer1.join()
            producer2.join()
            producer3.join()
            producer4.join()

            consumer.join()
