from ..views import *

# usercenter/asset
class asset(View):
    def get(self, request, **kwargs):
        username = kwargs.get('username')
        return render(request, 'asset.html', {'username': username})

    def post(self, request):
        pass