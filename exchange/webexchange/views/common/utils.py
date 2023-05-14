from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Q
from webexchange.models import User, Wallets, Asset
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

import pyfinite
from pyfinite import genericmatrix

from .appexceptions import InputException, DataException, AppException

from .genericgf import GenericGF
from .exceptions import NotAnElement, NotInvertible, PolynomialError

from .merkle import MerkleTree
from .zk_snarks import generate_proof, verify_proof

from .verify_algorithm import combine_data
from .exchange_center import Order, OrderConsumer, OrderManager, OrderProducer

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
    "Wallets",
    "Asset",
    "timezone",
    "reverse",
    "redirect",
    # my function
    "toJson",
    "hash_encrypt",
    "is_empty_input",
    "is_wrong_format_input",
    "database_match",
    # USER
    "get_user",
    "add_user",
    "get_user_data",
    # WALLET
    "get_wallet",
    "get_wallets",
    "add_wallet",
    "fetch_wallets_data",
    # ASSET
    "get_assets",
    "add_asset",
    "fetch_assets_data",
    # ORDER class
    'Order',
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
        wallets = Wallets.objects.filter(wallet_ID=value)
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
def get_user(**kw):
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


def add_user(username, password):
    # data packing
    user_ID = hash_encrypt(username)
    user_password = hash_encrypt(password)
    user_name = username
    
    # create user data
    user_obj = User(user_name=user_name, user_ID=user_ID,
                    user_password=user_password)
    user_obj.save()


# RETURN JSON
def fetch_user_data(**kw):
    """
        @Get User Object JSON data \n
        @Return: User Object JSON | None
    """
    user_name = kw.get('user_name')
    user_id = kw.get('user_id')
    user = get_user(user_name=user_name, user_id=user_id)
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


# RETURN OBJECT LIST
def get_wallets():
    """
        @Get Wallets Objects \n
        @Return: Wallets Objects List | None
    """
    wallets_obj = list(Wallets.objects.all())
    if len(wallets_obj) > 0:
        return wallets_obj  # wallet objects list
    else:
        return None


# RETURN OBJECT
def get_wallet(wallet_ID):
    """
        @Get Wallet Object \n
        @Return: Wallet Object | None
    """
    wallet_obj = list(Wallets.objects.filter(wallet_ID=wallet_ID))
    if len(wallet_obj) > 0:
        return wallet_obj[0]  # first wallet_obj
    else:
        return None


def add_wallet(wallet_ID):
    # generate Wallet_ID
    if wallet_ID == None:
        return None
    else:
        wallet_ID = wallet_ID
    
    # check database
    if database_match(wallet_ID=wallet_ID) is None:
        wallet = Wallets(wallet_ID=wallet_ID)
        wallet.save()
        return 1
    else:
        return None

# RETURN JSON LIST
def fetch_wallets_data():
    """
        @Get Wallets Objects JSON data\n
        @Return: Wallets Objects JSON List | None
        @@Return Style: \n
            "user_ID": user.user_ID,
            "wallet_ID": wallet_obj.wallet_ID
    """
    wallets_obj = get_wallets()
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
def get_assets(user):
    """
        @Get Assets Objects \n
        @Return: Assets Objects List | None
    """
    assets_obj = list(Asset.objects.filter(user=user))
    if len(assets_obj) > 0:
        return assets_obj
    else:
        return None


def add_asset(user, chain, asset_type, asset_amount):
    if user is not None:
        asset_obj = Asset(
            user=user,
            chain=chain,
            asset_type=asset_type,
            asset_amount=asset_amount,
        )
        asset_obj.save()

# RETURN JSON LIST
def fetch_assets_data(user):
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
    assets_obj = get_assets(user)
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
def get_user_data(user):
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
        "assets": [],
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
        user_data["user_name"] = user.user_name
        user_data["user_ID"] = user.user_ID
        user_data['assets'] = []
        user_data['assets'].append(fetch_assets_data(user))
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
    verifying_user_data = get_user_data()

    if all_users.exists():
        for user in all_users:
            user_data = get_user_data(user.user_name)
            all_users_data.append({user.user_name: user_data})

        information = combine_data(user_data)
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


"""
    No File or Function
"""
# 'NotAnElement', 'NotInvertible', 'PolynomialError']
