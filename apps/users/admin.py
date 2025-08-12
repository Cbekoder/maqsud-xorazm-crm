from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from models import User, Notification, UserNotification

# unregister the default Group model
admin.site.unregister(Group)

@admin.register(User)
class UserAdmin(BaseUserAdmin, admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "first_name",
        "last_name",
    )
    list_display_links = ("id", "username", "first_name", "last_name")
    search_fields = ("id", "username", "first_name", "last_name")
    list_filter = ("is_active",)
    ordering = ("-id",)

    fieldsets = BaseUserAdmin.fieldsets + (
        ("Qo'shimcha ma'lumotlar", {"fields": ("role", "phone")}),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("Qo'shimcha ma'lumotlar", {"fields": ("role", "phone")}),
    )


@admin.register(Notification)
class NotificationModelAdmin(admin.ModelAdmin):
    pass


@admin.register(UserNotification)
class UserNotificationModelAdmin(admin.ModelAdmin):
    pass
