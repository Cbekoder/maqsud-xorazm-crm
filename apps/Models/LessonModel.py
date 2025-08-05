from . import *

from .GroupModel import Group


class Lesson(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="lessons")

    lesson_date_time = models.DateTimeField(blank=True)
    topic = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


