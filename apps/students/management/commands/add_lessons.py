"""
Adding multiple lessons is <deprecated> since
automation of lesson creation added

Single item can be added through admin panel
"""


from django.core.management.base import BaseCommand
from datetime import date, time, timedelta
from models import Lesson, Group  # Update with your actual app name


class Command(BaseCommand):
    help = "Create lessons on specific weekdays (e.g., Tuesday, Thursday, Saturday)."

    def add_arguments(self, parser):
        parser.add_argument()

    def handle(self, *args, **options):
        # Settings
        start_date = date(2025, 9, 1)  # Starting date
        end_date = date(2025, 9, 10)    # Until this date
        group = Group.objects.get(id=14)  # Select your group

        # Weekdays we want → Tuesday=1, Thursday=3, Saturday=5
        target_weekdays = [0, 2, 4]

        current_date = start_date
        created_count = 0
        skipped_count = 0

        while current_date <= end_date:
            if current_date.weekday() in target_weekdays:
                # Try to create a new lesson
                lesson, created = Lesson.objects.get_or_create(
                    group=group,
                    lesson_date=current_date,
                    start_time=group.start_time,
                    defaults={
                        "end_time": group.end_time,
                    }
                )

                if created:
                    created_count += 1
                    self.stdout.write(self.style.SUCCESS(f"Added lesson on {current_date}"))
                else:
                    skipped_count += 1
                    self.stdout.write(self.style.WARNING(f"Lesson already exists on {current_date}"))

            # Go to the next day
            current_date += timedelta(days=1)

        # Final summary
        self.stdout.write(self.style.SUCCESS(
            f"\nDone! {created_count} lessons added, {skipped_count} skipped."
        ))




