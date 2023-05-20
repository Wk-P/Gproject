from webexchange.views.common.utils import *

# usercenter/asset
class asset(View):
    def get(self, request, **kwargs):
        username = kwargs.get('username')
        
        if database_match(user_name=username) is not None:
            return render(request, 'asset.html', {'username': username})
        else:
            return redirect('404')
        
    def post(self, request, **kwargs):
        
        response = {'alert': None}
        data = json.loads(request.body.decode('utf-8'))

        username = data['username']
        user = get_exchange_user(user_name=username)

        # get user asset_data
        asset_data = fetch_exchange_assets_data(user)
        if asset_data is not None:
            response['asset_data'] = asset_data
            response['alert'] = 'success'
        else:
            response['alert'] = 'No Data'
            response['asset_data'] = None
        return JsonResponse(response)