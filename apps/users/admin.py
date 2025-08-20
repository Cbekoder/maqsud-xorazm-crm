from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.html import format_html
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
        "photo_preview",   # ✅ show preview in list
    )
    list_display_links = ("id", "username", "first_name", "last_name")
    search_fields = ("id", "username", "first_name", "last_name")
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
