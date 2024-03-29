from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Q
from django.core.cache import cache
from webexchange.models import User, Wallet, Asset, User_Asset, User_Wallet, User_Trade_History
import re
import random
import time
import hashlib
import json
import os
import requests
import websockets
import asyncio
import threading
from hashlib import sha256
from typing import List
from django.utils import timezone
from django.urls import reverse
from django.http import JsonResponse
from random import randint

from sympy import FiniteField
import pyfinite
from pyfinite import genericmatrix

from .appexceptions import InputException, DataException, AppException

from .genericgf import GenericGF
from .exceptions import NotAnElement, NotInvertible, PolynomialError

from .merkle import MerkleTree
from .zk_snarks import generate_proof, verify_proof

from .verify_algorithm import combine_data
from .exchange_center import Order, Ordered, OrderConsumer, OrderManager, OrderProducer

__all__ = [
    # python3 package
    "os",
    "json",
    "re",
    "time",
    "random",
    "hashlib",
    "sha256",
    "List",
    "randint",
    "pyfinite",
    "requests",
    "websockets",
    "asyncio",
    "threading",
    # Django package
    "JsonResponse",
    "render",
    "View",
    "User",
    "Wallet",
    "Asset",
    "User_Asset", 
    "User_Wallet", 
    "User_Trade_History",
    "timezone",
    "reverse",
    "redirect",
    "cache",
    # my function
    "toJson",
    "hash_encrypt",
    "is_empty_input",
    "is_wrong_format_input",
    "database_match",
    # USER
    "get_exchange_user",
    "add_exchange_user",
    "get_exchange_user_data",
    # WALLET
    "get_user_private_wallet",
    "get_user_private_wallets",
    "add_exchange_wallet",
    "get_exchange_wallet",
    "get_all_exchange_wallets",
    "add_user_private_wallet",
    "fetch_exchange_wallets_data",
    # ASSET
    "get_user_private_asset",
    "get_exchange_assets",
    "add_exchange_asset",
    "fetch_exchange_assets_data",
    # TRADE
    "add_exchange_trade_history",
    "get_exchange_trade_history",
    # ORDER class
    'Order',
    'Ordered',
    'OrderManager',
    'OrderConsumer',
    'OrderProducer',
    # others
    "get_verification_information",
    # exceptions class
    "InputException",
    "DataException",
    "AppException",
    # algorithm package
    "MerkleTree",
    "genericmatrix",
    "GenericGF",
    "generate_proof",
    "verify_proof",
    "NotAnElement",
    "NotInvertible",
    "PolynomialError",
]

def toJson(string):
    return json.loads(string)

# string to hash code encrypting
def hash_encrypt(string):
    hash_obj = hashlib.md5()
    hash_obj.update(string.encode("utf-8"))
    return hash_obj.hexdigest()


def is_empty_input(input):
    """Check empty input"""
    try:
        if input == "":
            raise InputException
        else:
            # pass
            return False
    except InputException:
        return True


def is_wrong_format_input(input, mode):
    """
    Check input format
    Check Name and Password
    @return: -> str
                   OK:  Checking pass
        DataException:  Checking no pass
    """
    name_pattern = r"^[A-Za-z]+.*"
    password_pattern = r".*\s+.*"
    try:
        if mode == "name":
            if not re.match(name_pattern, input):
                raise InputException
            else:
                # pass
                return False
        elif mode == "password":
            if re.match(password_pattern, input):
                raise InputException
            else:
                # pass
                return False
        else:
            raise AppException
    except (InputException, AppException):
        return True


# match and fetch data
def database_match(**kw):
    """
    @ params:
        data_name: database column
        **data: (Dictionary)data contents
    @ return(bool):
        None: matching failed!
        Object: matched!
    """
    key = list(kw.keys())[0]
    value = list(kw.values())[0]
    if key == 'user_name':
        user_objs = User.objects.filter(user_name=value)
        try:
            if not user_objs.exists():
                raise DataException
            else:
                # matching
                return user_objs[0]
        except DataException:
            return None
    elif key == 'wallet_id':
        wallets = Wallet.objects.filter(wallet_ID=value)
        try:
            if not wallets.exists():
                raise DataException
            else:
                return wallets
        except DataException:
            return None


"""
    USER OPERATION FUNCTION
    get_user, add_user, fetch_user_data
"""


