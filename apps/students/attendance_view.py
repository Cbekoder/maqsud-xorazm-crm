from django.http import Http404
from django.shortcuts import render
from django.views import View
from django.core.paginator import Paginator

from apps.common.utils import RoleAccessMixin

from datetime import date


ATTENDANCE_STATUS_CHOICES_TRANSLATE = {
    "Present": "Keldi ✅",
    "Absent": "Kelmadi 🚫",
}
class StudentGroupAttendanceView(RoleAccessMixin, View):
    allowed_role = "student"

    def get(self, request, group_name):
        user = request.user
        if not user.user_groups.filter(group__name=group_name).exists():
            raise Http404

        user_group_attendances = (user.attendances
                                  .filter(lesson__group__name=group_name, lesson__lesson_date__lte=date.today())
                                  .order_by("-lesson__lesson_date"))

        paginator = Paginator(user_group_attendances, 5)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(
            request=request,
            template_name="students/group-attendance.html",
            context={
                "group_name": group_name,
                "page_obj": page_obj,
                "user_group_attendances": user_group_attendances,
                "ATTENDANCE_STATUS_CHOICES_TRANSLATE": ATTENDANCE_STATUS_CHOICES_TRANSLATE,
            }
        )


