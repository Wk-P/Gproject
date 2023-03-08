from ..views import *

# main
class main(View):
    def get(self, request, **kwargs):
        username = kwargs.get('username')
        return render(request, 'main.html', context={'username': username})
    
    def post(self, request):
        return render(request, 'main.html')

# index
class index(View):
    def get(self, request):
        return render(request, 'index.html')
    
    def post(self, request):
        if 'login' in request:
            return render(request, 'login.html')
        elif 'sign' in request:
            return render(request, 'register.html')
