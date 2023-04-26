from webexchange.views.common.utils import *

# usercenter/asset
class asset(View):
    def get(self, request, **kwargs):
        username = kwargs.get('username')

        user_data = get_user_data(username)

        if database_match(user_name=username) is not None:
            return render(request, 'asset.html', {'username': username, 'user_data': user_data})
        else:
            return redirect('404')
        
    def post(self, request, **kwargs):
        
        response = {'alert': None}
        res_data = []
        data = json.loads(request.body.decode('utf-8'))
        if data['click'] == "no":
            user = get_user(user_name=data['username'])
            wallets = get_wallets(user)
            wallets_id = []
            if wallets is None:
                response['alert'] = "No Wallet Data"
                return JsonResponse(response)
            
            for wallet in wallets:
                wallets_id.append(wallet.wallet_ID)
                asset_data = fetch_assets_data(data['username'], wallet)
                if asset_data is not None:
                    res_data.append(asset_data)
            # res_data == [None]
            response['wallet_id'] = wallets_id
            if len(res_data) > 0:
                # valid data
                response['alert'] = 'success'
                response['asset_data'] = res_data
            else:
                response['alert'] = 'incomplete'
                response['asset_data'] = None
        return JsonResponse(response)