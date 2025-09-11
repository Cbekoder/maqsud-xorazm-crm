from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import datetime, timedelta

from .GroupModel import Group

import os


class Lesson(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="lessons")

    lesson_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(blank=True)
    topic = models.TextField(blank=True, null=True)
    lesson_video_url = models.URLField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.end_time and self.start_time:
            dt = datetime.combine(datetime.today(), self.start_time)
            dt_end = dt + timedelta(hours=1, minutes=30)
            self.end_time = dt_end.time()

        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.group.lesson_name} | {self.group} ({self.lesson_date}) [{self.start_time} - {self.end_time}]"

    class Meta:
        verbose_name = _("Lesson")
        verbose_name_plural = _("Lessons")

        unique_together = ("group", "lesson_date", "start_time")

        app_label = 'common'


class ClassMaterial(models.Model):
    lesson = models.ForeignKey(to=Lesson, on_delete=models.CASCADE, related_name="class_materials")
    material = models.FileField(
        upload_to="students/lesson_materials/class_materials",
        blank=True,
        null=True
    )

    def __str__(self):
        return os.path.basename(self.material.name)

    class Meta:
        verbose_name = _("Class Material")
        verbose_name_plural = _("Class Materials")

        app_label = 'common'

class HomeworkMaterial(models.Model):
    lesson = models.ForeignKey(to=Lesson, on_delete=models.CASCADE, related_name="homework_materials")
    material = models.FileField(
        upload_to="students/lesson_materials/homework_materials",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = _("Homework Material")
        verbose_name_plural = _("Homework Materials")

        app_label = 'common'

