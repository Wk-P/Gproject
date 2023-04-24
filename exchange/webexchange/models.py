from django.db import models

# Create your models here.
# User information
class User(models.Model):
    # hash field
    user_ID = models.CharField(max_length=255, default=None, unique=True, db_index=True)
    user_password = models.CharField(max_length=200, default=None)

    # usuall field
    user_create_date = models.DateTimeField(auto_now_add=True)
    user_name = models.CharField(max_length=200, null=False)

# Wallets data related with User by user_ID
class Wallets(models.Model):
    # hash field
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    wallet_ID = models.CharField(max_length=200, default=None)

    # usuall field
    wallet_create_date = models.DateTimeField(auto_now_add=True)

class Asset(models.Model):
    # identifier
    wallet = models.ForeignKey(Wallets, on_delete=models.CASCADE, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    chain = models.CharField(max_length=200, default=None)

    # usuall field
    asset_type = models.CharField(max_length=200, default=None)
    asset_amount = models.FloatField(default=0)