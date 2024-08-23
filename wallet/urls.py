from django.urls import path, include

from wallet.views import wallet as wallet_views

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
]
app_name = "wallet"
urlpatterns = [
    path('wallet/', include((wallet_urlpatterns, 'wallet'), 'wallet')),
]
