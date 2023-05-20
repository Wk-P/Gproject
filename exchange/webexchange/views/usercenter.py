from webexchange.views.common.utils import *

# usercenter/usercenter
class usercenter(View):
    def get(self, request, **kwargs):
        username = kwargs.get('username')
        user = get_exchange_user(user_name=username)
        user_data = get_exchange_user_data(user)
        '''
            user_data = {
                'user_name': user_name,
                'user_ID': user_ID,
                'assets': [{
                    'asset_amount': asset_amount,
                    'asset_type': asset_type,
                }]
            }
        '''
        if database_match(user_name=username) is not None:
            return render(request, 'usercenter.html', context={'username': username, 'user_data': user_data})
        else:
            return redirect('404')
        
    def post(self, request, **kwargs):
        response = {'alert': None}
        
        data = json.loads(request.body.decode('utf-8'))

        username=data['username']
        user = get_exchange_user(user_name=data['username'])

        if user is not None:
            user_data = get_exchange_user_data(user)
            '''
                user_data = {
                    'user_name': user_name,
                    'user_ID': user_ID,
                    'assets': {[
                        'asset_amount': asset_amount,
                        'asset_type': asset_type,
                    ]},
                }
            '''
            history = get_exchange_trade_history(data['username'])
            response['trade_history'] = []

            if history is None:
                response['alert'] = None
                response['trade_history'] = None
            else:
                for h in history:
                    response['trade_history'].append(
                        {"action": h.action, "user_ID": h.user_ID, 
                        "in_wallet": h.in_wallet_ID, "out_wallet": h.out_wallet_ID,
                        "time_stamp": h.time_point, "chain":h.chain, 
                        "asset_type": h.symbol, "asset_amount": h.amount}
                        )
                if database_match(user_name=data['username']) is not None:
                    response['alert'] = 'success'
                    response['user_data'] = user_data
        else:
            response['alert'] = "No User Data"
        return JsonResponse(response)