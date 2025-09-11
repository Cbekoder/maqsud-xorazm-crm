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
        'USER': request.user if request.user.is_authenticated else None,
    }


def auth_user_notifications_context(request):
    context = {
        "user_notifications": [],
        "user_notification_enabled": True,
    }

    if request.user.is_authenticated:
        context["user_notifications"] = request.user.user_notifications.filter(is_read=False, is_archived=False)
        context["user_notification_enabled"] = request.user.notification_enabled

    return context


def student_context(request):
    context = {
        "active_tab": request.GET.get("active_tab")
    }

    return context


