from webexchange.views.common.utils import *

# views request handle
class trade(View):
    async def get(self, request, **kwargs):
        username = kwargs.get('username')
        return render(request, 'trade.html', context={'username': username})