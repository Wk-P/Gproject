from webexchange.views.common.utils import *


class proof(View):
    def get(self, request, **kwargs):
        username = kwargs.get('username')
        return render(request, 'proof.html', context={'username': username})

    def post(self, request, **kwargs):
        # sum of all users
        response = {'alert': None}
        data = json.loads(request.body.decode('utf-8'))
        username = data['username']
        symbols = data.get('symbols')

        # get all users assets data
        users = User.objects.all()
        result_data = {}
        for symbol in symbols:
            result_data[f"{symbol}"] = 0
            for user in users:
                assets_data = fetch_assets_data(user)
                if assets_data == None:
                    response['alert'] = 'NO DATA'
                    return JsonResponse(response)
                else:
                    for asset_data in assets_data:
                        if asset_data['asset_type'] == symbol:
                            result_data[f"{symbol}"] += asset_data['asset_amount']

        get_verification_information(user)

        response['data'] = result_data
        return JsonResponse(response)
