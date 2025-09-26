from django.db import models

from django.utils.translation import gettext_lazy as _


class Course(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Kurs nomi"))
    description = models.TextField(max_length=300, blank=True, null=True, verbose_name=_("Kurs tavsifi"))
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"

        app_label = 'common'
































