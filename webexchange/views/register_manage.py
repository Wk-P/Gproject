from . import *
name_pattern = r'^[A-Za-z]+.*'
password_pattern = r'.*\s+.*'

def hash_encrypt(string):
    hash_obj = hashlib.md5()
    hash_obj.update(string.encode('utf-8'))
    return hash_obj.hexdigest()

# check user name and password
def register_input_check(username, password, passworda):
    user_table = User.objects
    '''
        @type:
            0: Success
            1: Invalid input
            2: Password input wrong
            3: User has existed
    '''
    msg = {
        'alert': None,
        'type': None,
    }
    # check input weather valid
    if username == "" or password == "" or passworda == "" or \
        not re.match(name_pattern, username) or \
        re.match(password_pattern, password) or \
        re.match(password_pattern, passworda):
        msg['alert'] = 'Invalid Input'
        msg['type'] = '1'
    else:
        # password input wrong
        if password != passworda:
            msg['alert'] = "Password must be same"
            msg['type'] = '2'
        else:
            # empty user table
            # anable to add new user
            if user_table.count() == 0:
                msg['alert'] = 'Register successfully'
                msg['type'] = '0'
            try:
                # check user name weather already exist
                user_table.get(user_name=username)
                msg['alert'] = 'User already exists'
                msg['type'] = '3'
            except:
                # anable to add new user
                msg['alert'] = 'Register successfully'
                msg['type'] = '0'
            else:
                return msg
    return msg

# register
class register(View):
    def get(self, request):
        return render(request, 'register.html', {'count': str(User.objects.all().count())})
    
    def post(self, request, **kwargs):
        # Add user information to database
        username = request.POST.get('username')
        userpassword = request.POST.get('userpassword')
        userpassworda = request.POST.get('userpassworda')
        # check 
        msg = register_input_check(username, userpassword, userpassworda)

        if msg['type'] == '0':
            # hash MD5 encrypt
            # username -> user_ID / userpassword -> user_password
            user_ID = hash_encrypt(username)
            hash_password = hash_encrypt(userpassword)

            User(user_ID=user_ID, 
                 user_name=username, 
                 user_password=hash_password, 
                 user_create_date=timezone.now()).save()
            
        msg['count'] = str(User.objects.all().count())
        return render(request, 'register.html', msg)
