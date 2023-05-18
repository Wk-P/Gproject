from webexchange.views.common.utils import *

class transaction(View):
    def get(self, request, **kwargs):
        username = kwargs.get('username')
        user = get_user(user_name=username)
        wallet = get_exchange_wallet(user=user)
        return render(request, 'transaction.html', context={'username': username, 'wallet_address': wallet.exchange_wallet_ID})
        
    def post(self, request, **kwargs):
        response = {'alert': None}
        data = json.loads(request.body.decode('utf-8'))
        
        send_wallet_ID = data['send_out_wallet_address']
        recv_wallet_ID = data['send_in_wallet_address']
        username = data['username']
        user = get_user(user_name=username)
        exchange_wallet = get_exchange_wallet(user=user)

        if send_wallet_ID == recv_wallet_ID:
            response['alert'] = "Wrong Wallet Address"
            return JsonResponse(response)
        # send from exchange
        if exchange_wallet.exchange_wallet_ID == send_wallet_ID:
            assets = get_exchange_assets(user)
            update = False
            for a in assets:
                if a.asset_type == data['symbol'] and a.chain == data['chain']:
                    if a.asset_amount >= data['amount']:
                        a.asset_amount -= data['amount']
                        a.save()
                        update = True
                        break
                    else:
                        response['alert'] = "Error: Amount not enough"
            if update == False:
                response['alert'] = "Wrong Coin Symbol or Chain"
                return JsonResponse(response)
            # receive wallet
            ew = get_exchange_wallet(wallet_ID=recv_wallet_ID)
            uw = get_user_private_wallet(recv_wallet_ID)
            # ew or uw one is True
            if (ew == None) ^ (uw == None):
                if ew == None:
                    # asset to user's private wallet
                    asset = get_user_private_asset(username, uw.wallet_ID, data['symbol'], data['chain'])
                    if asset is not None:
                        asset.asset_amount += data['amount']
                else:
                    # asset to another user's exchange wallet
                    exchange_asset = get_exchange_assets(user)
                    if exchange_asset is not None:
                        update = False
                        for ea in exchange_asset:
                            if ea.asset_type == data['symbol'] and ea.chain == data['chain']:
                                ea.asset_amount += data['amount']
                                ea.save()
                                update = True
                                break
                        if update == False:
                            response['alert'] = "Wrong Coin Symobl or Chain"
                            return JsonResponse(response)
                        # return success result
                        response['alert'] = 'success'
                    else:
                        response['alert'] = "Database Error"
            else:
                response['alert'] = "Error Wallet Address"
        # send from exchange wallet
        # only exchange wallet address is anabled to us
        else:
            if recv_wallet_ID == exchange_wallet.exchange_wallet_ID:
                assets = get_exchange_assets(user)
                if assets is None:
                    add_exchange_asset(user, data['chain'], data['symbol'], data['amount'])
                else:
                    for a in assets:
                        if a.asset_type == data['symbol'] and a.chain == data['chain']:
                            a.asset_amount += data['amount']
                            a.save()
                            break
            else:
                response['alert'] = "Wrong Wallet Address"
        return JsonResponse(response)