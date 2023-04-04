from . import *

class tests(View):
    def get(self, request, **kwargs):
        return render(request, 'tests.html')