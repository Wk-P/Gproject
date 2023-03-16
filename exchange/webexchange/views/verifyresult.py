from . import *

class verifyresult(View):
    def get(self, request, **kwargs):
        # read result file
        username = kwargs.get('username')
        
        # feth verifydata
        # user_data = get_user_data(username) 
        data = json.loads(request.GET.get('data'))
        return render(request, 'verifyresult.html', context={'data': data}) #'user_data': user_data})