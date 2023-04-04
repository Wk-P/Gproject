from common.utils import *

# login
class login(View):

    def get(self, request):
        return render(request, 'login.html')
    
    def post(self, request):
        if 'submit' in request.POST:
            # get username and userpassword
            username_input = request.POST.get('username')
            userpassword_input = request.POST.get('userpassword')

            msg = login_input_check(username_input, userpassword_input)
            if msg['type'] == '0':
                return redirect(reverse('main', kwargs={'username': username_input}), context=msg)
            else:
                return render(request, 'login.html', msg)
        
        elif 'cancel' in request.POST:
            return redirect(reverse('index'))
        
        else:
            return render(request, 'login.html')