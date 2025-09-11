from django.views import View
from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import F, Value, Prefetch
from django.db.models.functions import NullIf
from django.http import Http404

from apps.common.utils import RoleAccessMixin
from models import Lesson, Group, CustomGroupDay, User, UserGroups, TeacherGroups

from datetime import date


class TeacherHomeView(RoleAccessMixin, View):
    allowed_role = 'teacher'

    def get(self, request):
        return render(request, "teachers/dashboard.html")


class TeacherTimeTableView(RoleAccessMixin, View):
    allowed_role = 'teacher'

    def get_lessons(self):
        lessons = []

        user = self.request.user
        lessons_qs = Lesson.objects.filter(group__teacher_groups__teacher=user, lesson_date__gte=date.today()).order_by(
            "-lesson_date")

        for lesson in lessons_qs:
            lesson_json = {
                "title": f"{lesson.group.name} "
                         f"[{lesson.start_time.strftime('%H:%M')}-{lesson.end_time.strftime('%H:%M')}]",
                "start": lesson.lesson_date.strftime('%Y-%m-%d')
            }
            if lesson.topic:
                lesson_json["title"] += f" | Mavzu: {lesson.topic}"

            lessons.append(lesson_json)

        return lessons

    def get(self, request):
        context = {}

        events = []
        events += self.get_lessons()

        context["events"] = events

        return render(request, "teachers/timetable.html", context)


class TeacherGroupDetailView(RoleAccessMixin, View):
    def get_custom_days(self, group) -> list:
        days = {
            CustomGroupDay.DayChoices.MONDAY: "Dushanba",
            CustomGroupDay.DayChoices.TUESDAY: "Seshanba",
            CustomGroupDay.DayChoices.WEDNESDAY: "Chorshanba",
            CustomGroupDay.DayChoices.THURSDAY: "Payshanba",
            CustomGroupDay.DayChoices.FRIDAY: "Juma",
            CustomGroupDay.DayChoices.SATURDAY: "Shanba",
            CustomGroupDay.DayChoices.SUNDAY: "Yakshanba",
        }

        custom_days_en = group.custom_group_days.all()
        if custom_days_en:
            return [days.get(i.day) for i in custom_days_en]

    def get(self, request, group_name):
        group = Group.objects.get(name=group_name)

        context = {
            "group_name": group_name,
            "group": group,
            "custom_days_uz": self.get_custom_days(group),
            "student_count": group.user_groups.all().count(),
            "group_lessons_count": group.lessons.all().count()
        }

        return render(request, "teachers/group_detail.html", context)


class AllTeacherStudentsView(RoleAccessMixin, View):
    allowed_role = "teacher"

    def get(self, request):
        students = (
            User.objects
            .filter(user_groups__group__teacher_groups__teacher=request.user)
            .order_by(
                NullIf(F("first_name"), Value("")).asc(nulls_last=True),
                "id"
            )
            .distinct()
            .prefetch_related(
                Prefetch(
                    "user_groups",
                    queryset=UserGroups.objects.filter(group__teacher_groups__teacher=request.user)
                )
            )
        )

        paginator = Paginator(students, 5)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context = {
            "students": students,
            "page_obj": page_obj,
        }

        return render(request, "teachers/all_students.html", context)


class TeacherGroupStudentsView(RoleAccessMixin, View):
    allowed_role = "teacher"

    def get(self, request, group_name):
        group = Group.objects.get(name=group_name)

        try:
            TeacherGroups.objects.get(teacher=request.user, group=group)
        except TeacherGroups.DoesNotExist:
            raise Http404

        group_students = (
            User.objects
            .filter(user_groups__group=group)
            .order_by(
                NullIf(F("first_name"), Value("")).asc(nulls_last=True),
                "id"
            )
            .prefetch_related(
                Prefetch(
                    lookup="user_groups",
                    queryset=UserGroups.objects.filter(group=group),
                    to_attr="student_group"
                )
            )
        )

        context = {"group_students": group_students, "group_name": group_name}

        return render(request, "teachers/group_students.html", context)
