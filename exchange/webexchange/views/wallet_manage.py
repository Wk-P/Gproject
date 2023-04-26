from webexchange.views.common.utils import *

class wallet(View):
    def get(self, request, **kwargs):
        username = kwargs.get('username')
        if username != "":
            return render(request, 'wallet.html', context={'username': username})
        else:
            return redirect('404')
        
    def post(self, request, **kwargs):
        response = {'alert': None}
        data = json.loads(request.body.decode('utf-8'))
        username = data['username']
        user = get_user(user_name=username)
        if data['register'] == 'yes':
            # register wallet to user
            wallet_ID = data['wallet_ID']
            if add_wallet(user, wallet_ID) is not None:
                response['register'] = 'success'
            else:
                response['register'] = 'failed'
        elif data['register'] == 'no':
            wallets_data = fetch_wallets_data(user=user)
            response['wallets_data'] = wallets_data
        return JsonResponse(response)