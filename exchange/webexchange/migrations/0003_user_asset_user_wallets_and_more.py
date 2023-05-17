# Generated by Django 4.1.7 on 2023-05-16 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webexchange', '0002_remove_asset_wallet_remove_wallets_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_Asset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wallet_ID', models.CharField(max_length=255)),
                ('user_ID', models.CharField(max_length=255)),
                ('asset_type', models.CharField(max_length=255)),
                ('chain', models.CharField(max_length=255)),
                ('asset_amount', models.FloatField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='User_Wallets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_ID', models.CharField(max_length=255)),
                ('wallet_ID', models.CharField(max_length=255)),
                ('chain', models.CharField(max_length=255)),
            ],
        ),
        migrations.RenameField(
            model_name='wallets',
            old_name='wallet_ID',
            new_name='exchange_wallet_ID',
        ),
        migrations.AddField(
            model_name='wallets',
            name='user_ID',
            field=models.CharField(default=None, max_length=255),
        ),
    ]
