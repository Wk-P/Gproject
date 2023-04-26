# Generated by Django 4.1.7 on 2023-04-26 06:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_ID', models.CharField(db_index=True, default=None, max_length=255, unique=True)),
                ('user_password', models.CharField(default=None, max_length=200)),
                ('user_create_date', models.DateTimeField(auto_now_add=True)),
                ('user_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Wallets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wallet_ID', models.CharField(default=None, max_length=200)),
                ('wallet_create_date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='webexchange.user')),
            ],
        ),
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chain', models.CharField(default=None, max_length=200)),
                ('asset_type', models.CharField(default=None, max_length=200)),
                ('asset_amount', models.FloatField(default=0)),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='webexchange.user')),
                ('wallet', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='webexchange.wallets')),
            ],
        ),
    ]
