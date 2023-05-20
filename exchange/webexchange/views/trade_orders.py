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

        # Return async finished orders of this user
        if len(order_manager.ordered_orders) > 0:
            order_list = []
            for o in order_manager.ordered_orders:
                if o.producer_name == data['username']:
                    order_list.append(o.info())
            
            response['ordered'] = order_list
        else:
            response['ordered'] = []
        print(response)
        return JsonResponse(response)
