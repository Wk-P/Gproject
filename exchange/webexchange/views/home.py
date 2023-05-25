from webexchange.views.common.utils import *

# index
class index(View):
    def get(self, request):
        return render(request, 'index.html')
    
    def post(self, request):
        response = {'alert': None}
        data = json.loads(request.body.decode('utf-8'))

        if data.get('click') == 'login':
            return JsonResponse(response)
        elif data.get('click') == 'sign':
            return JsonResponse(response)
        else:
            response['alert'] = "Page Wrong!"
            return JsonResponse(response)