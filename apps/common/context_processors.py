from django.conf import settings

def global_context(request):
    return {
        'PROJECT_NAME': 'LCRM System',
        'COMPANY_NAME': 'MyCompany.uz',
        'CURRENT_PATH': request.path,
        'IS_ADMIN': request.path.startswith('/managers/'),
        'SUPPORT_EMAIL': 'support@mycompany.uz',
        'FOOTER_YEAR': 2025,  # yoki dynamic bo‘lishi uchun datetime.now().year
        'DEBUG_MODE': settings.DEBUG,
    }


def auth_user_notifications_context(request):
    user_notification_enabled = request.user.notification_enabled
    context = {
        "user_notifications": [],
        "user_notification_enabled": user_notification_enabled,
    }

    if request.user.is_authenticated:
        if user_notification_enabled:
            context["user_notifications"] = request.user.user_notifications.filter(is_read=False, is_archived=False)

    return context



