"""
TEMPLATE FOR COMMAND

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Help Text"

    def add_arguments(self, parser):
        parser.add_argument("argument", type=int)

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(
            "test"
        ))

"""