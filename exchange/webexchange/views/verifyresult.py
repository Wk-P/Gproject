from webexchange.views.common.utils import *

class verifyresult(View):
    def get(self, request, **kwargs):
        username = kwargs.get('username')
        return render(request, 'verifyresult.html', context={'username': username})
    
    def post(self, request, **kwargs):
        # read result file
        username = kwargs.get('username')
        # feth verifydata from file
        # user_data = get_user_data(username) 
        
        # test code
        # test_file_name = "../verify_res_json/test.json"
        current_dir = os.path.dirname(os.path.abspath(__file__))
        result_file_name = os.path.join(current_dir, 'verify_res_json', 'output_data.json')

        with open(result_file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return JsonResponse(data[-1])