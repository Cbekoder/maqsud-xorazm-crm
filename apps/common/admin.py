from django.contrib import admin
from apps.common.models import VersionHistory

from models import (User, Lesson, Group, UserGroups, Attendance, ActivityGrade, HomeworkGrade,
                    ClassMaterial, HomeworkMaterial,
                    TeacherGroups, Course, Room, CustomGroupDay)


@admin.register(VersionHistory)
class VersionHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "version", "required", "created_at", "updated_at")
    list_display_links = ("id", "version")
    list_filter = ("required",)
    search_fields = ("version",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(Group)
class GroupModelAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "created_by":
            kwargs["queryset"] = User.objects.filter(role="manager")

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(CustomGroupDay)
class CustomGroupDayModelAdmin(admin.ModelAdmin):
    list_display = ("day", "group")


@admin.register(Course)
class CourseModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Room)
class RoomModelAdmin(admin.ModelAdmin):
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


@admin.register(ActivityGrade)
class ActivityGradeModelAdmin(admin.ModelAdmin):
    list_display = ("lesson", "student", "score", "comment")


@admin.register(HomeworkGrade)
class HomeworkGradeModelAdmin(admin.ModelAdmin):
    list_display = ("lesson", "student", "score", "comment")


@admin.register(ClassMaterial)
class ClassMaterialModelAdmin(admin.ModelAdmin):
    pass


@admin.register(HomeworkMaterial)
class HomeworkMaterialModelAdmin(admin.ModelAdmin):
    pass


# FOR TEACHER
@admin.register(TeacherGroups)
class TeacherGroupsModelAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "teacher":
            kwargs["queryset"] = User.objects.filter(role="teacher")

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

