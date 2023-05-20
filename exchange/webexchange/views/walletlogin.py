from webexchange.views.common.utils import *

class walletlogin(View):
    def get(self, request, **kwargs):
        return render(request, 'walletlogin.html')
    
    def post(self, request, **kwargs):
        response = {'alert': None}
        data = json.loads(request.body.decode())

        username = data['username']
        password_hash = hash_encrypt(data['password'])

        user = get_exchange_user(user_name=username)
        if user is not None and user.user_password == password_hash:
            response['alert'] = 'success'
        else:
            response['alert'] = 'Login Failed!\nPlease check password and user name!'
        return JsonResponse(response)

    