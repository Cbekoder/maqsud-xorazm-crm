from django.views import View
from django.shortcuts import render

from apps.common.utils import RoleAccessMixin

import pprint


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


class StudentTimeTableView(RoleAccessMixin, View):
    allowed_role = 'student'

    def convert_to_embed(self, url):
        if "youtube.com/watch" in url:
            from urllib.parse import urlparse, parse_qs
            parsed = urlparse(url)
            video_id = parse_qs(parsed.query).get("v", [None])[0]
            if video_id:
                return f"https://www.youtube.com/embed/{video_id}"
        return url

    def get(self, request):
        context = {
            "group_lessons": []
        }
        events = []
        user_groups = request.user.user_groups.all()

        for user_group in user_groups:
            for lesson in user_group.group.lessons.all():
                lesson_json = {
                    "title": f"{lesson.lesson_name} "
                             f"[{lesson.start_time.strftime('%H:%M')}-{lesson.end_time.strftime('%H:%M')}]",
                    "start": lesson.lesson_date.strftime('%Y-%m-%d')
                }
                if lesson.topic:
                    lesson_json["title"] += f" | Mavzu: {lesson.topic}"

                events.append(lesson_json)

            context["group_lessons"].append(user_group.group.lessons.all().order_by("-lesson_date"))

        context["events"] = events

        # Embed url logic
        video_url = request.GET.get("video")
        lesson_id = request.GET.get("lesson")
        if video_url:
            context["video_url"] = self.convert_to_embed(video_url)
        if lesson_id:
            context["lesson_id"] = lesson_id

        return render(request, "students/timetable.html", context=context)


