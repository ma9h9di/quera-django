from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from wallet.models import Wallet


def create(request: HttpRequest) -> HttpResponse:
    pass


def list_of_wallets(request: HttpRequest) -> HttpResponse:
    all_wallets = Wallet.objects.all().values('id', 'balance', 'name')
    context = {
        'my_wallets': all_wallets,
    }
    return render(
        request,
        "wallet/list_of_wallets.html",
        context,
    )


def get(request: HttpRequest, pk: int) -> HttpResponse:
    worker_wallet = Wallet.objects.get(pk=pk)
    context = {
        'wallet': worker_wallet,
    }
    return render(
        request,
        "wallet/wallet_details.html",
        context,
    )


def update(request: HttpRequest, pk: int) -> HttpResponse:
    pass


def delete(request: HttpRequest, pk: int) -> HttpResponse:
    worker_wallet = Wallet.objects.get(pk=pk)
    context = {
        'wallet': worker_wallet,
    }
    worker_wallet.delete()
    return render(
        request,
        "wallet/wallet_delete.html",
        context,
    )
