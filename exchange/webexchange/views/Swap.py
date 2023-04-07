from webexchange.views.common.utils import *

class swap(View):
    def get(self, request, **kwargs):
        return render(request, 'swap.html')