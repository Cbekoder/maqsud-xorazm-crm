from django.core.management.base import BaseCommand

from models import User


class Command(BaseCommand):
    help = "Create list of students"

    def handle(self, *args, **options):
        student_created = 0
        student_exists = 0
        for n in range(3, 14):
            user, created = User.objects.get_or_create(
                username=f"student{n}",
                defaults={
                    "password": "Abc#12345",
                    "role": "student",
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(
                    "student added"
                ))
                student_created += 1
            else:
                self.stdout.write(self.style.WARNING(
                    "student exists"
                ))

                student_exists += 1

        self.stdout.write(self.style.SUCCESS(
            f"Summary: Added {student_created}, exists {student_exists}"
        ))
