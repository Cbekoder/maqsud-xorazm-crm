from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.html import format_html
from models import User, Notification, UserNotification, StudentParent

# unregister the default Group model
admin.site.unregister(Group)

@admin.register(User)
class UserAdmin(BaseUserAdmin, admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "first_name",
        "role",
        "photo_preview",   # ✅ show preview in list
    )
    list_display_links = ("id", "username", "first_name", "role")
    search_fields = ("id", "username", "first_name", "role")
    list_filter = ("is_active",)
    ordering = ("-id",)

    fieldsets = BaseUserAdmin.fieldsets + (
        (
            "Qo'shimcha ma'lumotlar",
            {
                "fields": (
                    "role",
                    "phone",
                    "qr_token",
                    "notification_enabled",
                    "picture",        # ✅ upload field
                    "photo_preview",  # ✅ preview inside detail page
                )
            },
        ),
    )
    readonly_fields = ("qr_token", "photo_preview")

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("Qo'shimcha ma'lumotlar", {"fields": ("role", "phone")}),
    )

    def photo_preview(self, obj):
        if obj.picture:
            return format_html(
                '<img src="{}" style="width: 50px; height:50px; object-fit: cover; border-radius: 5px;" />',
                obj.picture.url,
            )
        return "No Image"

    photo_preview.short_description = "Preview"


@admin.register(Notification)
class NotificationModelAdmin(admin.ModelAdmin):
    pass


@admin.register(UserNotification)
class UserNotificationModelAdmin(admin.ModelAdmin):
    pass


@admin.register(StudentParent)
class StudentParentModelAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "student":
            kwargs["queryset"] = User.objects.filter(role="student")
        if db_field.name == "parent":
            kwargs["queryset"] = User.objects.filter(role="parent")

        return super().formfield_for_foreignkey(db_field, request, **kwargs)
