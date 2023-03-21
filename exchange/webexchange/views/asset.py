from . import *

# usercenter/asset
class asset(View):
    def get(self, request, **kwargs):
        username = kwargs.get('username')

        user_data = get_user_data(username)

        if username_check(username):
            return render(request, 'asset.html', {'username': username, 'user_data': user_data})
        else:
            return redirect('404')
        
    def post(self, request, **kwargs):
        
        # users request amount verification and send a request data package with wallet amount from users' local (or from server)
        # 从服务器端直接验证
        # wallet data from users

        username = kwargs.get('username')
        
        if 'verify' in request.POST:
        # 从服务器端数据库中找出用户服务器的数据
        # get details wallet data from database
        # take_wallet():
        #   pass 
            # verification information
            user_data = get_user_data(username)
            information = get_verification_information(username)
            if information != None:
                
                
                
                return redirect(reverse('verifyresult', kwargs={'username': username}))
            else:
                return redirect('404')
