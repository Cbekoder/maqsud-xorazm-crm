from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import datetime, timedelta

from .GroupModel import Group


class Lesson(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="lessons")

    lesson_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(blank=True)
    lesson_name = models.CharField(default="Matematika")
    topic = models.TextField(blank=True, null=True)
    material = models.FileField(upload_to="lesson_materials", blank=True, null=True)
    lesson_video_url = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.start_time:
            dt = datetime.combine(datetime.today(), self.start_time)
            dt_end = dt + timedelta(hours=1, minutes=30)
            self.end_time = dt_end.time()

        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.lesson_name} | {self.group} [{self.start_time} - {self.end_time}]"

    class Meta:
        verbose_name = _("Lesson")
        verbose_name_plural = _("Lessons")

        app_label = 'common'

