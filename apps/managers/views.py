from django.views import View
from django.shortcuts import render

from apps.common.utils import RoleAccessMixin


class ManagerHomeView(RoleAccessMixin, View):
    allowed_role = 'manager'

    def get(self, request):
        return render(request, "managers/dashboard.html")