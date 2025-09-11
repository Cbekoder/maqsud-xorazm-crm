import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

from apps.common.models import BaseModel


class User(AbstractUser, BaseModel):
    class RoleChoices(models.TextChoices):
        MANAGER = "manager", _("Manager")
        TEACHER = "teacher", _("Teacher")
        STUDENT = "student", _("Student")
        PARENT = "parent", _("Parent")

    phone_validator = [RegexValidator(
        regex=r'^\+?\d{9,15}$',
        message="Phone number must be in the format: '+998901234567'. Up to 15 digits allowed."
    )]

    role = models.CharField(max_length=20, choices=RoleChoices.choices, verbose_name=_("Role"))
    phone = models.CharField(max_length=15, validators=phone_validator, blank=True, null=True)
    picture = models.ImageField(upload_to="user_pictures", blank=True, null=True)
    notification_enabled = models.BooleanField(default=True)
    qr_token = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    coin = models.IntegerField(default=0)

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

        app_label = 'users'


class StudentParent(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="student_parents")
    parent = models.ForeignKey(User, on_delete=models.CASCADE, related_name="parent_students")

    class Meta:
        verbose_name = _("Student Parent")
        verbose_name_plural = _("Student Parents")
        unique_together = ("student", "parent")

        app_label = 'users'

    def __str__(self):
        return (f"S:{self.student.first_name if self.student.first_name else self.student.username} "
                f"-> P:{self.parent.first_name if self.parent.first_name else self.parent.username}")

