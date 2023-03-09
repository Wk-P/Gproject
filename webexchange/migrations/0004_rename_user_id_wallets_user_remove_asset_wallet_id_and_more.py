# Generated by Django 4.1.7 on 2023-03-09 13:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webexchange', '0003_alter_user_user_create_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wallets',
            old_name='user_ID',
            new_name='user',
        ),
        migrations.RemoveField(
            model_name='asset',
            name='wallet_ID',
        ),
        migrations.AddField(
            model_name='asset',
            name='wallet',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='webexchange.wallets'),
        ),
    ]
