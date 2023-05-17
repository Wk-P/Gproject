from webexchange.views.common.utils import *

class coins(View):
    def get(self, request):
        return render(request, 'coins.html')

    def post(self, request):
        response = {'alert': None}
        # TODO here...

        return JsonResponse(response)