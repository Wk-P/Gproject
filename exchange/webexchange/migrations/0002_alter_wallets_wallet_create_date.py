# Generated by Django 4.1.7 on 2023-04-23 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webexchange', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallets',
            name='wallet_create_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
