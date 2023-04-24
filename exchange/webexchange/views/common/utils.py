from django.shortcuts import render, redirect
from django.views import View
from webexchange.models import User, Wallets, Asset
import re, random, time, hashlib, json, os, requests, websockets, asyncio
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
        # others
            "get_wallet_asset_amount",
            "get_user_all_asset_amount",
            "fetch_user_all_assets_data",
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
def database_match(data):
    """
    @ params:
        data_name: database column
        **data: (Dictionary)data contents
    @ return(bool):
        None: matching failed!
        Object: matched!
    """
    key = list(data.keys())[0]
    value = list(data.values())[0]

    if key == "user_name":
        user_objs = User.objects.filter(user_name=value)
        try:
            if not user_objs.exists():
                raise DataException
            else:
                # matching
                return user_objs[0]
        except DataException:
            return None
    else:
        return None


"""
    USER OPERATION FUNCTION
    get_user, add_user, fetch_user_data
"""


# RETURN OBJECT
def get_user(username):
    user_obj = User.objects.filter(user_name=username)
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
    user_obj = User(user_name=user_name, user_ID=user_ID, user_password=user_password)
    user_obj.save()


# RETURN JSON
def fetch_user_data(username):
    user = get_user(username)
    if user is not None:
        return {
            "user_name": user.user_name,
            "user_ID": user.user_ID,
            "user_create_date": user.user_create_date,
        }
    else:
        return user


"""
    WALLET OPERATION FUNCTION
    get_wallet, add_wallet, fetch_wallets_data
"""


# RETURN OBJECT LIST
def get_wallets(user):
    wallets_obj = list(Wallets.objects.filter(user=user))
    if len(wallets_obj) > 0:
        return wallets_obj  # wallet objects list
    else:
        return None


# RETURN OBJECT
def get_wallet(user, wallet_ID):
    wallet_obj = list(Wallets.objects.filter(user=user, wallet_ID=wallet_ID))
    if wallet_obj > 0:
        return wallet_obj[0]  # first wallet_obj
    else:
        return None


def add_wallet(username):
    user_ID = hash_encrypt(username)
    user_obj = User.objects.filter(user_name=username, user_ID=user_ID)
    # create Wallets object
    wallet_ID = hash_encrypt(user_ID + username)


# RETURN JSON LIST
def fetch_wallets_data(user):
    wallets_obj = get_wallets(user)
    res_data = []
    if len(wallets_obj) > 0:
        for wallet_obj in wallets_obj:
            res_data.append(
                {"user_ID": user.user_ID, "wallet_ID": wallet_obj.wallet_ID}
            )
        return res_data
    else:
        return None


"""
    ASSETS OPERATION FUNCTION
    get_assets, add_assets, fetch
"""


# RETURN OBJECT LIST
def get_assets(user, wallet_ID):
    wallet = get_wallet(user, wallet_ID)  # choose wallet
    assets_obj = list(Asset.objects.filter(wallet=wallet))
    if len(assets_obj) > 0:
        return assets_obj
    else:
        return None


def add_asset(username, wallet_ID, chain, asset_type, asset_amount):
    user = get_user(username)
    if user is not None:
        wallet_obj = get_wallet(user, wallet_ID)
        if wallet_obj is not None:
            asset_obj = Asset(
                user=user,
                chain=chain,
                wallet=wallet_obj, 
                asset_type=asset_type, 
                asset_amount=asset_amount,
            )
            asset_obj.save()


# RETURN JSON LIST
def fetch_assets_data(username, wallet_ID):
    user = get_user(username)
    wallet_obj = get_wallet(user, wallet_ID)
    assets_obj = get_assets(user, wallet_obj)
    res_data = []
    if assets_obj is not None:
        for asset_obj in assets_obj:
            res_data.append(
                {
                    "wallet_ID": wallet_ID,
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


# RETURN JSON LIST
def fetch_user_all_assets_data(username):
    """
    user -> [{ asset type , asset amount }]
    """

    user = get_user(username)
    # get all assets list of user
    wallets_list = get_wallets(user)
    res_data = []
    if len(wallets_list) > 0:
        for wallet in wallets_list:
            res_data.append({
                user.user_ID: fetch_assets_data(username, wallet.wallet_ID),
            })
        return res_data
    else:
        return None

# --------------------------------- #


def get_user_data(username):
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
                "wallet_ID"
                "asset_type"
                "asset_amount"
            }]
        }
    """

    users = User.objects.filter(user_name=username)
    if users.exists():
        user = users.first()
        user_data["user_name"] = user.user_name
        user_data["user_ID"] = user.user_ID

        wallets = Wallets.objects.filter(user=user)
        if wallets.exists():
            for wallet in wallets:
                assets = Asset.objects.filter(wallet=wallet)
                if assets.exists():
                    for asset in assets:
                        user_data["assets"].append(
                            {
                                "wallet_ID": wallet.wallet_ID,
                                "asset_type": asset.asset_type,
                                "asset_amount": asset.asset_amount,
                            }
                        )
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
        """
            # 验证函数: 用户名和钱包数据
            # verify(name, wallet):
            #   ...
            #   return data
        """
        information = combine_data(user_data)
        return information
    else:
        return None


"""
    No File or Function
"""
# 'NotAnElement', 'NotInvertible', 'PolynomialError']
