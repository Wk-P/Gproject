from . import *

# main
class main(View):
    def get(self, request):
        return render(request, 'main.html')
    
    def post(self, request):
        return render(request, 'main.html')

# index
class index(View):
    def get(self, request):
        return render(request, 'index.html')
    
    def post(self, request):
        return render(request, 'index.html')
