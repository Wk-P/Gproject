from ..views import *

# usercenter/usercenter
class usercenter(View):
    def get(self, request, **kwargs):
        username = kwargs.get('username')
        if username_check(username):
            return render(request, 'usercenter.html', context={'username': username})
        else:
            return redirect('404')
    def post(self, request):
        return render(request, 'usercenter.html')