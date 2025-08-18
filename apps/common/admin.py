from django.contrib import admin
from apps.common.models import VersionHistory

from models import Lesson, Group, UserGroups, Attendance


@admin.register(VersionHistory)
class VersionHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "version", "required", "created_at", "updated_at")
    list_display_links = ("id", "version")
    list_filter = ("required",)
    search_fields = ("version",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(Group)
class GroupModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Lesson)
class LessonModelAdmin(admin.ModelAdmin):
    pass


@admin.register(UserGroups)
class UserGroupsModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Attendance)
class AttendanceModelAdmin(admin.ModelAdmin):
    pass
