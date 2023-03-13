from ..views import *

# usercenter/usercenter
class usercenter(View):
    def get(self, request, **kwargs):
        username = kwargs.get('username')

        if username_check(username):
            user_data = get_user_data(username)
            print(user_data)
            return render(request, 'usercenter.html', context={'username': username, 'user_data': user_data})
        else:
            return redirect('404')
    def post(self, request):
        return render(request, 'usercenter.html')