from webexchange.views.common.utils import *

class coins(View):
    def get(self, request, **kwargs):
        return render(request, 'coins.html')