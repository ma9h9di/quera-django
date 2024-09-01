from django.test import TestCase
from model_bakery import baker

from wallet.models import Wallet, WalletUser, Country


class WalletTestCase(TestCase):

    def setUp(self) -> None:
        self.user = baker.make(WalletUser, username='mahdi')
        self.wallet = baker.make(Wallet, user=self.user)

    def tearDown(self) -> None:
        self.wallet.delete()
        self.user.delete()

    def test_add_wallet(self):
        self.assertEqual(Wallet.objects.count(), 1)
        Wallet.objects.create(
            user=self.user,
            balance=2323213,
            name="test-test",
            country=Country.IRAN.value
        )
        self.assertEqual(Wallet.objects.count(), 2)

    def test_add_wallet_2(self):
        self.assertEqual(Wallet.objects.count(), 1)
        Wallet.objects.using("sqlite").create(
            user=self.user,
            balance=2323213,
            name="test-test",
            country=Country.IRAN.value
        )
        self.assertEqual(Wallet.objects.count(), 2)
