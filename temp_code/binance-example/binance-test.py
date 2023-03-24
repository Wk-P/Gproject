from coinmarketcapapi import CoinMarketCapAPI
import json
cmc = CoinMarketCapAPI()

rep = cmc.exchange_marketpairs_latest(slug='binance', symbol='BTC, ETC', convert='CNY')


# rep = cmc.cryptocurrency_priceperformancestats_latest(symbol='BTC', convert='CNY')

for i in rep.data:
    print(i)

with open("test1.jsonl", 'w') as f:
    json.dump(rep.data, f, indent=4, ensure_ascii=False)

# print(data['market_pairs'][0], end='\n')
    
# market_pairs.quotes.quote['BTC/USD