# Create your models here.
from enum import Enum

from django.contrib.auth.models import User
from django.db import models


class Country(Enum):
    IRAN = 'ir'
    Canada = 'ca'

    @classmethod
    def choices(cls):
        return [
            (cls.IRAN.value, 'Iran'),
            (cls.Canada.value, 'Canada'),
        ]


class TransactionStatus(Enum):
    STARTED = 'S'
    COMMITTED = 'D'
    FAILED = 'F'
    PENDING = 'P'

    @classmethod
    def choices(cls):
        return [
            (cls.STARTED.value, 'Started'),
            (cls.COMMITTED.value, 'Committed'),
            (cls.FAILED.value, 'Failed'),
            (cls.PENDING.value, 'Pending'),
        ]


class WalletUser(User):
    updated_at = models.DateTimeField(auto_now=True, null=False)
    national_id = models.CharField(max_length=11, null=False, blank=False, unique=True, db_index=True)


class Wallet(models.Model):
    user = models.ForeignKey(WalletUser, on_delete=models.CASCADE, null=False)
    balance = models.PositiveIntegerField(default=0, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    country = models.CharField(max_length=2, choices=Country.choices())
    name = models.CharField(max_length=50, null=False, blank=False)


class Transaction(models.Model):
    from_wallet = models.ForeignKey(
        Wallet, on_delete=models.PROTECT, null=True,
        related_name='wallet_outcome'
    )
    to_wallet = models.ForeignKey(
        Wallet, on_delete=models.PROTECT, null=True,
        related_name='wallet_income'
    )
    amount = models.PositiveIntegerField(default=0, null=False)
    status = models.CharField(
        max_length=1, choices=TransactionStatus.choices(),
        default=TransactionStatus.STARTED.value
    )
    updated_at = models.DateTimeField(auto_now=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    committed_at = models.DateTimeField(null=True)
