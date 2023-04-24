from webexchange.views.common.utils import *

name_pattern = r'^[A-Za-z]+.*'
password_pattern = r'.*\s+.*'

# register
class register(View):

    def get(self, request):
        return render(request, 'register.html')
    
    def post(self, request):
        response = {'alert': None}
        data = json.loads(request.body.decode('utf-8'))
        if data.get('click') == "submit":
            # fetch data
            username = data.get('username')
            userpassword = data.get('userpassword')
            userpassworda = data.get('userpassworda')

            # checking
            if is_empty_input(username) or is_empty_input(userpassword):
                response['alert'] = "Empty Input!"
                return JsonResponse(response)
            
            if is_wrong_format_input(username, "name") or is_wrong_format_input(userpassword, "password"):
                response['alert'] = "Invalid Input!"
                return JsonResponse(response)

            # compare password with passworda
            if userpassword != userpassworda:
                response['alert'] = "Passwords must be entered consistently!"
                return JsonResponse(response)
            
            # checking pass 
            db_data = database_match({'user_name': username})
            if db_data is None:
                # register
                add_user(username, userpassword)
                response['alert'] = 'success'
            else:
                response['alert'] = 'User already exists!'
            
            return JsonResponse(response)
        
        elif data.get('click') == "cancel":
            response['alert'] = None
            return JsonResponse(response)
        elif data.get('click') == 'login':
            response['alert'] = None
            return JsonResponse(response)
        else:
            response['alert'] = "Page Wrong!"
            return JsonResponse(response)
            