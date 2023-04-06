from webexchange.views.common.utils import *

class exchange(View):
    def get(self, request, **kwargs):
        return render(request, 'exchange.html')