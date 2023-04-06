from webexchange.views.common.utils import *

# data dict
response_data = {}

def toJson(string):
    return json.loads(string)

async def fetch_data():
    uri_prices = "wss://ws.coincap.io/prices?assets=bitcoin,ethereum,litecoin"
    uri_trades = "wss://ws.coincap.io/trades/binance"
    async with websockets.connect(uri_prices) as websocket_prices:
        prices_redata = await websocket_prices.recv()
        response_data['prices-data'] = prices_redata

    async with websockets.connect(uri_trades) as websocket_trades:
        trades_redata = await websocket_trades.recv()
        trades_redata = toJson(trades_redata)
        response_data['trades-data'] = trades_redata

# market
class market(View):
    async def get(self, request):
        return render(request, 'market.html')
    
    async def post(self, request):
        loop = asyncio.get_event_loop()
        if loop.is_running():
            await fetch_data()
        else:
            await asyncio.run(fetch_data())
        
        print(response_data)
        return JsonResponse(response_data)
