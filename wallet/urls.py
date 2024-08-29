from django.contrib.auth import views as auth_views
from django.urls import include
from django.urls import path

from wallet.views import user as user_views
from wallet.views import wallet as wallet_views
from wallet.views.transaction import IncreaseBalanceView, DecreaseBalanceView, TransferAmountView, TransactionView
from wallet.views.wallet import WalletGenericListView, WalletGenericDetailView, WalletGenericDeleteView, \
    WalletGenericCreateView, WalletGenericUpdateView

user_urlpatterns = [
    path('signup/', user_views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='finance:user:login'), name='logout'),
    # other paths
]

wallet_generic_urlpatterns = [
    path("create/", WalletGenericCreateView.as_view(), name='create-wallet'),
    path("list/", WalletGenericListView.as_view(), name='list-wallets'),
    path(
        "<int:pk>/",
        include(
            [
                path("delete/", WalletGenericDeleteView.as_view(), name='delete-wallet'),
                path("update/", WalletGenericUpdateView.as_view(), name='update-wallet'),
                path("details/", WalletGenericDetailView.as_view(), name='get-wallet'),
            ]
        ),
    ),

]
wallet_urlpatterns = [
    path("create/", wallet_views.create, name='create-wallet'),
    path("list/", wallet_views.list_of_wallets, name='list-wallets'),
    path(
        "<int:pk>/",
        include(
            [
                path("delete/", wallet_views.delete, name='delete-wallet'),
                path("update/", wallet_views.update, name='update-wallet'),
                path("details/", wallet_views.get, name='get-wallet'),
            ]
        ),
    ),
    path('generic/', include((wallet_generic_urlpatterns, 'generic'), namespace='generic')),

]

transaction_urlpatterns = [
    path('increase-balance/', IncreaseBalanceView.as_view(), name='increase_balance'),
    path('decrease-balance/', DecreaseBalanceView.as_view(), name='decrease_balance'),
    path('transfer/', TransferAmountView.as_view(), name='transfer'),
    path('transactions/', TransactionView.as_view(), name='transactions'),

]

app_name = "wallet"
urlpatterns = [
    path('wallet/', include((wallet_urlpatterns, 'wallet'), namespace='wallet')),
    path('user/', include((user_urlpatterns, 'user'), namespace='user')),
    path('transaction/', include((transaction_urlpatterns, 'transaction'), namespace='transaction')),
]
