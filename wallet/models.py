# Create your models here.
from enum import StrEnum

from django.contrib.auth.models import User
from django.db import models


class Country(StrEnum):
    IRAN = 'ir'
    Canada = 'ca'

    @classmethod
    def choices(cls):
        return [
            (cls.IRAN, 'Iran'),
            (cls.Canada, 'Canada'),
        ]


class TransactionStatus(StrEnum):
    STARTED = 'S'
    COMMITTED = 'D'
    FAILED = 'F'
    PENDING = 'P'

    @classmethod
    def choices(cls):
        return [
            (cls.STARTED, 'Started'),
            (cls.COMMITTED, 'Committed'),
            (cls.FAILED, 'Failed'),
            (cls.PENDING, 'Pending'),
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


class Transaction(models.Model):
    from_wallet = models.ForeignKey(
        Wallet, on_delete=models.PROTECT, null=False,
        related_name='wallet_outcome'
    )
    to_wallet = models.ForeignKey(
        Wallet, on_delete=models.PROTECT, null=False,
        related_name='wallet_income'
    )
    amount = models.PositiveIntegerField(default=0, null=False)
    status = models.CharField(
        max_length=1, choices=TransactionStatus.choices(),
        default=TransactionStatus.STARTED
    )
    updated_at = models.DateTimeField(auto_now=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    committed_at = models.DateTimeField(null=True)
