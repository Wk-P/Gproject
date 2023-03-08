from ..views import *

# usercenter/usercenter
class usercenter(View):
    def get(self, request, **kwargs):
        username = kwargs.get('username')
        return render(request, 'usercenter.html', context={'username': username})
    
    def post(self, request):
        return render(request, 'usercenter.html')