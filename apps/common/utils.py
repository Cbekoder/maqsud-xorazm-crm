from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin

ROLE_DASHBOARD_MAP = {
    "student": "/student/",
    "teacher": "/teacher/",
    "manager": "/manager/",
    "parent": "/parent/",
}

class RoleAccessMixin(LoginRequiredMixin):
    login_url = '/users/login/'
    redirect_field_name = 'next'
    allowed_role = None  # 'student', 'teacher', etc.

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        # If the user doesn't have the allowed role → redirect to their own dashboard
        if request.user.role != self.allowed_role:
            return redirect(ROLE_DASHBOARD_MAP.get(request.user.role, '/'))

        return super().dispatch(request, *args, **kwargs)
