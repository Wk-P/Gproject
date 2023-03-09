from django.shortcuts import render, redirect
from django.views import View
from ..models import User, Wallets, Asset
import re
from django.utils import timezone
import hashlib
from django.urls import reverse

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
    user_data = {
        'user_name': user_name,
        'wallet_ID': wallet_ID,
        'user_ID': user_obj.user_ID,
        'asset_amount': asset_amount,
        'asset_type': asset_type,
    }
    try:
        user_obj = User.objects.get(user_name=username)
        user_ID = user_obj.user_ID  
        user_name = user_obj.user_name
    except:
        user_data = None
        return user_data

    # Not access empty attribute

    wallets_obj = Wallets.objects.filter(user_ID=user_ID)
    
    if wallets_obj.exists():
        wallet_obj = wallets_obj.first()
        wallet_ID = wallet_obj.wallet_ID

    else:
        user_data = None
        return user_data
    
    assets_obj = Asset.objects.filter(wallet_ID=wallet_ID)

    if assets_obj.exists():
        asset_obj = assets_obj.first()
        asset_type = asset_obj.asset_type
        asset_amount = asset_obj.asset_amount
    else: 
        user_data = None
        return user_data
        
    user_data = {
        'user_name': user_name,
        'wallet_ID': wallet_ID,
        'user_ID': user_obj.user_ID,
        'asset_amount': asset_amount,
        'asset_type': asset_type,
    }
    
    return user_data

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

__all__ = ['get_verification_information', 'username_check', 'render', 'View', 'User', 'Wallets', 'Asset', 're', 'timezone', 'hashlib', 'reverse', 'redirect', 'hash_encrypt', 'login_input_check', 'register_input_check']