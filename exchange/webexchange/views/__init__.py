from django.shortcuts import render, redirect
from django.views import View
from webexchange.models import User, Wallets, Asset
import re,random, time, hashlib
from django.utils import timezone
from django.urls import reverse

def test(ctype):
    print(get_all_user_data(ctype))

def get_all_user_data():
    usersname = User.objects.all()
    users_data = []
    for username in usersname:
        users_data.append(get_user_data(username))
    
    return users_data

# Get all wallet data bu user name
def fetch_wallets_data(user):
    wallets_data = []
    wallets = Wallets.objects.filter(user=user)
    if wallets.exists():
        for wallet in wallets:
            wallets_data.append({
                'wallet_ID': wallet.wallet_ID,
                'wallet': wallet,
            })
    else:
        wallets_data = None
    
    return wallets_data

# Get all asset data bu wallet
def fetch_asset_data(wallet, ctype):
    asset_data = {
        'wallet': None,
        'asset_amount': None,
    }
    asset = Asset.objects.filter(wallet=wallet, asset_type=ctype)
    if asset.exists():
        asset_data['asset_amount'] = asset.first().asset_amount
    else:
        asset_data = None
    
    return asset_data
    
def hash_encrypt(string):
    hash_obj = hashlib.md5()
    hash_obj.update(string.encode('utf-8'))
    return hash_obj.hexdigest()

def login_input_check(username, password):
    user_table = User.objects
    '''
        @type:
            0: Success
            1: Invalid input
            2: Password input wrong
            3: User not exists
    '''
    msg = {
        'alert': None,
        'type': None,
    }
    # check input weather valid
    if username == "" or password == "":
        msg['alert'] = 'Invalid Input!'
        msg['type'] = '1'
    else:
        try:
            # check user name weather already exist
            user_obj = user_table.get(user_name=username)
            hash_password = hash_encrypt(password)
            if hash_password == user_obj.user_password:
                msg['alert'] = "Login successfully!"
                msg['type'] = '0'
            else:
                msg['alert'] = 'Password input wrong!'
                msg['type'] = '2'
        except:
            # User not exists
            msg['alert'] = 'User not exists'
            msg['type'] = '3'
        else:
            return msg
    return msg

# check user name and password
def register_input_check(username, password, passworda):
    name_pattern = r'^[A-Za-z]+.*'
    password_pattern = r'.*\s+.*'
    user_table = User.objects
    '''
        @type:
            0: Success
            1: Invalid input
            2: Password input wrong
            3: User has existed
    '''
    msg = {
        'alert': None,
        'type': None,
    }
    # check input weather valid
    if username == "" or password == "" or passworda == "" or \
        not re.match(name_pattern, username) or \
        re.match(password_pattern, password) or \
        re.match(password_pattern, passworda):
        msg['alert'] = 'Invalid Input'
        msg['type'] = '1'
    else:
        print('sss')
        # password input wrong
        if password != passworda:
            msg['alert'] = "Password must be same"
            msg['type'] = '2'
        else:
            # empty user table
            # anable to add new user
            if user_table.count() == 0:
                msg['alert'] = 'Register successfully'
                msg['type'] = '0'
            try:
                # check user name weather already exist
                user_table.get(user_name=username)
                msg['alert'] = 'User already exists'
                msg['type'] = '3'
            except:
                # anable to add new user
                msg['alert'] = 'Register successfully'
                msg['type'] = '0'
            else:
                return msg
    return msg

def username_check(username):
    try:
        User.objects.get(user_name=username)
    except:
        return False
    return True


def get_user_data(username):
    # get user object
    # get all wallets of user
    # get all assets of wallets
    user_data = {
        'user_name': None,
        'user_ID': None,
        'assets': [],
    }
    '''
        user_data = {
            "user_name"
            "user_ID"
            "assets": [{
                "wallet_ID"
                "asset_type"
                "asset_amount"
            }]
        }
    '''

    users = User.objects.filter(user_name=username)
    if users.exists():
        user = users.first()
        user_data['user_name'] = user.user_name
        user_data['user_ID'] = user.user_ID

        wallets = Wallets.objects.filter(user=user)
        if wallets.exists():
            for wallet in wallets:

                assets = Asset.objects.filter(wallet=wallet)
                if assets.exists():
                    for asset in assets:
                        user_data['assets'].append({
                            'wallet_ID': wallet.wallet_ID,
                            'asset_type': asset.asset_type,
                            'asset_amount': asset.asset_amount,
                        })
                else:
                    pass
        else:
            return None
        return user_data
    else:
        return None

def get_verification_information(username):
    ret_set = {
        'all_user_data': None,
        'verificating_user_data': None,
        'except': False
    }

    all_user_data = []
    # all_user_data style
    # all user
    #   wallet_ID, user_ID, asset_amount
    try:
        all_username = User.objects.all().values_list('user_name', flat=True)
        for username in all_username:
            try:
                user_data = get_user_data(user_name)
                all_user_data.append(user_data)
            except:
                ret_set['all_user_data'] = None
                ret_set['verificating_user_data'] = None
                ret_set['except'] = True
                return ret_set

    except:
        ret_set['all_user_data'] = None
        ret_set['verificating_user_data'] = None
        ret_set['except'] = True
        return ret_set
    

    # single user
    #   wallet_ID, user_ID, asset_amount, asset_type, user_name
    try:
        user_obj = User.objects.get(user_name=username)
        user_ID = user_obj.user_ID  
        user_name = user_obj.user_name
    except:
        ret_set['all_user_data'] = None
        ret_set['verificating_user_data'] = None
        ret_set['except'] = True
        return ret_set

    # Not access empty attribute

    wallets_obj = Wallets.objects.filter(user_ID=user_ID)
    
    if wallets_obj.exists():
        wallet_obj = wallets_obj.first()
        wallet_ID = wallet_obj.wallet_ID

    else:
        ret_set['all_user_data'] = None
        ret_set['verificating_user_data'] = None
        ret_set['except'] = True
        return ret_set
    
    assets_obj = Asset.objects.filter(wallet_ID=wallet_ID)

    if assets_obj.exists():
        asset_obj = assets_obj.first()
        asset_type = asset_obj.asset_type
        asset_amount = asset_obj.asset_amount
    else: 
        ret_set['all_user_data'] = None
        ret_set['verificating_user_data'] = None
        ret_set['except'] = True
        return ret_set
        
    verificated_user_data = {
        'user_name': user_name,
        'wallet_ID': wallet_ID,
        'user_ID': user_obj.user_ID,
        'asset_amount': asset_amount,
        'asset_type': asset_type,
    }

    ret_set['all_user_data'] = all_user_data
    ret_set['verificating_user_data'] = verificated_user_data
    ret_set['except'] = False
    return ret_set

__all__ = ['fetch_asset_data', 'fetch_wallets_data', 'get_user_data', 'time','random', 'get_verification_information', 
           'username_check', 'render', 'View', 'User', 'Wallets', 'Asset', 're', 'timezone', 'hashlib', 
           'reverse', 'redirect', 'hash_encrypt', 'login_input_check', 'register_input_check', 'test']