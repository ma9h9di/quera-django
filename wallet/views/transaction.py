from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from django.views import View

from wallet.models import Wallet, Transaction, TransactionStatus, WalletUser


class IncreaseBalanceMixin:
    def increase_balance(self, wallet: Wallet, amount: int):
        with transaction.atomic():
            Transaction.objects.create(
                to_wallet=wallet,
                amount=amount,
                status=TransactionStatus.COMMITTED.value,
                committed_at=now()
            )
            wallet.balance += amount
            wallet.save()
        return JsonResponse({"message": "Balance increased", "new_balance": wallet.balance})


class DecreaseBalanceMixin:
    def decrease_balance(self, wallet: Wallet, amount: int):
        if wallet.balance < amount:
            return JsonResponse({"error": "Insufficient balance"}, status=400)
        with transaction.atomic():
            Transaction.objects.create(
                from_wallet=wallet,
                amount=amount,
                status=TransactionStatus.COMMITTED.value,
                committed_at=now()
            )
            wallet.balance -= amount
            wallet.save()
        return JsonResponse({"message": "Balance decreased", "new_balance": wallet.balance})


class TransferAmountMixin:
    def transfer_amount(self, from_wallet, to_wallet, amount):
        if from_wallet.balance < amount:
            return JsonResponse({"error": "Insufficient balance"}, status=400)

        with transaction.atomic():
            Transaction.objects.create(
                from_wallet=from_wallet,
                to_wallet=to_wallet,
                amount=amount,
                status=TransactionStatus.COMMITTED.value,
                committed_at=now()
            )
            from_wallet.balance -= amount
            from_wallet.save()
            to_wallet.balance += amount
            to_wallet.save()

        return JsonResponse({"message": "Transfer successful", "from_wallet_balance": from_wallet.balance,
                             "to_wallet_balance": to_wallet.balance})


class IncreaseBalanceView(LoginRequiredMixin, IncreaseBalanceMixin, View):
    def post(self, request, *args, **kwargs):
        wallet = get_object_or_404(Wallet, pk=request.POST.get('wallet_id'), user_id=request.user.pk)
        amount = int(request.POST.get('amount'))

        return self.increase_balance(wallet, amount)


class DecreaseBalanceView(LoginRequiredMixin, DecreaseBalanceMixin, View):
    def post(self, request, *args, **kwargs):
        wallet = get_object_or_404(Wallet, pk=request.POST.get('wallet_id'), user_id=request.user.pk)
        amount = int(request.POST.get('amount'))

        return self.decrease_balance(wallet, amount)


class TransferAmountView(LoginRequiredMixin, TransferAmountMixin, View):
    def post(self, request, *args, **kwargs):
        from_wallet = get_object_or_404(Wallet, pk=request.POST.get('from_wallet_id'), user_id=request.user.pk)
        to_wallet = get_object_or_404(Wallet, pk=request.POST.get('to_wallet_id'))
        amount = int(request.POST.get('amount'))

        return self.transfer_amount(from_wallet, to_wallet, amount)


class GetTransactionMixin:
    @staticmethod
    def get_transaction(transaction_id):
        transaction = get_object_or_404(Transaction, id=transaction_id)
        return JsonResponse({
            "id": transaction.id,
            "from_wallet": transaction.from_wallet.id,
            "to_wallet": transaction.to_wallet.id,
            "amount": transaction.amount,
            "status": transaction.status,
            "created_at": transaction.created_at,
            "updated_at": transaction.updated_at,
            "committed_at": transaction.committed_at
        })


class ListTransactionsMixin:
    @staticmethod
    def list_transactions(user: WalletUser):
        transactions = Transaction.objects.filter(
            (Q(from_wallet__user_id=user.pk) | Q(to_wallet__user_id=user.pk))
        )
        transactions_data = serializers.serialize('json', transactions)
        return JsonResponse(transactions_data, safe=False)


class TransactionView(LoginRequiredMixin, GetTransactionMixin, ListTransactionsMixin, View):
    def get(self, request, *args, **kwargs):
        transaction_id = request.GET.get('transaction_id')

        if transaction_id:
            return self.get_transaction(transaction_id)
        else:
            return self.list_transactions(user=request.user)
