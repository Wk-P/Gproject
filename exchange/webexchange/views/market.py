from webexchange.views.common.utils import *

def toJson(string):
    return json.loads(string)

def fetch_prices_data(coin_list):
    uri_prices = "wss://ws.coincap.io/prices?assets=" + ','.join(coin_list)
    async def fetch_data():
        async with websockets.connect(uri_prices) as websocket_prices:
            try:
                prices_redata = await websocket_prices.recv()
                prices_redata = toJson(prices_redata)
                return prices_redata
            except websockets.exceptions.ConnectionClosed as e:
                print(f"Error: {e}. Closing websocket connection...")
                await websocket_prices.close()
                return None
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        prices_data = loop.run_until_complete(fetch_data())
        return prices_data
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()

def fetch_trades_data():
    uri_trades = "wss://ws.coincap.io/trades/binance"
    async def fetch_data():
        async with websockets.connect(uri_trades) as websocket_trades:
            try:
                trades_redata = await websocket_trades.recv()
                trades_redata = toJson(trades_redata)
                return trades_redata
            except websockets.exceptions.ConnectionClosed as e:
                print(f"Error: {e}. Closing websocket connection...")
                await websocket_trades.close()
                return None
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        trades_data = loop.run_until_complete(fetch_data())
        return trades_data
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()

def fetch_market_information():
    coin_list = []
    url = 'https://api.coincap.io/v2/assets'
    coin_data = toJson(requests.request("GET", url).content)['data']
    for i in range(20):
        coin_list.append(coin_data[i]['id'])

    prices_data = fetch_prices_data(coin_list)
    trades_data = fetch_trades_data()

    response_data = {}
    response_data['assets_data'] = coin_data
    response_data['prices-data'] = prices_data
    response_data['trades-data'] = trades_data

    return response_data

class market(View):
    def get(self, request):
        return render(request, 'market.html')

    def post(self, request):
        try:
            response_data = fetch_market_information()
            return JsonResponse(response_data)
        except Exception as e:
            return JsonResponse({'error': str(e)})
