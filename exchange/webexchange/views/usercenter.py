from webexchange.views.common.utils import *

# usercenter/usercenter
class usercenter(View):
    def get(self, request, **kwargs):
        username = kwargs.get('username')
        user = get_user(user_name=username)
        user_data = get_user_data(user)
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
    def post(self, request):
        return render(request, 'usercenter.html')