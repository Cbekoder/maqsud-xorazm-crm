from django.core.management.base import BaseCommand
from datetime import date, time, timedelta
from models import Lesson, Group  # Update with your actual app name


class Command(BaseCommand):
    help = "Create lessons on specific weekdays (e.g., Tuesday, Thursday, Saturday)."

    def handle(self, *args, **options):
        # Settings
        start_date = date(2025, 7, 24)  # Starting date
        end_date = date(2025, 8, 24)    # Until this date
        group = Group.objects.get(id=2)  # Select your group
        start_time = time(12, 0)         # Lesson start time
        end_time = time(13, 30)           # Lesson end time
        lesson_name = "English"

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
                    start_time=start_time,
                    defaults={
                        "end_time": end_time,
                        "lesson_name": lesson_name,
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




