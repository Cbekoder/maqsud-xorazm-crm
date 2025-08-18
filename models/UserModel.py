import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import AbstractUser

from apps.common.models import BaseModel


ROLE_CHOICES = (
    ("manager", _("Manager")),
    ("teacher", _("Teacher")),
    ("student", _("Student")),
    ("parent", _("Parent")),
)


class User(AbstractUser, BaseModel):
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, verbose_name=_("Role"))
    phone = models.CharField(max_length=15, blank=True, null=True)
    notification_enabled = models.BooleanField(default=True)
    qr_token = models.UUIDField(unique=True, editable=False, blank=True, null=True)

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

        app_label = 'users'


