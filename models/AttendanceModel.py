from django.db import models
from django.utils.translation import gettext_lazy as _

from .UserModel import User
from .LessonModel import Lesson


class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="attendances")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    came_at = models.DateTimeField(blank=True, null=True)
    left_at = models.DateTimeField(blank=True, null=True)
    is_present = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        app_label = 'common'

