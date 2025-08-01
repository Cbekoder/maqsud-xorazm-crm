from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel

ROLE_CHOICES = (
    ("managers", _("Admin")),
    ("teachers", _("Teacher")),
    ("students", _("Student")),
    ("parent", _("Parent")),
)


# Create your moddels here.
class User(AbstractUser, BaseModel):
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, verbose_name=_("Role"))

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
