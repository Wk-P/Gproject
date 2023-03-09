from ..views import *

# usercenter/asset
class asset(View):
    def get(self, request, **kwargs):
        username = kwargs.get('username')
        if username_check(username):
            return render(request, 'asset.html', {'username': username})
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
            amount = request.POST.get('amount')
            coin_type = request.POST.get('coin_type')
            if get_verification_information(username):
                print("Yes")
                return render(request, 'asset.html')
            else:
                return redirect('404')
            # get user asset data from database
            '''
            # 验证函数: 用户名和钱包数据
            # verify(name, wallet):
            #   ...
            #   return data
            '''

            
        # 从验证函数中拿到数据返回前端 
        # if status == ok:
            # self.response_data = {
            #     'status': 'ok',
            #     'status': '
            # }

