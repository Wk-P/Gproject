from webexchange.views.common.utils import *

async def price_fetch():
    global response_data
    async with websockets.connect('wss://stream.binance.com:9443/ws/btcusdt@kline_1s') as ws:
        while True:
            # 接收响应数据
            response = await ws.recv()
            # 判断数据是否为完整的 JSON 字符串
            try:
                if len(response_data) > 50:
                    response_data = []
                response_data.append(json.loads(response))
            except json.JSONDecodeError as e:
                continue
            # 延时 1 秒，避免 CPU 过高
            await asyncio.sleep(1)

async def asyncloop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    await price_fetch()
    loop.close()

response_data = []

t = threading.Thread(target=asyncio.run, args=(asyncloop(), ))
t.start()

class trade_websocket(View):
    async def post(self, request, **kwargs):
        response = {'alert': None}
        
        if len(response_data) > 0:
            response['price_data'] = response_data[-1]
        else:
            response['price_data'] = []
        return JsonResponse(response)