# RETURN OBJECT
def get_exchange_user(**kw):
    """ 
        @Get User Object \n
        @Return: User Object | None
    """
    user_name = kw.get('user_name')
    user_id = kw.get('user_id')
    user_obj = User.objects.filter(Q(user_name=user_name) | Q(user_ID=user_id))
    if user_obj.exists():
        return user_obj.first()
    else:
        return None


def add_exchange_user(username, password):
    # data packing
    user_ID = hash_encrypt(username)
    user_password = hash_encrypt(password)
    user_name = username
    
    # create user data
    user_obj = User(user_name=user_name, user_ID=user_ID,
                    user_password=user_password)
    user_obj.save()


# RETURN JSON
def get_exchange_user_data(**kw):
    """
        @Get User Object JSON data \n
        @Return: User Object JSON | None
        @return { \n
            "user_name": user.user_name, \n
            "user_ID": user.user_ID, \n
            "user_create_date": user.user_create_date, \n
        }
    """
    user_name = kw.get('user_name')
    user_id = kw.get('user_id')
    user = get_exchange_user(user_name=user_name, user_id=user_id)
    if user is not None:
        # get wallets
        return {
            "user_name": user.user_name,
            "user_ID": user.user_ID,
            "user_create_date": user.user_create_date,
        }
    else:
        return None



"""
    WALLET OPERATION FUNCTION
    get_wallet, add_wallet, fetch_wallets_data
"""

def get_exchange_wallet(**kw):
    user = kw.get('user', None)
    exchange_wallet_ID = kw.get('wallet_ID', None)
    if user is None and exchange_wallet_ID is None:
        return None

    # generate query filter expression
    query = Q()
    if user is not None:
        query |= Q(user_ID=user.user_ID)
    if exchange_wallet_ID is not None:
        query |= Q(exchange_wallet_ID=exchange_wallet_ID)
    
    wallet_obj = Wallet.objects.filter(query)
    if wallet_obj.exists():
        return wallet_obj.first()
    else:
        return None

# RETURN OBJECT LIST
def get_all_exchange_wallets():
    """
        @Get Wallets Objects \n
        @Return: Wallets Objects List | None
    """
    wallets_obj = Wallet.objects.all()
    if wallets_obj.exists():
        return wallets_obj  # wallet objects list
    else:
        return None


# RETURN OBJECT
def get_user_private_wallet(wallet_ID):
    """
        @Get Wallet Object \n
        @Return: Wallet Object | None
    """
    wallet_obj = User_Wallet.objects.filter(wallet_ID=wallet_ID)
    if wallet_obj.exists():
        return wallet_obj.first()  # first wallet_obj
    else:
        return None

def add_exchange_wallet(username):
    user = get_exchange_user(user_name=username)
    wallet_ID = hash_encrypt(user.user_ID[0:10])
    Wallet(user_ID=user.user_ID, exchange_wallet_ID=wallet_ID).save()
    

def add_user_private_wallet(wallet_ID):
    # generate Wallet_ID
    
    check = User_Wallet.objects.filter(wallet_ID=wallet_ID)

    # check database
    if not check.exists():
        wallet = User_Wallet(wallet_ID=wallet_ID)
        wallet.save()
        return 1
    else:
        return None

# RETURN JSON LIST
def fetch_exchange_wallets_data():
    """
        @Get Wallets Objects JSON data\n
        @Return: Wallets Objects JSON List | None
        @@Return Style: \n
            "user_ID": user.user_ID,
            "wallet_ID": wallet_obj.wallet_ID
    """
    wallets_obj = get_all_exchange_wallets()
    res_data = []
    if wallets_obj is not None:
        for wallet_obj in wallets_obj:
            res_data.append({ 
                "wallet_ID": wallet_obj.wallet_ID 
            })
        return res_data
    else:
        return None


"""
    ASSETS OPERATION FUNCTION
    get_assets, add_assets, fetch
"""


# RETURN OBJECT LIST
def get_exchange_assets(**kw):
    user = kw.get('user')
    wallet_ID = kw.get('wallet_ID')
    """
        @Get Assets Objects \n
        @Return: Assets Objects List | None
    """
    query = Q()
    if user is not None:
        query |= Q(user=user)
    if wallet_ID is not None:
        query |= Q(wallet_ID=wallet_ID)

    assets_obj = Asset.objects.filter(query)
    if assets_obj.exists():
        return assets_obj
    else:
        return None


