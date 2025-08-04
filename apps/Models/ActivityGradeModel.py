from . import *


from .LessonModel import Lesson
from .UserModel import User


class ActivityGrades(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, related_name="activity_grades", blank=True, null=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="activity_grades")
    score = models.SmallIntegerField()
    comment = models.TextField(blank=True, null=True)


