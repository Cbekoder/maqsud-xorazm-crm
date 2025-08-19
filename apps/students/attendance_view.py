import json
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model
from models import Attendance, Lesson

from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

User = get_user_model()

def staff_required(u):  # change to your permission logic
    return u.is_authenticated and (u.is_staff or u.is_superuser)

@login_required
@user_passes_test(staff_required)
def scan_attendance(request, lesson_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    return render(request, "students/scan.html", {"lesson": lesson})

@login_required
@user_passes_test(staff_required)
@require_POST
def api_mark_attendance(request):
    # Accept JSON body: { "token": "...", "lesson_id": 123 }
    try:
        payload = json.loads(request.body.decode("utf-8"))
        token = payload.get("token")
        lesson_id = int(payload.get("lesson_id"))
    except Exception:
        return JsonResponse({"ok": False, "error": "Bad JSON"}, status=400)

    if not token or not lesson_id:
        return JsonResponse({"ok": False, "error": "token and lesson_id required"}, status=400)

    lesson = get_object_or_404(Lesson, pk=lesson_id)

    try:
        student = User.objects.get(qr_token=token)
    except User.DoesNotExist:
        return JsonResponse({"ok": False, "error": "Invalid QR"}, status=404)

    obj, created = Attendance.objects.get_or_create(
        student=student,
        lesson=lesson,
        defaults={"status": Attendance.PRESENT},
    )

    if created:
        return JsonResponse({"ok": True, "status": "marked", "student": student.get_full_name() or student.username})
    else:
        return JsonResponse({"ok": True, "status": "already_marked", "student": student.get_full_name() or student.username})


ATTENDANCE_STATUS_CHOICES_TRANSLATE = {
    "Present": "Keldi",
    "Absent": "Kelmadi",
}
class StudentGroupAttendanceView(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request, group_name):
        user = request.user
        if not user.user_groups.filter(group__name=group_name).exists():
            raise Http404

        user_group_attendances = user.attendances.all().filter(lesson__group__name=group_name)

        return render(
            request=request,
            template_name="students/group_attendance.html",
            context={
                "group_name": group_name,
                "user_group_attendances": user_group_attendances,
                "ATTENDANCE_STATUS_CHOICES_TRANSLATE": ATTENDANCE_STATUS_CHOICES_TRANSLATE,
            }
        )


