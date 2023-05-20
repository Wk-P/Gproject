from webexchange.views.common.utils import *

class wallet(View):
    def get(self, request, **kwargs):
        username = kwargs.get('username')
        userid = get_exchange_user(user_name=username).user_ID
        return render(request, 'wallet.html', context={'username': username, 'userid': userid})
    
    def post(self, request, **kwargs):
        response = {'alert': None}
        data = json.loads(request.body.decode())

        username = data['username']
        user = get_exchange_user(user_name=username)
        
        response['asset_data'] = []

        # get private assets
        
        asset_data = User_Asset.objects.filter(userid=user.user_ID)
        if asset_data.exists():
            for ad in asset_data:
                d = {
                    "wallet_ID": ad.wallet_ID,
                    "symbol": ad.symbol,
                    "chain": ad.chain,
                    "amount": ad.amount
                }
                response['asset_data'].append(d)
            response['alert'] = 'success'
        else:
            response['alert'] = None
            response['asset_data'] = None

        return JsonResponse(response)