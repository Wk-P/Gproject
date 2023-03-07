from . import *

# 404
class pagenotfound(View):
    def get(self, request):
        return render(request, '404.html')

    def post(self, request):
        return render(request, '404.html')