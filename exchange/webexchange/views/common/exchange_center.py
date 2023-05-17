import threading
import time
import hashlib

class Order:
    def __init__(self, order_type, order_id, stock_name, price, quantity, producer_name):
        self.order_type = order_type  # 订单类型，buy 或 sell
        self.order_id = order_id  # 订单编号
        self.stock_name = stock_name  # 股票名称
        self.price = price  # 订单价格
        self.quantity = quantity  # 订单数量
        self.producer_name = producer_name

    def __str__(self):
        return f"[ID]{self.order_id} [STOCK]{self.stock_name} [PRICE]{self.price} [QUANTITY]{self.quantity} [RPODUCER]{self.producer_name}"    


class Ordered():
    def __init__(self, buy_order_id, sell_order_id, stock_name, price, quantity, producer_name):
        self.buy_order_id = buy_order_id
        self.sell_order_id = sell_order_id
        self.stock_name = stock_name
        self.price = price
        self.quantity = quantity
        self.producer_name = producer_name

    def info(self):
        return {
        'buy_order_id': self.buy_order_id,
        'sell_order_id': self.sell_order_id,
        'stock_name': self.stock_name,
        'price': self.price,
        'quantity': self.quantity,
        'producer_name': self.producer_name
    }

    def __str__(self):
        return f"'sell_order_id':{self.sell_order_id},'buy_order_id':{self.buy_order_id},'stock_name':{self.stock_name},'price':{self.price},'quantity':{self.quantity},'producer':{self.producer_name}"    

class OrderManager:
    def __init__(self):
        self.buy_orders = []  # 存储买单
        self.sell_orders = []  # 存储卖单
        self.ordered_orders = [] # 成交结果
        self.lock = threading.Lock() # 添加线程锁
        self.condition = threading.Condition(self.lock) # 添加条件变量


    def __str__(self):
        string = ""
        for order in self.buy_orders:
            string += str(order)

        for order in self.sell_orders:
            print(order)
            string += str(order)

        return string
    
    def add_order(self, order):
        with self.lock: # 对临界区代码添加线程锁
            if order.order_type == 'buy':
                self.buy_orders.append(order)
            elif order.order_type == 'sell':
                self.sell_orders.append(order)
            self.condition.notify_all() # 通知所有等待条件变量的线程

    def match_orders(self):
        # match from buy_order
        while len(self.buy_orders) > 0 and len(self.sell_orders) > 0:
            # Test Code
            # print(self.buy_orders)
            # print(self.sell_orders)
            self.buy_orders.sort(key=lambda o: o.price)
            buy_order = self.buy_orders[-1]
            sell_order = self.sell_orders.sort(key=lambda o: o.price)
            sell_order = self.sell_orders[0]
            if buy_order.price == sell_order.price:
                trade_quantity = min(buy_order.quantity, sell_order.quantity)
                # Message Code
                print(f"[DEAL]{buy_order.order_id} [BUY-IN]{sell_order.stock_name} [QUANTITY]{trade_quantity} [PRICE]{sell_order.price}")
                print(f"[DAEL]{sell_order.order_id} [SELL-OUT]{sell_order.stock_name} [QUANTITY]{trade_quantity} [PRICE]{sell_order.price}")
                if len(self.ordered_orders) > 500:
                    self.ordered_orders.pop(0)
                self.ordered_orders.append(Ordered(buy_order.order_id, sell_order.order_id, buy_order.stock_name, buy_order.price, trade_quantity, buy_order.producer_name))
                buy_order.quantity -= trade_quantity
                sell_order.quantity -= trade_quantity
                # change orders
                if buy_order.quantity == 0:
                    self.buy_orders.remove(buy_order)
                if sell_order.quantity == 0:
                    self.sell_orders.remove(sell_order)
            else:
                return

    def wait_for_orders(self):
        while True:
            with self.lock: # 对临界区代码添加线程锁
                if len(self.buy_orders) == 0 or len(self.sell_orders) == 0:
                    print("WAITTING ORDER...")
                    self.condition.wait() # 等待条件变量被通知
                else:
                    self.match_orders()
                    self.condition.notify_all() # 通知所有等待条件变量的线程
            # release lock

    # 异步成交函数，返回成交数据

class OrderProducer(threading.Thread):
    def __init__(self, order_manager, order_type, stock_name, price, quantity, producer_name):
        super().__init__()
        self.order_manager = order_manager
        self.producer_name = producer_name
        self.order_type = order_type
        self.stock_name = stock_name
        self.price = price
        self.quantity = quantity
        # md5 hash code : SRC-STRING = str(timestamp * 100) + producer_name 
        m = hashlib.md5()
        m.update((str(int(time.time() * 100)) + self.producer_name).encode("utf-8"))
        self.order_id = m.hexdigest()

        # thread control

    def run(self):
        order = Order(self.order_type, self.order_id, self.stock_name, self.price, self.quantity, self.producer_name)
        self.order_manager.add_order(order)

class OrderConsumer(threading.Thread):
    def __init__(self, order_manager):
        super().__init__()
        self.order_manager = order_manager

    def run(self):
        self.order_manager.wait_for_orders()