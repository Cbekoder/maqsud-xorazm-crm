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