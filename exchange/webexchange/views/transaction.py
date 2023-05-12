from webexchange.views.common.utils import *

class transaction(View):
    def get(self, request, **kwargs):
        return render(request, 'wallet.html')
        
    def post(self, request, **kwargs):
        response = {'alert': None}
        data = json.loads(request.body.decode('utf-8'))
        
        # 

        return JsonResponse(response)