from django.views import View
from django.views.generic import DetailView
from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import Http404

from datetime import date, timedelta

from apps.common.utils import RoleAccessMixin
from models import Lesson

import os


class StudentHomeView(RoleAccessMixin, View):
    allowed_role = 'student'

    # Returns {"pres_rate": pres_rate, "abs_rate": abs_rate}
    def calc_attendance_rates(self) -> dict:
        total_num = self.request.user.attendances.count()

        if total_num:
            pres_num = self.request.user.attendances.filter(status="Present").count()
            abs_num = self.request.user.attendances.filter(status="Absent").count()

            pres_rate = round(pres_num / total_num * 100)
            abs_rate = round(abs_num / total_num * 100)
        else:
            pres_rate = 0
            abs_rate = 0

        return {"pres_rate": pres_rate, "abs_rate": abs_rate}

    def get(self, request):
        context = {}

        attendance_rates = self.calc_attendance_rates()
        context.update(attendance_rates)

        return render(request, "students/dashboard.html", context=context)


class StudentProgressView(RoleAccessMixin, View):
    allowed_role = 'student'

    def get(self, request):
        return render(request, "students/progress.html")


class StudentTimeTableView(RoleAccessMixin, View):
    allowed_role = 'student'

    def get(self, request):
        context = {
            "group_lessons": [],
            "user_groups": request.user.user_groups.all(),
        }
        events = []

        for user_group in context["user_groups"]:
            # Event Logic
            lessons_qs = user_group.group.lessons.filter(lesson_date__gte=date.today()).order_by("-lesson_date")

            for lesson in lessons_qs:
                lesson_json = {
                    "title": f"{lesson.group.lesson_name} "
                             f"[{lesson.start_time.strftime('%H:%M')}-{lesson.end_time.strftime('%H:%M')}]",
                    "start": lesson.lesson_date.strftime('%Y-%m-%d')
                }
                if lesson.topic:
                    lesson_json["title"] += f" | Mavzu: {lesson.topic}"

                events.append(lesson_json)

            context["group_lessons"].append(lessons_qs)

        context["events"] = events

        return render(request, "students/timetable.html", context=context)


class StudentLessonsListView(RoleAccessMixin, View):
    allowed_role = "student"

    def get(self, request, group_name):

        if not request.user.user_groups.filter(group__name=group_name).exists():
            raise Http404

        group_lessons = (Lesson.objects
                         .filter(
                            group__name=group_name,
                            lesson_date__lt=date.today())
                         .order_by("-lesson_date"))
        next_lesson = Lesson.objects.filter(group__name=group_name, lesson_date__gte=date.today()).order_by("lesson_date").first()

        paginator = Paginator(group_lessons, 5)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(request, "students/lessons.html", context={
            "page_obj": page_obj,
            "group_lessons": group_lessons,
            "next_lesson": next_lesson,
            "group_name": group_name,
        })


class StudentLessonDetailView(RoleAccessMixin, DetailView):
    allowed_role = "student"

    model = Lesson
    template_name = "students/lesson_detail.html"
    context_object_name = "lesson"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        user = self.request.user

        if not obj.group.user_groups.filter(user=user).exists():
            raise Http404

        return obj

    def convert_to_embed(self, url):
        if "youtube.com/watch" in url:
            from urllib.parse import urlparse, parse_qs
            parsed = urlparse(url)
            video_id = parse_qs(parsed.query).get("v", [None])[0]
            if video_id:
                return f"https://www.youtube.com/embed/{video_id}"
        return url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lesson = self.get_object()

        # URL to embed [LOGIC]
        if lesson.lesson_video_url:
            context["lesson_video_url_embed"] = self.convert_to_embed(lesson.lesson_video_url)
        else:
            context["lesson_video_url_embed"] = None

        context["class_materials"] = lesson.class_materials.all()
        for class_material in context["class_materials"]:
            class_material.file_name = os.path.basename(class_material.material.name)

        context["homework_materials"] = lesson.homework_materials.all()
        for homework_material in context["homework_materials"]:
            homework_material.file_name = os.path.basename(homework_material.material.name)

        return context
