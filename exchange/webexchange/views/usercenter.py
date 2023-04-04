from webexchange.views.common.utils import *

# usercenter/usercenter
class usercenter(View):
    def get(self, request, **kwargs):
        username = kwargs.get('username')

        user_data = get_user_data(username)
        '''
            user_data = {
                'user_name': user_name,
                'user_ID': user_ID,
                'assets': {[
                    'wallet_ID': wallet_ID,
                    'asset_amount': asset_amount,
                    'asset_type': asset_type,
                ]}
            }
        '''
        if username_check(username):
            return render(request, 'usercenter.html', context={'username': username, 'user_data': user_data})
        else:
            return redirect('404')
    def post(self, request):
        return render(request, 'usercenter.html')