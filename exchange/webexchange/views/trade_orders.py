from webexchange.views.common.utils import *

# price matching
order_manager = OrderManager()
consumer = OrderConsumer(order_manager=order_manager)
consumer.start()

class trade_orders(View):
    async def post(self, request, **kwargs):
        response = {'alert': None}
        data = json.loads(request.body.decode('utf-8'))
        # receive ordered
        if data['reqtype'] == 'trade':
            producer = OrderProducer(
                order_manager=order_manager, order_type=data['order']['type'], 
                stock_name=data['order']['stockname'], 
                price=data['order']['price'], 
                quantity=data['order']['quantity'],
                producer_name=data['username']
            )
            producer.start()
            producer.join()
            response['alert'] = f"{data['order']['type']} 提交成功!"
        
        
        ordered_list = []
        buy_orders_list = []
        sell_orders_list = []
        
        # buy orders
        if len(order_manager.buy_orders) > 0:
            for o in order_manager.buy_orders:
                buy_orders_list.append(o.info())
            
            response['buy_orders'] = buy_orders_list  
        else:
            response['buy_orders'] = []

        # sell orders
        if len(order_manager.sell_orders) > 0:
            for o in order_manager.sell_orders:
                sell_orders_list.append(o.info())
            
            response['sell_orders'] = sell_orders_list
        else:
            response['sell_orders'] = []

        # async finished orders of this user
        if len(order_manager.ordered_orders) > 0:
            for o in order_manager.ordered_orders:
                ordered_list.append(o.info())
            
            response['ordered'] = ordered_list
        else:
            response['ordered'] = []
        return JsonResponse(response)
