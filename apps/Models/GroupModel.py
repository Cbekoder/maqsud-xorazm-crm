from . import *

from .UserModel import User


class Group(models.Model):
    name = models.CharField(max_length=50)
    schedule = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class TeacherGroups(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="groups", blank=True, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

