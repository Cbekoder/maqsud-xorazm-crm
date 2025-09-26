import uuid

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView

from apps.common.utils import RoleAccessMixin

from models import User, Attendance, Lesson, Group, Course
from .forms import CourseForm

from datetime import datetime


class ManagerAccessMixin(RoleAccessMixin):
    allowed_role = "manager"


class ManagerHomeView(RoleAccessMixin, View):
    allowed_role = 'manager'

    def get(self, request):
        return render(request, "managers/dashboard.html")


class GroupListView(RoleAccessMixin, View):
    allowed_role = 'manager'

    def get(self, request):
        context = {
            "groups": Group.objects.all()
        }

        return render(request, "managers/groups.html", context)


class GroupLessonsListView(RoleAccessMixin, View):
    allowed_role = 'manager'

    def get(self, request, group_name):
        context = {}

        group = Group.objects.get(name=group_name)
        group_lessons = group.lessons.all()
        context["group_lessons"] = group_lessons

        return render(request, "managers/group-lessons.html", context)


class EnterLessonAttendance(RoleAccessMixin, View):
    allowed_role = 'manager'

    def get(self, request, lesson_id):
        context = {"lesson_id": lesson_id}

        return render(request, "managers/enter-lesson-attendance.html", context)


class ExitLessonAttendance(RoleAccessMixin, View):
    allowed_role = 'manager'

    def get(self, request, lesson_id):
        context = {"lesson_id": lesson_id}

        return render(request, "managers/exit-lesson-attendance.html", context)


def response(status_code, status_str, msg, name=None, image=None):
    json_response = JsonResponse(
        {
            "status": status_str,
            "msg": msg,
            "name": name,
            "image": image
        },
        status=status_code,
    )

    return json_response

def handle_token_exceptions(token):
    if not token:
        return response(400, "warning", "No QR code detected")

    try:
        uuid_obj = uuid.UUID(token, version=4)
    except ValueError:
        return response(400, "warning", "Invalid QR code format")

    try:
        User.objects.get(qr_token=str(uuid_obj))
        return True
    except User.DoesNotExist:
        return response(404, "warning", "Student not identified")


def handle_student_not_in_group_exception(lesson: Lesson, student: User):
    if not Lesson.objects.filter(id=lesson.id, group__user_groups__user=student).exists():
        return response(400, "warning", "O'quvchida bu dars yo'q!")

    return True

def handle_time_exception(lesson: Lesson):
    now = datetime.now()
    now_date = now.date()
    now_time = now.time()

    if lesson.lesson_date != now_date:
        return response(400, "warning", "Davomatni DARS SANASIDA qilish shart!")

    # Time check
    if now_time < lesson.start_time or now_time > lesson.end_time:
        return response(400, "warning", "Davomatni DARS VAQTIDA qilish shart!")

    return True


def check_enter_qr(request, lesson_id):
    token = request.GET.get("uuid")

    token_exception_response = handle_token_exceptions(token)
    if token_exception_response is not True:
        return token_exception_response

    uuid_obj = uuid.UUID(token, version=4)

    student = User.objects.get(qr_token=str(uuid_obj))
    lesson = Lesson.objects.get(pk=lesson_id)

    # Exception handling
    not_in_group_exception_response = handle_student_not_in_group_exception(lesson, student)
    if not_in_group_exception_response is not True:
        return not_in_group_exception_response

    # Exception handling
    time_exception_response = handle_time_exception(lesson)
    if time_exception_response is not True:
        return time_exception_response

    attendance, created = Attendance.objects.get_or_create(
        user=student,
        lesson=lesson,
    )

    if attendance.came_at:
        return response(
            status_code=400,
            status_str="dark",
            msg="O'quvchi kelish davomati qilingan!",
            name=student.get_full_name() or student.username,
            image=getattr(student, "picture_url", None)
        )

    attendance.came_at = datetime.now()
    attendance.save()

    return response(
        status_code=200,
        status_str="success",
        msg="O'quvchi kelish davomati qilindi!",
        name=student.get_full_name() or student.username,
        image=getattr(student, "picture_url", None)
    )


def check_exit_qr(request, lesson_id):
    token = request.GET.get("uuid")
    exception_response = handle_token_exceptions(token)

    if not exception_response:
        return exception_response

    uuid_obj = uuid.UUID(token, version=4)
    student = User.objects.get(qr_token=str(uuid_obj))
    lesson = Lesson.objects.get(pk=lesson_id)

    try:
        attendance = Attendance.objects.get(user=student, lesson=lesson)
    except Attendance.DoesNotExist:
        return response(
            status_code=404,
            status_str="warning",
            msg="Birinchi kelish davomatini qiling!",
            name=student.get_full_name() or student.username,
            image=getattr(student, "picture_url", None)
        )

    if attendance.left_at:
        return response(
            status_code=400,
            status_str="dark",
            msg="O'quvchi ketish davomati qilingan!",
            name=student.get_full_name() or student.username,
            image=getattr(student, "picture_url", None)
        )

    attendance.left_at = datetime.now()
    attendance.save()

    return response(
        status_code=200,
        status_str="success",
        msg="O'quvchi ketish davomati qilindi!",
        name=student.get_full_name() or student.username,
        image=getattr(student, "picture_url", None)
    )


class ManagerCourseListView(RoleAccessMixin, View):
    allowed_role = "manager"
    template_name = "managers/courses/course-list.html"

    def get_context_data(self):
        context = {}

        courses = Course.objects.all()
        context["courses"] = courses

        return context

    def get(self, request):
        form = CourseForm()

        context = self.get_context_data()
        context["course_form"] = form

        return render(request, self.template_name, context)

    def post(self, request):
        form = CourseForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect(request.META.get("HTTP_REFERER", "manager_course_list"))

        context = self.get_context_data()
        context["course_form"] = form

        return render(request, self.template_name, context)


class ManagerEditCourseView(RoleAccessMixin, UpdateView):
    allowed_role = "manager"
    model = Course
    form_class = CourseForm
    template_name = "managers/courses/edit-course.html"
    pk_url_kwarg = "course_id"
    success_url = reverse_lazy("manager_course_list")


@method_decorator(require_POST, name="dispatch")
class ManagerDeleteCourseView(RoleAccessMixin, View):
    allowed_role = "manager"

    def post(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        course.delete()
        return JsonResponse({"success": True, "message": "Course deleted"})

