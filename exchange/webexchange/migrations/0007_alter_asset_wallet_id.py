# Generated by Django 4.1.7 on 2023-05-17 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webexchange', '0006_wallet_delete_wallets_asset_wallet_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='wallet_ID',
            field=models.CharField(default='', max_length=255),
        ),
    ]
