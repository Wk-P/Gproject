from webexchange.views.common.utils import *

class nav(View):
    def get(self, request, **kwargs):
        return render(request, 'nav.html')