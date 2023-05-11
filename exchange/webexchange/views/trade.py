from webexchange.views.common.utils import *

async def price_fetch():
    async with websockets.connect('wss://stream.binance.com:9443/ws/btcusdt@kline_1s') as ws:
        while True:
            # 接收响应数据
            response = await ws.recv()
            # 判断数据是否为完整的 JSON 字符串
            try:
                response_data.append(json.loads(response))
            except json.JSONDecodeError:
                # 如果不是完整的 JSON 字符串，继续接收数据并拼接
                continue
            # 延时 1 秒，避免 CPU 过高
            await asyncio.sleep(1)

def asyncloop():
    asyncio.get_event_loop().run_until_complete(price_fetch())

# price matching    
order_manager = OrderManager()
consumer = OrderConsumer(order_manager=order_manager)
consumer.start()

# websocket -> price fetching
response_data = []
socket = threading.Thread(target=asyncloop, args=(response_data))
socket.start()


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
                order_manager=order_manager, order_type=data['type'], stock_name=data['stockname'], price=data['price'], quantity=data['quantity'])
            producer.start()
            producer.join()
            response['alert'] = f"{data['type']} 提交成功!"

        if 'match' in data['reqtype']:
            # 返回异步成交数据
            if len(order_manager.ordered_orders) > 0:
                response['orderd'] = order_manager.ordered_orders

        return JsonResponse(response)
