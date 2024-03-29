from django.db import models

# Create your models here.
# User information
class User(models.Model):
    # hash field
    user_ID = models.CharField(max_length=255, default=None, unique=True, db_index=True)
    user_password = models.CharField(max_length=255, default=None)

    # usuall field
    user_create_date = models.DateTimeField(auto_now_add=True)
    user_name = models.CharField(max_length=255, null=False)


# Wallets data related with User by user_ID
class Wallet(models.Model):
    # hash field
    user_ID = models.CharField(max_length=255, default=None)
    exchange_wallet_ID = models.CharField(max_length=255, default=None)

    # usuall field
    wallet_create_date = models.DateTimeField(auto_now_add=True)


class Asset(models.Model):
    # identifier
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True)
    chain = models.CharField(max_length=255, default=None)
    wallet_ID = models.CharField(max_length=255, default='')

    # usuall field
    asset_type = models.CharField(max_length=255, default=None)
    asset_amount = models.FloatField(default=0)


class User_Trade_History(models.Model):
    time_point = models.DateTimeField(auto_now_add=True)
    out_wallet_ID = models.CharField(max_length=255,default=None)
    in_wallet_ID = models.CharField(max_length=255,default=None)
    chain = models.CharField(max_length=255,default=None)
    user_ID = models.CharField(max_length=255,default=None)
    action = models.CharField(max_length=255,default=None)
    amount = models.FloatField(default=0)
    user_name = models.CharField(max_length=255,default=None)
    symbol = models.CharField(max_length=255, default=None)


class User_Wallet(models.Model):
    user_ID = models.CharField(max_length=255, default=None)
    wallet_ID = models.CharField(max_length=255, default=None)


class User_Asset(models.Model):
    wallet_ID = models.CharField(max_length=255,default=None)
    userid = models.CharField(max_length=255,default=None)
    symbol = models.CharField(max_length=255,default=None)
    chain = models.CharField(max_length=255,default=None)
    amount = models.FloatField(max_length=255,default=None)