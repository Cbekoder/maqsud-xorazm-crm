from django.db import models
from django.utils.translation import gettext_lazy as _

from .UserModel import User


class Notification(models.Model):
    created_by = models.ForeignKey(to=User, on_delete=models.SET_NULL, related_name="notifications_created_by", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    title = models.CharField(max_length=100)
    message = models.TextField(max_length=500)
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")

        app_label = 'users'


class UserNotification(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_notifications")

    class Meta:
        verbose_name = _("User Notification")
        verbose_name_plural = _("User Notifications")

        app_label = 'users'


