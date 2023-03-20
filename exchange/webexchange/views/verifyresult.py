from . import *

class verifyresult(View):
    def get(self, request, **kwargs):
        username = kwargs.get('username')
        return render(request, 'verifyresult.html', context={'username': username})
    
    def post(self, request, **kwargs):
        # read result file
        username = kwargs.get('username')
        # feth verifydata from file
        # user_data = get_user_data(username) 

        data = {
            'time': '2023',
            'user_ID': '1313131',
        }
        return JsonResponse(data) #'user_data': user_data})