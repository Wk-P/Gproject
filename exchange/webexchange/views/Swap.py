from webexchange.views.common.utils import *

class Swap(View):
    def get(self, request, **kwargs):
        return render(request, 'Swap.html')