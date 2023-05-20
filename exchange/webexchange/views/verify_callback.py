from webexchange.views.common.utils import *

class callback(View):
    def post(self, request, **kw):
        response = {'alert': None}

        data = json.loads(request.body.decode())
        username = data['username']        

        user = get_exchange_user(user_name=username)

        # get all users assets data
        # result = get_verification_information(user)
        # if result is not None:
        #     response['alert'] = 'success'
        #     response['result'] = result
        # else:
        #     response['alert'] = "No Data"
        
        response['test'] = "TEST"
        return JsonResponse(response)