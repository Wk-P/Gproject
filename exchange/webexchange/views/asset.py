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
            
            if wallets is None:
                response['alert'] = "No Wallet Data"
                return JsonResponse(response)
            
            for wallet in wallets:
                asset_data = fetch_assets_data(user, wallet)
                res_data.append(asset_data)
            
            response['asset_data'] = res_data
            return JsonResponse(response)
        else:
            return JsonResponse(response)