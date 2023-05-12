from webexchange.views.common.utils import *

class walletlogin(View):
    def get(self, request, **kwargs):
        return render(request, 'walletlogin.html')
    
    def post(self, request, **kwargs):
        username = kwargs.get('username')
        user = get_user(username=username)

    