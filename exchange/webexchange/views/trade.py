from webexchange.views.common.utils import *

# price matching    
order_manager = OrderManager()
consumer = OrderConsumer(order_manager=order_manager)
consumer.start()

# views request handle
class trade(View):
    async def get(self, request, **kwargs):
        username = kwargs.get('username')
        return render(request, 'trade.html', context={'username': username})

    async def post(self, request, **kwargs):
        response = {'alert': None}
        data = json.loads(request.body.decode('utf-8'))

        if 'trade' in data['reqtype']:
            producer = OrderProducer(
                order_manager=order_manager, order_type=data['order']['type'], 
                stock_name=data['order']['stockname'], 
                price=data['order']['price'], 
                quantity=data['order']['quantity']
            )
            producer.start()
            producer.join()
            response['alert'] = f"{data['order']['type']} 提交成功!"

        if 'match' in data['reqtype']:
            # 返回异步成交数据
            if len(order_manager.ordered_orders) > 0:
                response['orderd'] = order_manager.ordered_orders

        return JsonResponse(response)
