from . import *

# check user name and password
def login_input_check(username, password):
    user_table = User.objects
    '''
        @type:
            0: Success
            1: Invalid input
            2: Password input wrong
            3: User not exists
    '''
    msg = {
        'alert': None,
        'type': None,
    }
    # check input weather valid
    if username == "" or password == "":
        msg['alert'] = 'Invalid Input!'
        msg['type'] = '1'
    else:
        try:
            # check user name weather already exist
            user_table.get(user_name=username)
            if password == user_table.get(user_name=username).user_password:
                msg['alert'] = "Login successfully!"
                msg['type'] = '0'
            else:
                msg['alert'] = 'Password input wrong!'
                msg['type'] = '2'
        except:
            # User not exists
            msg['alert'] = 'User not exists'
            msg['type'] = '3'
        else:
            return msg
    return msg

# login
class login(View):
    def get(self, request):
        return render(request, 'login.html')
    
    def post(self, request):
        # get username and userpassword
        username_input = request.POST.get('username')
        userpassword_input = request.POST.get('userpassword')

        msg = login_input_check(username_input, userpassword_input)
        if msg['type'] == '0':
            return render(request, 'login.html', msg)

        return render(request, 'login.html')