from . import *

from .UserModel import User
from .LessonModel import Lesson


GRADE_TYPE_CHOICES = [
    ("Stars", "Stars"),
    ("Percent", "Percent"),
]


class HomeworkGrade(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="homework_grades")
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="homework_grades")

    grade_type = models.CharField(max_length=50, choices=GRADE_TYPE_CHOICES, blank=True, null=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)


