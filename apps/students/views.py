from django.views import View
from django.shortcuts import render

from apps.common.utils import RoleAccessMixin


class StudentHomeView(RoleAccessMixin, View):
    allowed_role = 'student'

    def get(self, request):
        return render(request, "students/dashboard.html")


class StudentScheduleView(RoleAccessMixin, View):
    allowed_role = 'student'

    def get(self, request):
        return render(request, "students/schedule.html")


class StudentProgressView(RoleAccessMixin, View):
    allowed_role = 'student'

    def get(self, request):
        return render(request, "students/progress.html")


class StudentAttendanceView(RoleAccessMixin, View):
    allowed_role = 'student'

    def get(self, request):
        return render(request, "students/attendance.html")
