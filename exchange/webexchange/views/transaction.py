from webexchange.views.common.utils import *

class transaction(View):
    def get(self, request, **kwargs):
        username = kwargs.get('username')
        user = get_exchange_user(user_name=username)
        wallet = get_exchange_wallet(user=user)
        return render(request, 'transaction.html', context={'username': username, 'wallet_address': wallet.exchange_wallet_ID})
        
    def post(self, request, **kwargs):
        response = {'alert': None}
        data = json.loads(request.body.decode('utf-8'))
        
        send_wallet_ID = data['send_out_wallet_address']
        recv_wallet_ID = data['send_in_wallet_address']
        username = data['username']
        user = get_exchange_user(user_name=username)
        exchange_wallet = get_exchange_wallet(user=user)

        # int -> float
        data['amount'] = float(data['amount'])

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
                        a.asset_amount = float(a.asset_amount) - data['amount']
                        a.save()
                        update = True
                        break
                    else:
                        response['alert'] = "Error: Amount not enough"
                        break
            if update == False:
                response['alert'] = "Wrong Coin Symbol or Chain or Amount not Enough"
                return JsonResponse(response)
            # receive wallet
            ew = get_exchange_wallet(wallet_ID=recv_wallet_ID)
            uw = get_user_private_wallet(wallet_ID=recv_wallet_ID)
            # ew or uw one is True
            if (ew == None) ^ (uw == None):

                # send asset to exchange's wallet
                if ew == None:
                    asset = get_user_private_asset(username, uw.wallet_ID, data['symbol'], data['chain'])
                    if asset is not None:
                        asset.amount = float(asset.amount) + data['amount']
                        asset.save()
                        response['alert'] = 'success'
                    else:
                        User_Asset(wallet_ID=uw.wallet_ID, userid=user.user_ID, symbol=data['symbol'], chain=data['chain'], amount=data['amount']).save()
                        return JsonResponse(response)
                    
                # send asset to user's wallet
                else:
                    exchange_asset = get_exchange_assets(user)
                    if exchange_asset is not None:
                        update = False
                        for ea in exchange_asset:
                            if ea.asset_type == data['symbol'] and ea.chain == data['chain']:
                                ea.asset_amount = float(ea.asset_amount) + data['amount']
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
                add_exchange_trade_history(username=username, out_wallet=send_wallet_ID, in_wallet=recv_wallet_ID, amount=data['amount'], asset_type=data['symbol'], action="out", chain=data['chain'])
            else:
                response['alert'] = "Wrong Wallet Address"
        # send from exchange wallet
        # only exchange wallet address is anabled to us
        else:
            if recv_wallet_ID == exchange_wallet.exchange_wallet_ID:
                assets = get_exchange_assets(user)
                # assets record don't exsist
                if assets is None:
                    add_exchange_asset(user, data['chain'], data['symbol'], data['amount'])
                # assets record exists
                else:
                    update = False
                    for a in assets:
                        if a.asset_type == data['symbol'] and a.chain == data['chain']:
                            a.asset_amount = float(a.asset_amount) + data['amount']
                            a.save()
                            
                            update = True
                            break
                    if update == False:
                        add_exchange_asset(user, data['chain'], data['symbol'], data['amount'])
                
                response['alert'] = 'success'
            else:
                check = User_Wallet.objects.filter(wallet_ID=recv_wallet_ID)
                if check.exists():
                    wallet = check.first()
                    check_a = User_Asset.objects.filter(wallet_ID=wallet.wallet_ID, symbol=data['symbol'], chain=data['chain'])
                    if check_a.exists():
                        check_a.first().amount = float(check_a.first().amount) + data['amount']
                    else:
                        User_Asset(wallet_ID=wallet.wallet_ID, symbol=data['symbol'], chain=data['chain'], amount=data['amount']).save()

                response['alert'] = 'success'

            add_exchange_trade_history(username=username, out_wallet=send_wallet_ID, in_wallet=recv_wallet_ID, amount=data['amount'], asset_type=data['symbol'], action="out", chain=data['chain'])
        return JsonResponse(response)