from django.dispatch import receiver
from django.db.models.signals import post_save

from models import Group, Lesson, CustomGroupDay

from datetime import timedelta


@receiver(post_save, sender=Group)
def create_lessons_for_group(sender, instance, created, **kwargs):
    """
    When a new group is created, automatically generate Lesson objects.
    """

    if created and instance.start_date and instance.end_date:
        current_date = instance.start_date

        while current_date <= instance.end_date:
            if instance.days == Group.DaysChoices.ODD and current_date.weekday() in [0, 2, 4]:
                Lesson.objects.get_or_create(
                    group=instance,
                    lesson_date=current_date,
                    start_time=instance.start_time,
                    end_time=instance.end_time,
                )

            elif instance.days == Group.DaysChoices.EVEN and current_date.weekday() in [1, 3, 5]:
                Lesson.objects.get_or_create(
                    group=instance,
                    lesson_date=current_date,
                    start_time=instance.start_time,
                    end_time=instance.end_time,
                )

            current_date += timedelta(days=1)


@receiver(post_save, sender=CustomGroupDay)
def create_custom_day_lesson(sender, instance, created, **kwargs):
    weekday_indexes = {
        CustomGroupDay.DayChoices.MONDAY: 0,
        CustomGroupDay.DayChoices.TUESDAY: 1,
        CustomGroupDay.DayChoices.WEDNESDAY: 2,
        CustomGroupDay.DayChoices.THURSDAY: 3,
        CustomGroupDay.DayChoices.FRIDAY: 4,
        CustomGroupDay.DayChoices.SATURDAY: 5,
        CustomGroupDay.DayChoices.SUNDAY: 6
    }

    if created and instance.group.start_date and instance.group.end_date:
        current_date = instance.group.start_date

        while current_date <= instance.group.end_date:
            day_index = weekday_indexes.get(instance.day)

            if current_date.weekday() == day_index:
                Lesson.objects.get_or_create(
                    group=instance.group,
                    lesson_date=current_date,
                    start_time=instance.group.start_time,
                    end_time=instance.group.end_time,
                )

            current_date += timedelta(days=1)


