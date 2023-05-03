from webexchange.views.common.utils import *

class wallet(View):
    def get(self, request, **kwargs):
        username = kwargs.get('username')
        return render(request, 'wallet.html', context={'username': username})
    
    def post(self, request, **kwargs):
        username = kwargs.get('username')
        user = get_user(username=username)

    