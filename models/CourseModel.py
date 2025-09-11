from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"

        app_label = 'common'
































