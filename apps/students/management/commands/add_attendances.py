"""
ex.: py manage.py add_attendances 7 164:Present 165:Present 166:Present

--- first argument under 7 is -> user_id
--- second argument under key:value pairs are lesson_id:attendance_status

"""


from django.core.management.base import BaseCommand

from models import Attendance, Lesson, User


class Command(BaseCommand):
    help = "Create attendances to lessons"

    def add_arguments(self, parser):
        parser.add_argument("student_id", type=int)
        parser.add_argument(
            "pairs",
            nargs="+",
            help="Lesson and status pairs in the format lesson_id:status",
        )

    def handle(self, *args, **options):
        student_id = options["student_id"]
        pairs = options["pairs"]

        added, exists = 0, 0
        for pair in pairs:
            try:
                lesson_id, status = pair.split(":")
                lesson_id = int(lesson_id)

                lesson = Lesson.objects.get(pk=lesson_id)
                user = User.objects.get(pk=student_id)
                attendance, created = Attendance.objects.get_or_create(
                    user=user,
                    lesson=lesson,
                    defaults={
                        "status": status
                    }
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(
                        "Attendance added"
                    ))
                    added += 1
                else:
                    self.stdout.write(self.style.WARNING(
                        "Attendance exists"
                    ))
                    exists += 1
            except ValueError:
                self.stdout.write(self.style.ERROR(
                    f"Invalid pair format: {pair}. Use lesson_id:status"
                ))
            except Lesson.DoesNotExist:
                self.stdout.write(self.style.ERROR(
                    f"Lesson {lesson_id} does not exist."
                ))

        self.stdout.write(self.style.SUCCESS(
            f"Attendances added: {added}, Attendances exist: {exists}"
        ))


