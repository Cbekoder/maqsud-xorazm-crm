from django.db import models
from django.utils.translation import gettext_lazy as _

from .UserModel import User
from .LessonModel import Lesson


class Attendance(models.Model):
    ATTENDANCE_STATUS_CHOICES = [
        ("Present", "Present"),
        ("Absent", "Absent"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="attendances")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="attendances")
    came_at = models.DateTimeField(blank=True, null=True)
    left_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=ATTENDANCE_STATUS_CHOICES, default=ATTENDANCE_STATUS_CHOICES[0][0])
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.id} | {self.lesson.group.name} | lesson_id={self.lesson.id}"

    class Meta:
        unique_together = ("user", "lesson")
        app_label = 'common'

