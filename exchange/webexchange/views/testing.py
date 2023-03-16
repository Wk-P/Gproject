from . import *

class testing(View):
    def get(self, request):
        return render(request, 'testing.html')
    
    def post(self, request):
        data = {
            'message': "OK",
        }
        return JsonResponse(data)