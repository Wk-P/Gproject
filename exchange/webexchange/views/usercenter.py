from webexchange.views.common.utils import *

# usercenter/usercenter
class usercenter(View):
    def get(self, request, **kwargs):
        username = kwargs.get('username')
        user = get_user(user_name=username)
        user_data = get_exchange_user_data(user)
        '''
            user_data = {
                'user_name': user_name,
                'user_ID': user_ID,
                'assets': {[
                    'asset_amount': asset_amount,
                    'asset_type': asset_type,
                ]}
            }
        '''
        if database_match(user_name=username) is not None:
            return render(request, 'usercenter.html', context={'username': username, 'user_data': user_data})
        else:
            return redirect('404')
        
    def post(self, request, **kwargs):
        response = {'alert': None}
        
        data = json.loads(request.body.decode('utf-8'))

        user = get_user(user_name=data['username'])
        user_data = get_exchange_user_data(user)
        '''
            user_data = {
                'user_name': user_name,
                'user_ID': user_ID,
                'assets': {[
                    'asset_amount': asset_amount,
                    'asset_type': asset_type,
                ]}
            }
        '''
        trade_data = get_trade_history(data['username'])
        if database_match(user_name=data['username']) is not None:
            response['alert'] = 'success'
            response['user_data'] = user_data
            response['trade_data'] = trade_data
        return JsonResponse(response)