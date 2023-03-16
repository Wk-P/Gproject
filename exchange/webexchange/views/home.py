from . import *

# main
class main(View):
    def get(self, request, **kwargs):
        username = kwargs.get('username')
        if username_check(username):
            return render(request, 'main.html', context={'username': username})
        else:
            return redirect('404')
        
    def post(self, request):
        return render(request, 'main.html')

# index
class index(View):
    def get(self, request):
        return render(request, 'index.html')
    
    def post(self, request):
        if 'login' in request.POST:
            return redirect(reverse('login'))
        elif 'sign' in request.POST:
            return redirect(reverse('register'))
        else:
            return render(request, 'index.html')
