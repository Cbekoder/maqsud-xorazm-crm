import uuid

from django.http import JsonResponse
from django.views import View
from django.shortcuts import render
from django.views.generic import TemplateView

from apps.common.utils import RoleAccessMixin
from apps.users.models import User


class ManagerHomeView(RoleAccessMixin, View):
    allowed_role = 'manager'

    def get(self, request):
        return render(request, "managers/dashboard.html")


class QRScannerView(RoleAccessMixin, TemplateView):
    allowed_role = 'manager'
    template_name = "managers/scanner.html"


def check_scanned_QR(request):
    token = request.GET.get("uuid")
    if not token:
        return JsonResponse({
            "status": "warning",
            "msg": "No QR code detected"
        }, status=400)
    try:
        uuid_obj = uuid.UUID(token, version=4)
    except ValueError:
        return JsonResponse({
            "status": "warning",
            "msg": "Invalid QR code format"
        }, status=400)
    try:
        student = User.objects.get(qr_token=str(uuid_obj))
    except User.DoesNotExist:
        return JsonResponse({
            "status": "warning",
            "msg": "Student not identified"
        }, status=404)

    # TODO: real timetable / attendance check
    has_lesson = True
    if not has_lesson:
        return JsonResponse({
            "status": "dark",
            "msg": "Student has no lessons today"
        }, status=200)

    # Example: mark attendance here
    # Attendance.objects.create(student=student, date=timezone.now())

    return JsonResponse({
        "status": "success",
        "name": student.get_full_name() or student.username,
        "image": getattr(student, "picture_url", None),  # if you have a profile image field
        "msg": f"{student.username} marked as present"
    }, status=200)