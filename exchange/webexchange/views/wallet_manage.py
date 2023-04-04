from common.utils import *

class wallet(View):
    def get(self, request, **kwargs):
        username = kwargs.get('username')
        if username != "":
            return render(request, 'wallet.html', context={'username': username})
        else:
            return redirect('404')
        
    def post(self, request, **kwargs):
        username = kwargs.get('username')
        user_data = get_user_data(username)
        return JsonResponse(user_data)