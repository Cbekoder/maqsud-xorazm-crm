from django.core.management.base import BaseCommand

from models import User


class Command(BaseCommand):
    help = "Create list of students"

    def handle(self, *args, **options):
        for n in range(3, 14):
            user = User.objects.get(
                username=f"student{n}",
            )

            user.first_name = f"Student{n}"
            user.save()

        self.stdout.write(self.style.SUCCESS(
            f"Summary: Added names"
        ))