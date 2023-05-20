from webexchange.views.common.utils import *

class callback(View):
    def post(self, request, **kw):
        response = {'alert': None}
        data = json.loads(request.body.decode('utf-8'))
        username = data['username']

        # get all users assets data
        user = get_exchange_user(user_name=username)
        verify_result = get_verification_information(user)

        response['verify-result'] = verify_result
        return JsonResponse(response)