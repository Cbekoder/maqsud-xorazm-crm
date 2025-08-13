from django.views import View
from django.shortcuts import render

from apps.common.utils import RoleAccessMixin

class ParentHomeView(RoleAccessMixin, View):
    allowed_role = 'parent'

    def get(self, request):
        return render(request, "parents/dashboard.html")
