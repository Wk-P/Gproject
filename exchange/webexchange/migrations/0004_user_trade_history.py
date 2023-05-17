# Generated by Django 4.1.7 on 2023-05-17 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webexchange', '0003_user_asset_user_wallets_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_Trade_History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_point', models.DateTimeField(auto_now_add=True)),
                ('wallet_ID', models.CharField(max_length=255)),
                ('user_ID', models.CharField(max_length=255)),
                ('action', models.CharField(max_length=255)),
                ('amount', models.FloatField(default=0)),
                ('user_name', models.CharField(max_length=255)),
            ],
        ),
    ]