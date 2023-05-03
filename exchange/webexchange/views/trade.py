from webexchange.views.common.utils import *

class trade(View):
    def get(self, request, **kwargs):
        return render(request, 'trade.html')
