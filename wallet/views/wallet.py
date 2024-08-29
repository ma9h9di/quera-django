from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError
from django.http import HttpRequest, HttpResponse, Http404, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from wallet.forms.wallet import WalletCreateForm, WalletUpdateForm
from wallet.models import Wallet


@csrf_exempt
@require_POST
def create(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = WalletCreateForm(request.POST, user=request.user)
        if form.is_valid():
            form.save(commit=True)

            return redirect('finance:wallet:list-wallets')  # Redirect to a list or detail view
    else:
        form = WalletCreateForm()

    return render(request, 'wallet/wallet_form.html', {'form': form, 'action': 'Create'})


@login_required
def list_of_wallets(request: HttpRequest) -> HttpResponse:
    all_wallets = Wallet.objects.filter(user=request.user).values('id', 'balance', 'name')
    context = {
        'object_list': all_wallets,
    }
    return render(
        request,
        "wallet/list_of_wallets.html",
        context,
    )


def get(request: HttpRequest, pk: int) -> HttpResponse:
    try:
        worker_wallet = Wallet.objects.get(pk=pk)
    except Wallet.DoesNotExist:
        raise Http404
    context = {
        'object': worker_wallet,
    }
    return render(
        request,
        "wallet/wallet_details.html",
        context,
    )


def update(request: HttpRequest, pk: int) -> HttpResponse:
    wallet = get_object_or_404(Wallet, pk=pk)

    if request.method == 'POST':
        form = WalletUpdateForm(request.POST, instance=wallet)
        if form.is_valid():
            form.save()
            return redirect('finance:wallet:get-wallet', pk=wallet.pk)  # Redirect to detail view or another page
    else:
        form = WalletUpdateForm(instance=wallet)

    return render(request, 'wallet/wallet_form.html', {'form': form, 'action': 'Update'})


def delete(request: HttpRequest, pk: int) -> HttpResponse:
    worker_wallet = Wallet.objects.get(pk=pk)
    context = {
        'object': worker_wallet,
    }
    try:
        worker_wallet.delete()
    except ProtectedError as e:
        return HttpResponseBadRequest(str(e))

    return render(
        request,
        "wallet/wallet_delete.html",
        context,
    )


class WalletGenericListView(LoginRequiredMixin, generic.ListView):
    model = Wallet
    template_name = 'wallet/list_of_wallets.html'


class WalletGenericDetailView(LoginRequiredMixin, generic.DetailView):
    model = Wallet
    template_name = 'wallet/wallet_details.html'
    pk_url_kwarg = 'pk'


class WalletGenericCreateView(generic.CreateView):
    model = Wallet
    template_name = 'wallet/wallet_form.html'
    fields = ['balance', 'country', 'name']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class WalletGenericUpdateView(generic.UpdateView):
    model = Wallet
    template_name = 'wallet/wallet_form.html'
    fields = ['balance', 'country', 'name']


class WalletGenericDeleteView(generic.DeleteView):
    model = Wallet
    success_url = reverse_lazy("finance:wallet:list-wallets")
