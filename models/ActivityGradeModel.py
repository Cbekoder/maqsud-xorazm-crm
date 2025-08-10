from django.db import models
from django.utils.translation import gettext_lazy as _


from .LessonModel import Lesson
from .UserModel import User


class ActivityGrade(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, related_name="activity_grades", blank=True, null=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="activity_grades")
    score = models.SmallIntegerField()
    comment = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = _("Activity Grade")
        verbose_name_plural = _("Activity Grades")

        app_label = 'common'

