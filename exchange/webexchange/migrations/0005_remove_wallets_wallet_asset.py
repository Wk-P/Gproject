# Generated by Django 4.1.7 on 2023-03-09 13:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webexchange', '0004_rename_user_id_wallets_user_remove_asset_wallet_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wallets',
            name='wallet_asset',
        ),
    ]