def add_exchange_asset(user, chain, asset_type, asset_amount):
    wallet = get_exchange_wallet(user=user)
    if user is not None:
        asset_obj = Asset(
            user=user,
            chain=chain,
            wallet_ID=wallet.exchange_wallet_ID,
            asset_type=asset_type,
            asset_amount=asset_amount,
        )
        asset_obj.save()

# RETURN JSON LIST
def fetch_exchange_assets_data(user):
    """
        @Get Assets Objects JSON data\n
        @Return: Assets Objects JSON List | None
        @@Return Type: \n
        [{
            "chain": asset_obj.chain,
            "asset_type": asset_obj.asset_type,
            "asset_amount": asset_obj.asset_amount,
        }]
    """
    assets_obj = get_exchange_assets(user=user)
    res_data = []
    if assets_obj is not None:
        for asset_obj in assets_obj:
            res_data.append(
                {
                    "chain": asset_obj.chain,
                    "asset_type": asset_obj.asset_type,
                    "asset_amount": asset_obj.asset_amount,
                }
            )
        return res_data
    else:
        return None

"""
    VERIFICATION FUNCTION
"""
def get_exchange_user_data(user):
    """
    @Get specified user object JSON data
    @@Return Style: \n
        "user_name" \n
        "user_ID"   \n
        "assets": [{    \n
            "chain",    \n
            "asset_type",   \n
            "asset_amount", \n
        }]
    """
    # get user object
    # get all wallets of user
    # get all assets of wallets
    user_data = {
        "user_name": None,
        "user_ID": None,
        "assets": None,
    }
    """
        user_data = {
            "user_name"
            "user_ID"
            "assets": [{
                "chain"
                "asset_type"
                "asset_amount"
            }]
        }
    """
    if user is not None:
        wallet = get_exchange_wallet(user=user)
        user_data["user_name"] = user.user_name
        user_data["user_ID"] = user.user_ID
        user_data['wallet_ID'] = wallet.exchange_wallet_ID
        user_data['assets'] = fetch_exchange_assets_data(user)
        return user_data
    else:
        return None


def get_verification_information(user):
    all_users_data = []
    # all_user_data style
    # all user
    #   wallet_ID, user_ID, asset_amount

    # get all users data
    all_users = User.objects.all()
    verifying_user_data = get_exchange_user_data(user)

    if all_users.exists():
        for user in all_users:
            user_data = get_exchange_user_data(user)
            all_users_data.append(user_data)

        information = combine_data(verifying_user_data, all_users_data)
        information['wallet_ID'] = get_exchange_wallet(user=user).exchange_wallet_ID
        # verify
        """
            # 验证函数: 用户名和钱包数据
            # verify(name, wallet):
            #   ...
            #   return data
        """
        return information
    else:
        return None


def add_exchange_trade_history(username, out_wallet, in_wallet, amount, asset_type, action, chain):
    user = get_exchange_user(user_name=username)
    wallet = get_exchange_wallet(user=user)
    # save trade history to DB
    User_Trade_History(user_name=username, user_ID=user.user_ID, amount=amount, in_wallet_ID=in_wallet, out_wallet_ID=out_wallet, symbol=asset_type, action=action, chain=chain).save()
    
def get_exchange_trade_history(username):
    user = get_exchange_user(user_name=username)
    history = User_Trade_History.objects.filter(user_ID=user.user_ID)
    if history.exists():
        return history
    else:
        return None

def get_user_private_asset(username, wallet_ID, symbol, chain):
    user = get_exchange_user(user_name=username)
    asset = User_Asset.objects.filter(userid=user.user_ID, wallet_ID=wallet_ID, symbol=symbol, chain=chain)
    if asset.exists():
        return asset.first()
    else:
        return None

def get_user_private_wallets(username):
    user = get_exchange_user(user_name=username)
    wallets = User_Wallet.objects.filter(user_ID=user.user_ID)
    if wallets.exists():
        return wallets
    else:
        return None
    
def get_user_private_wallet(wallet_ID):
    wallet = User_Wallet.objects.filter(wallet_ID=wallet_ID)
    if wallet.exists():
        return wallet.first()
    else:
        return None

"""
    No File or Function
"""
# 'NotAnElement', 'NotInvertible', 'PolynomialError']
