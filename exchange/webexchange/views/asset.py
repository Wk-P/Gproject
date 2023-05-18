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
        res_data = []
        data = json.loads(request.body.decode('utf-8'))

        user = get_user(user_name=data['username'])
        if data['click'] == "no":
            asset_data = fetch_exchange_assets_data(user)
            if asset_data is not None:
                res_data.append({"asset_data":asset_data})
            # res_data == [None]
            
            response['alert'] = 'success'
            if len(res_data) > 0:
                # valid data
                response['asset_data'] = res_data
            else:
                response['asset_data'] = None
        return JsonResponse(response)