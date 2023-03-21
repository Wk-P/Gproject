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
        
        result_file_name = "../verify_res_json/output_data.json"
        test_file_name = "../verify_res_json/test.json"
        with open(result_file_name, 'r') as f:
            data = json.load(f)
            
        data = {
        }
        return JsonResponse(data) #'user_data': user_data})