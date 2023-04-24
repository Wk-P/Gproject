from webexchange.views.common.utils import *

# login
class login(View):

    def get(self, request):
        return render(request, 'login.html')
    
    def post(self, request):
        """ Submit button
            Check input and match data with database """
        
        response = {'alert': None}
        data = json.loads(request.body.decode('utf-8'))

        if data.get('click') == "submit":
            # fetch input
            username = data.get('username')
            userpassword = data.get('userpassword')
            # checking
            if is_empty_input(username) or is_empty_input(userpassword):
                response['alert'] = "Empty Input!"
                return JsonResponse(response)
            
            if is_wrong_format_input(username, "name") or is_wrong_format_input(userpassword, "password"):
                response['alert'] = "Invalid Input!"
                return JsonResponse(response)
            
            # checking pass 
            db_data = database_match({'user_name': username})
            if db_data is None:
                response['alert'] = 'Data Matching Failed!'
            else:
            # Login password check
                userpassword = hash_encrypt(userpassword)   # plaintext to ciph
                if db_data.user_password != userpassword:
                    response['alert'] = 'Wrong Password!'
                else:
                    response['alert'] = 'success'
                    response['username'] = username
            return JsonResponse(response)
        
        elif data.get('click') == "cancel":
            response['alert'] = None
            return JsonResponse(response)
        elif data.get('click') == 'register':
            response['alert'] = None
            return JsonResponse(response)
        else:
            response['alert'] = "Page Wrong!"
            return JsonResponse(response)
        