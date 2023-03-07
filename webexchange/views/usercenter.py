from . import *

# usercenter
class usercenter(View):
    def get(self, request):
        return render(request, 'usercenter.html')
    
    def post(self, request):
        return render(request, 'usercenter.html')