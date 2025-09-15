"""

Student list of students with same password and username and according to the pattern accordingly (studentN, StudentN)

"""


from django.core.management.base import BaseCommand

from models import User


class Command(BaseCommand):
    help = "Create list of students"

    def add_arguments(self, parser):
        parser.add_argument("start_index", type=int)
        parser.add_argument("end_index", type=int)

    def handle(self, *args, **options):
        start_index = options["start_index"]
        end_index = options["end_index"]

        student_created = 0
        student_exists = 0
        for n in range(start_index, end_index + 1):
            user, created = User.objects.get_or_create(
                username=f"student{n}",
                defaults={
                    "password": "Abc#12345",
                    "role": "student",
                    "first_name": f"Student{n}",
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
