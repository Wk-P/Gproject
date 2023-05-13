from webexchange.views.common.utils import *

trades_redata = []
prices_redata = []

async def fetch_prices_data(coin_list):
    global prices_redata
    uri_prices = "wss://ws.coincap.io/prices?assets=" + ','.join(coin_list)
    async with websockets.connect(uri_prices) as websocket_prices:
        try:
            response = await websocket_prices.recv()
            if len(prices_redata) > 300:
                prices_redata = []
            prices_redata.append(json.loads(response))
        except websockets.exceptions.ConnectionClosed as e:
            print(f"Error: {e}. Closing websocket connection...")
            await websocket_prices.close()


async def fetch_trades_data():
    global trades_redata
    uri_trades = "wss://ws.coincap.io/trades/binance"
    async with websockets.connect(uri_trades) as websocket_trades:
        try:
            response = await websocket_trades.recv()
            if len(trades_redata) > 300:
                trades_redata = []
            trades_redata.append(json.loads(response))
        except websockets.exceptions.ConnectionClosed as e:
            print(f"Error: {e}. Closing websocket connection...")
            await websocket_trades.close()
        except Exception as e:
            print(f"Unhandled exception: {e}")
            raise

async def fetch_coins_information():
    global prices_redata
    global trades_redata
    coin_list = []
    url = 'https://api.coincap.io/v2/assets'
    coin_data = json.loads(requests.get(url).content)['data']
    for i in range(20):
        coin_list.append(coin_data[i]['id'])

    await fetch_prices_data(coin_list)
    await fetch_trades_data()

    return {
        'prices-data': prices_redata[-1],
        'trades-data': trades_redata[-1],
        'assets-data': coin_data,
    }


class coins_websocket(View):
    async def post(self, request):
        response = {'alert': None}
        try:
            response_data = await fetch_coins_information()
            response['prices-data'] = response_data['prices-data']
            response['trades-data'] = response_data['trades-data']
            response['assets-data'] = response_data['assets-data']
            return JsonResponse(response)
        except Exception as e:
            return JsonResponse({'error': str(e)})
