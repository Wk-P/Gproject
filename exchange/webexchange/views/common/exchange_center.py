import threading
import time

class Order:
    def __init__(self, order_type, order_id, stock_name, price, quantity):
        self.order_type = order_type  # 订单类型，buy 或 sell
        self.order_id = order_id  # 订单编号
        self.stock_name = stock_name  # 股票名称
        self.price = price  # 订单价格
        self.quantity = quantity  # 订单数量

    def __str__(self):
        return f"\n订单类型: {self.order_type},订单ID: {self.order_id},股票名称: {self.stock_name},价格: {self.price},数量: {self.quantity}\n"


class Ordered():
    def __init__(self, order_id, stock_name, price, quantity):
        self.order_id = order_id
        self.stock_name = stock_name
        self.price = price
        self.quantity = quantity

    def __str__(self):
        return f"\n订单ID:{self.order_id},股票名称:{self.stock_name},价格:{self.price},数量:{self.quantity}\n"    
    

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
            buy_order = sorted(self.buy_orders, key=lambda o: o.price)[-1]
            sell_order = sorted(self.sell_orders, key=lambda o: o.price)[0]
            if buy_order.price == sell_order.price:
                trade_quantity = min(buy_order.quantity, sell_order.quantity)
                print(f"成交：{buy_order.order_id} 买入 {sell_order.stock_name} {trade_quantity} 股，单价 {sell_order.price}")
                print(f"成交：{sell_order.order_id} 卖出 {sell_order.stock_name} {trade_quantity} 股，单价 {sell_order.price}")
                print("-----------")
                self.ordered_orders.append(Ordered((buy_order.order_id + sell_order.order_id), buy_order.stock_name, buy_order.price, trade_quantity))
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
    def __init__(self, order_manager, order_type, stock_name, price, quantity):
        super().__init__()
        self.order_manager = order_manager
        self.order_type = order_type
        self.stock_name = stock_name
        self.price = price
        self.quantity = quantity

    def run(self):
        order = Order(self.order_type, self.name, self.stock_name, self.price, self.quantity)
        self.order_manager.add_order(order)
        print(f"提交订单：{order.order_id} {order.order_type} {order.stock_name} {order.quantity} 股，单价 {order.price}")


class OrderConsumer(threading.Thread):
    def __init__(self, order_manager):
        super().__init__()
        self.order_manager = order_manager

    def run(self):
        self.order_manager.wait_for_orders()



# order_manager = OrderManager()
# order_consumer = OrderConsumer(order_manager)
# order_consumer.start()

# if __name__ == "__main__":


    
    # while True:
    #     try:
    #         order_producer1 = OrderProducer(order_manager, 'buy', 'ABC', 10, 100)
    #         order_producer2 = OrderProducer(order_manager, 'sell', 'ABC', 10, 50)
    #         order_producer3 = OrderProducer(order_manager, 'sell', 'ABC', 10, 50)
    #         order_producer1.start()
    #         order_producer2.start()
    #         order_producer3.start()
    #         # order_producer3 = OrderProducer(order_manager, 'sell', 'ABC', 10, 50)
    #         # order_producer4 = OrderProducer(order_manager, 'sell', 'ABC', 10, 50)
    #         # order_producer5 = OrderProducer(order_manager, 'buy', 'ABC', 10, 50)

    #         # order_producer4.start()
    #         # order_producer5.start()
            
    #         order_producer1.join()
    #         order_producer2.join()
    #         order_producer3.join()
    #         # order_producer4.join()
    #         # order_producer5.join()

    #         time.sleep(1)
    #     except:
    #         print("Exception!")
    #         time.sleep(100)
    #         continue