from webexchange.views.common.utils import *

# market
class market(View):
    def get(self, request):
        return render(request, 'market.html')
    
    def post(self, request):
        url = 'https://api.coincap.io/v2/markets'
        method = 'GET'
        data = json.loads(requests.request(method, url).content)
        return JsonResponse(data)