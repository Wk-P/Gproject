from webexchange.views.common.utils import *

# main
class main(View):
    def get(self, request, **kwargs):
        username = kwargs.get('username')
        if database_match(user_name=username) is not None:
            return render(request, 'main.html', context={'username': username})
        else:
            return redirect('404')
        
    def post(self, request):
        return render(request, 'main.html')

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