from ..views import *
name_pattern = r'^[A-Za-z]+.*'
password_pattern = r'.*\s+.*'

# def hash_encrypt(string):
#     hash_obj = hashlib.md5()
#     hash_obj.update(string.encode('utf-8'))
#     return hash_obj.hexdigest()


# register
class register(View):
    def get(self, request):
        return render(request, 'register.html', {'count': str(User.objects.all().count())})
    
    def post(self, request):
        if 'submit' in request.POST:
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

                user = User(user_ID=user_ID, 
                    user_name=username, 
                    user_password=hash_password, 
                    user_create_date=timezone.now())
                user.save()
                

                 # default generate wallet and BTC coin amount
            
                random.seed(time.time())
                rnum = random.randint(0, 5000)

                # wallet generate
                wallet_ID = hash_encrypt(str(rnum)+username)
                wallet_create_date=timezone.now()
                wallet = Wallets(wallet_ID=wallet_ID, 
                        user=user,
                        wallet_create_date=wallet_create_date)
                wallet.save()
                
                # BTC coin amount generate
                asset_amount = 10314.5
                asset_type = 'BTC'
                Asset(wallet=wallet, asset_type=asset_type, 
                    asset_amount=asset_amount).save()

            msg['count'] = str(User.objects.all().count())
            return render(request, 'register.html', msg)
        
        elif 'cancel' in request.POST:
            return redirect(reverse('index'))
        
        # add wallet and coin
        else:
            return render(request, 'register.html')