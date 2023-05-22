from webexchange.views.common.utils import *


class proof(View):
    def get(self, request, **kwargs):
        # get all user asset amount sum
        username = kwargs.get('username')

        return render(request, 'proof.html')

    def post(self, request, **kwargs):
        response = {'alert': None}

        # without request.body

        wallets = get_all_exchange_wallets()
        
        response['assets_data'] = []

        if wallets.exists():
        # fetch data with wallets' ID
            for wallet in wallets:
                # every wallet assets data
                assets_data = get_exchange_assets(wallet_ID=wallet.exchange_wallet_ID)
                if assets_data.exists():
                    # fetch asset data from assets data
                    for asset in assets_data:
                        if asset.asset_type in response['assets_data']:
                            response['assets_data']['asset_type'] += asset.asset_amount
                        else:
                            response['assets_data'].append({
                                "asset_type": asset.asset_type,
                                "asset_amount": asset.asset_amount,
                            })
            
        else:
            response['alert'] = "No Data"

        return JsonResponse(response)