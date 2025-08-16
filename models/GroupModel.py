from django.db import models
from django.utils.translation import gettext_lazy as _

from .UserModel import User


class Group(models.Model):
    name = models.CharField(max_length=50)
    schedule = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Group"
        verbose_name_plural = "Groups"
        unique_together = ("name", "schedule")

        app_label = 'common'


class TeacherGroups(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="teacher_groups", blank=True, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Teacher Group"
        verbose_name_plural = "Teacher Groups"
        unique_together = ("teacher", "group")

        app_label = 'common'


class UserGroups(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="user_groups", blank=True, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return f"User: {self.user.username}, Group: {self.group.name}"

    class Meta:
        verbose_name = "User Group"
        verbose_name_plural = "User Groups"
        unique_together = ("user", "group")

        app_label = 'common'

