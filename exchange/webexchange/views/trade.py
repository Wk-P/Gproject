from webexchange.views.common.utils import *

response_data = []

async def price_fetch():
    global response_data
    async with websockets.connect('wss://stream.binance.com:9443/ws/btcusdt@kline_1s') as ws:
        while True:
            # 接收响应数据
            response = await ws.recv()
            # 判断数据是否为完整的 JSON 字符串
            try:
                response_data.append(json.loads(response))
                print(response_data)
            except json.JSONDecodeError:
                # 如果不是完整的 JSON 字符串，继续接收数据并拼接
                continue
            # 延时 1 秒，避免 CPU 过高
            await asyncio.sleep(0.2)


async def get_price():
    await asyncio.gather(price_fetch(), trade.post())

async def asyncloop():
    await asyncio.run(get_price())

# price matching
order_manager = OrderManager()
consumer = OrderConsumer(order_manager=order_manager)
consumer.start()

# websocket -> price fetching
asyncloop()
# views request handle


class trade(View):
    async def get(self, request, **kwargs):
        username = kwargs.get('username')
        return render(request, 'trade.html', context={'username': username})

    async def post(self, request, **kwargs):
        global response_data
        response = {'alert': None}
        data = json.loads(request.body.decode('utf-8'))
        if 'trade' in data['reqtype']:
            producer = OrderProducer(
                order_manager=order_manager, order_type=data['type'], stock_name=data['stockname'], price=data['price'], quantity=data['quantity'])
            producer.start()
            producer.join()
            response['alert'] = f"{data['type']} 提交成功!"


        # 返回异步成交数据
        if len(order_manager.ordered_orders) > 0:
            response['orderd'] = order_manager.ordered_orders

        if len(response_data) > 0:
            response['price_data'] = response_data[-1]
        else:
            response['price_data'] = {}

        response['alert'] = "POST"

        return JsonResponse(response)
