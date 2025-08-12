from django.views import View
from django.shortcuts import render

from apps.common.utils import RoleAccessMixin


class TeacherHomeView(RoleAccessMixin, View):
    allowed_role = 'teacher'

    def get(self, request):
        return render(request, "teachers/dashboard.html")
