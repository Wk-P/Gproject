from ..views import *

# usercenter/asset
class asset(View):
    def get(self, request, **kwargs):
        username = kwargs.get('username')
        return render(request, 'asset.html', {'username': username})

    def post(self, request, **kwargs):
        
        # users request amount verification and send a request data package with wallet amount from users' local (or from server)
        # 从服务器端直接验证
        username = kwargs.get('username')
        wallet = kwargs.get('wallet')
        # wallet data from users
            
        wallet_amount = kwargs.get('amount')
        # 从服务器端数据库中找出用户服务器的数据
        # get details wallet data from database
        # take_wallet():
        #   pass 

        if username_check(username):
            self.url = 'wallet.html'
            self.context['username'] = username


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
        

        else:
            self.url = '404.html'
            return render(request, self.url, self.context)
        return render(request, self.url, self.context)
        pass