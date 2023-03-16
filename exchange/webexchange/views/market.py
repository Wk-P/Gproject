from . import *

# market
class market(View):
    def get(self, request):
        return render(request, 'market.html')
    
    def post(self, request):
        return render(request, 'market.html')