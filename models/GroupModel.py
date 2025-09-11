from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import timedelta

from .UserModel import User
from .CourseModel import Course


class Group(models.Model):
    class StatusChoices(models.TextChoices):
        WAITING = "waiting", "Waiting"
        ACTIVE = "active", "Active"

    class DaysChoices(models.TextChoices):
        ODD = "odd", "Odd"
        EVEN = "even", "Even"
        CUSTOM = "custom", "Custom"

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course_groups")
    name = models.CharField(max_length=50, unique=True)
    lesson_name = models.CharField(default="Matematika")
    status = models.CharField(max_length=25, choices=StatusChoices.choices, default=StatusChoices.WAITING)

    days = models.CharField(choices=DaysChoices.choices)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)

    notes = models.TextField(max_length=300, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="created_groups")

    def set_created_by(self):
        if self._state.adding and not self.created_by:
            from crum import get_current_user
            user = get_current_user()

            if user and not user.is_anonymous:
                self.created_by = user

    def save(self, *args, **kwargs):
        self.set_created_by()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Group"
        verbose_name_plural = "Groups"

        app_label = 'common'


class CustomGroupDay(models.Model):
    class DayChoices(models.TextChoices):
        MONDAY = "mon", "Monday"
        TUESDAY = "tue", "Tuesday"
        WEDNESDAY = "wed", "Wednesday"
        THURSDAY = "thu", "Thursday"
        FRIDAY = "fri", "Friday"
        SATURDAY = "sat", "Saturday"
        SUNDAY = "sun", "Sunday"

    day = models.CharField(max_length=3, choices=DayChoices.choices)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="custom_group_days")

    def __str__(self):
        return self.day

    class Meta:
        verbose_name = "Custom Group Day"
        verbose_name_plural = "Custom Group Days"

        app_label = 'common'


class TeacherGroups(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="teacher_groups", blank=True, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="teacher_groups")
    date_joined = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Teacher Group"
        verbose_name_plural = "Teacher Groups"
        unique_together = ("teacher", "group")

        app_label = 'common'


class UserGroups(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_groups")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="user_groups")
    date_joined = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"User: {self.user}, Group: {self.group.name}"

    class Meta:
        verbose_name = "User Group"
        verbose_name_plural = "User Groups"
        unique_together = ("user", "group")

        app_label = 'common'

