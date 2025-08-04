from . import *

from django.contrib.auth.models import AbstractUser

from apps.common.models import BaseModel


ROLE_CHOICES = (
    ("managers", _("Admin")),
    ("teachers", _("Teacher")),
    ("students", _("Student")),
    ("parent", _("Parent")),
)


class User(AbstractUser, BaseModel):
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, verbose_name=_("Role"))
    phone = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

