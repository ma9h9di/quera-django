from django.core.management.base import BaseCommand

from wallet.models import Wallet


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        parser.add_argument("balance", type=int, help="Wallet initial balance")
        parser.add_argument("--name", type=str)
        parser.add_argument("--user_id", type=int)
        parser.add_argument("--country", choices=['ca', 'ir'], nargs='?', default='ir')

    def handle(
            self,
            *args,
            balance: int,
            name: str,
            user_id: int,
            country: str,
            **options
    ):
        Wallet.objects.create(
            balance=balance,
            name=name,
            user_id=user_id,
            country=country
        )
