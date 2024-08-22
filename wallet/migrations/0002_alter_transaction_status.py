# Generated by Django 5.1 on 2024-08-22 10:43

import wallet.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='status',
            field=models.CharField(choices=[(wallet.models.TransactionStatus['STARTED'], 'Started'), (wallet.models.TransactionStatus['COMMITTED'], 'Committed'), (wallet.models.TransactionStatus['FAILED'], 'Failed'), (wallet.models.TransactionStatus['PENDING'], 'Pending')], default=wallet.models.TransactionStatus['STARTED'], max_length=1),
        ),
    ]
