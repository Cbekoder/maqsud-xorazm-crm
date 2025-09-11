from django.db import models
from django.utils.translation import gettext_lazy as _

from .UserModel import User
from .LessonModel import Lesson


class HomeworkGrade(models.Model):
    class ScoreChoices(models.IntegerChoices):
        ONE = 1, "1"  # first will be stored in the Database, second will be displayed (django admin or other tool)
        TWO = 2, "2"
        THREE = 3, "3"
        FOUR = 4, "4"
        FIVE = 5, "5"
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="homework_grades")
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="homework_grades")

    score = models.PositiveSmallIntegerField(choices=ScoreChoices.choices)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = _("Homework Grade")
        verbose_name_plural = _("Homework Grades")

        unique_together = ("lesson", "student")

        app_label = 'common'

