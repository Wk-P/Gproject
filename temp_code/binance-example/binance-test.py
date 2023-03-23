from binance.spot import Spot

# Spot : account(账号)

def test1():
    client = Spot()

    # Get server timestamp
    print(client.time())
    # Get klines of BTCUSDT at 1m interval
    print(client.klines("BTCUSDT", "1m"))
    # Get last 10 klines of BNBUSDT at 1h interval
    print(client.klines("BNBUSDT", "1h", limit=10))

    # API key/secret are required for user data endpoints
    client = Spot(api_key='<api_key>', api_secret='<api_secret>')

    # Get account and balance information
    # print(client.account())

    # Post a new order
    params = {
        'symbol': 'BTCUSDT',
        'side': 'SELL',
        'type': 'LIMIT',
        'timeInForce': 'GTC',
        'quantity': 0.002,
        'price': 9500
    }

    # response = client.new_order(**params)
    # print(response)

if __name__ == "__main__":
    test1()