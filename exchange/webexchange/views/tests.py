from . import *
import requests

class tests(View):
    def get(self, request, **kwargs):
        return render(request, 'tests.html')
    
    def post(self, request):
        url = 'https://api.coincap.io/v2/markets'
        method = "GET"
        data = json.loads(requests.request(method, url).content)
        return JsonResponse(data)