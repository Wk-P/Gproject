from django.shortcuts import render, redirect
from django.views import View
from webexchange.models import User, Wallets, Asset
import re, random, time, hashlib, json, os, requests
from hashlib import sha256
from typing import List
from django.utils import timezone
from django.urls import reverse
from django.http import JsonResponse
from random import randint

import pyfinite
from pyfinite import genericmatrix

from .genericgf import GenericGF
from .exceptions import NotAnElement, NotInvertible, PolynomialError

from .merkle import MerkleTree
from .zk_snarks import generate_proof, verify_proof

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
    all_users_data = []
    
    # all_user_data style
    # all user
    #   wallet_ID, user_ID, asset_amount

    # get all users data
    all_users = User.objects.all()
    verifying_user_data = get_user_data(username)

    

    if all_users.exists():
        for user in all_users:
            user_data = get_user_data(user.user_name)
            all_users_data.append(user_data)

        # verify
        '''
            # 验证函数: 用户名和钱包数据
            # verify(name, wallet):
            #   ...
            #   return data
        '''
        information = {'test': 'test_OK'}
        return information
    else:
        return None
    
__all__ = [ 
    'os', 'json', 're', 'time', 'random', 'hashlib', 'sha256', 'List', 'randint', 'pyfinite', 'requests',       # python3 package
    'JsonResponse', 'render', 'View', 'User', 'Wallets', 'Asset', 'timezone', 'reverse', 'redirect',            # Django package
    'fetch_asset_data', 'fetch_wallets_data', 'get_user_data', 'get_verification_information',                  # my package
    'username_check', 'hash_encrypt', 'login_input_check', 'register_input_check', 
    'MerkleTree', 'genericmatrix', 'GenericGF', 'generate_proof', 'verify_proof', 'NotAnElement', 'NotInvertible', 'PolynomialError'] # algorithm package

"""
    No File or Function
"""
# 'NotAnElement', 'NotInvertible', 'PolynomialError']