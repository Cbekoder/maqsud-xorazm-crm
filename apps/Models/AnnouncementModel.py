from . import *

from .UserModel import User


class Announcement(models.Model):
    created_by = models.ForeignKey(to=User, on_delete=models.SET_NULL, related_name="announcements", blank=True, null=True)

    title = models.CharField(max_length=100)
    message = models.TextField(max_length=500)
    sent_at = models.DateTimeField(auto_now_add=True)
    is_global = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Announcement")
        verbose_name_plural = _("Announcements")

