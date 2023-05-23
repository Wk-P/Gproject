from webexchange.views.common.utils import *

class walletadd(View):
    def post(self, request, **kwargs):
        response = {'alert': None}
        data = json.loads(request.body.decode())

        username = data['username']
        wallet_ID = data['wallet_ID']

        user = get_exchange_user(user_name=username)

        check = User_Wallet.objects.filter(wallet_ID=wallet_ID)

        if not check.exists():
            User_Wallet(wallet_ID=wallet_ID, user_ID=user.user_ID).save()
            default_coins = [
                'BitCoin', "Ethereum", 'Tether', 'BNB', 'USD Coin', 'XRP', 'Cardano', 'Dogecoin',
                'Polygon', 'Solana', 'TRON', 'Litecoin', 'Shiba Inu'
            ]
            coin_number = randint(1, len(default_coins))
            if coin_number > 0:
                for i in range(coin_number):
                    coin_amount = randint(1, 20)
                    User_Asset(userid=user.user_ID, wallet_ID=wallet_ID, chain="ETH", symbol=default_coins[i], amount=coin_amount).save()
            response['alert'] = 'success'
            response['wallet_ID'] = wallet_ID
        else:
            response['alert'] = 'Wallet has existed!'
        return JsonResponse(response)