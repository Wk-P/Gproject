from webexchange.views.common.utils import *

# price matching
order_manager = OrderManager()
consumer = OrderConsumer(order_manager=order_manager)
consumer.start()

def rest_amount_check(username, stockname, quantity):
    user = get_exchange_user(user_name=username)
    # only check when order type is 'sell'
    assets = get_exchange_assets(user=user)
    if assets is not None:
        # find_r -> find result number
        # trade_r -> traded flag
        find_r, trade_r = 0, 0
        for a in assets:
            if a.asset_type == stockname and a.asset_amount >= quantity and find_r < 2: 
                # find_r < 2 is for different chain
                a.asset_amount -= quantity
                a.save()
                trade_r = 1
                break
            else:
                continue
        if trade_r == 0:
            return False
        return True
    else:
        return False




class trade_orders(View):
    async def post(self, request, **kwargs):
        response = {'alert': None}
        data = json.loads(request.body.decode('utf-8'))
        # prepare for quantity check
        username = data['username']
        




        # receive ordered
        if data['reqtype'] == 'trade':
            
            stockname = data['order']['stockname']
            quantity = data['order']['quantity']
            ordertype = data['order']['type']
            price = data['order']['price']
            
            # database sync mothed
            result_event = threading.Event()
            result = None
            async def get_result():
                nonlocal result
                # await 添加
                result = rest_amount_check(username=username, stockname=stockname, quantity=quantity)
                result_event.set()

            data_base_thread = threading.Thread(target=get_result)
            data_base_thread.start()
            data_base_thread.join()


            producer = OrderProducer(
                order_manager=order_manager, 
                order_type=ordertype,
                stock_name=stockname,
                price=price, 
                quantity=quantity,
                producer_name=username
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
