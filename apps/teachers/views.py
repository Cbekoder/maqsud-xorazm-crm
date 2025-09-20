from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import F, Value, Prefetch
from django.db.models.functions import NullIf
from django.http import Http404, JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST

from apps.common.utils import RoleAccessMixin
from models import (Lesson, Group, CustomGroupDay, User, UserGroups, TeacherGroups, ClassMaterial, HomeworkMaterial,
                    ActivityGrade, HomeworkGrade)

from datetime import date

import os


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

        return render(request, "teachers/group-detail.html", context)


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

        return render(request, "teachers/all-students.html", context)


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

        return render(request, "teachers/group-students.html", context)


class AllTeacherLessonsView(RoleAccessMixin, View):
    allowed_role = "teacher"

    def get(self, request):
        context = {}

        qs = Lesson.objects.filter(group__teacher_groups__teacher=request.user)

        paginator = Paginator(object_list=qs, per_page=10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context["page_obj"] = page_obj
        context["lessons"] = qs

        return render(request, "teachers/all-lessons.html", context)


MONTH_INTS_TO_NAMES = {
    1: "Yanvar",
    2: "Fevral",
    3: "Mart",
    4: "Aprel",
    5: "May",
    6: "Iyun",
    7: "Iyul",
    8: "Avgust",
    9: "Sentabr",
    10: "Oktabr",
    11: "Noyabr",
    12: "Dekabr",
}
class TeacherGroupLessonsView(RoleAccessMixin, View):
    allowed_role = "teacher"

    def get(self, request, group_name):
        context = {}

        try:
            TeacherGroups.objects.get(teacher=request.user, group__name=group_name)
        except TeacherGroups.DoesNotExist:
            return Http404

        group_lessons = Lesson.objects.filter(group__name=group_name).order_by("lesson_date")

        # Months FILTER logic
        existing_month_pairs = {}
        for group_lesson in group_lessons:
            month = group_lesson.lesson_date.month
            if month not in existing_month_pairs:
                existing_month_pairs[month] = MONTH_INTS_TO_NAMES.get(month)
        context["months"] = existing_month_pairs

        selected_month = request.GET.get("selected_month")
        if selected_month:
            selected_month = int(selected_month)
            context["selected_month"] = selected_month

            group_lessons = Lesson.objects.filter(group__name=group_name, lesson_date__month=selected_month).order_by("lesson_date")

        context["group_lessons"] = group_lessons

        return render(request, "teachers/group-lessons.html", context)


class TeacherLessonDetailView(RoleAccessMixin, View):
    template_name = "teachers/lesson-detail.html"
    allowed_role = "teacher"

    def convert_to_embed(self, url):
        if "youtube.com/watch" in url:
            from urllib.parse import urlparse, parse_qs
            parsed = urlparse(url)
            video_id = parse_qs(parsed.query).get("v", [None])[0]
            if video_id:
                return f"https://www.youtube.com/embed/{video_id}"
        return url

    def get(self, request, pk):
        lesson = get_object_or_404(Lesson, pk=pk)
        context = {
            "lesson": lesson,
            "class_materials": lesson.class_materials.all(),
            "homework_materials": lesson.homework_materials.all(),
            "lesson_video_url_embed": None
        }

        if lesson.lesson_video_url:
            context["lesson_video_url_embed"] = self.convert_to_embed(lesson.lesson_video_url)
            print(context["lesson_video_url_embed"])

        for class_material in context["class_materials"]:
            class_material.file_name = os.path.basename(class_material.material.name)

        for homework_material in context["homework_materials"]:
            homework_material.file_name = os.path.basename(homework_material.material.name)

        return render(request, self.template_name, context)

    def post(self, request, pk):
        lesson = get_object_or_404(Lesson, pk=pk)

        # FIELDS ACCORDING
        # ---------------------------------------------------------------
        # Topic
        topic = request.POST.get("topic")
        if topic:
            lesson.topic = topic
        # Video url
        video_url = request.POST.get("video_url")
        if video_url:
            lesson.lesson_video_url = video_url
        lesson.save()
        # CW files
        cw_files = request.FILES.getlist("cw_files")
        if cw_files:
            for i in cw_files:
                ClassMaterial.objects.create(lesson=lesson, material=i)
        # HW files
        hw_files = request.FILES.getlist("hw_files")
        if hw_files:
            for i in hw_files:
                HomeworkMaterial.objects.create(lesson=lesson, material=i)
        # ---------------------------------------------------------------

        return redirect("teacher_lesson_detail", pk=lesson.pk)


@require_POST
def delete_class_material(request, material_id):
    material = get_object_or_404(ClassMaterial, pk=material_id)

    material.material.delete(save=False)
    material.delete()

    return JsonResponse({"status": "success", "msg": "Fayl muvaffaqiyatli o‘chirildi"})


@require_POST
def delete_homework_material(request, material_id):
    material = get_object_or_404(HomeworkMaterial, pk=material_id)

    material.material.delete(save=False)
    material.delete()

    return JsonResponse({"status": "success", "msg": "Fayl muvaffaqiyatli o‘chirildi"})


class TeacherClassworkMarkingView(RoleAccessMixin, View):
    template_name = "teachers/cw-marking.html"
    allowed_role = "teacher"

    def get_context_data(self, request) -> dict:
        context = {}

        teacher_groups = TeacherGroups.objects.filter(teacher=request.user)
        context["teacher_groups"] = teacher_groups

        group_query = request.GET.get("group")
        if not group_query or group_query == "all":
            grade_qs = (ActivityGrade.objects
                        .filter(lesson__group__teacher_groups__teacher=request.user)
                        .order_by("lesson__group__name"))
        elif teacher_groups.filter(group__name=group_query).exists():
            grade_qs = (ActivityGrade.objects
                        .filter(lesson__group__teacher_groups__teacher=request.user, lesson__group__name=group_query)
                        .order_by("lesson__group__name"))
        else:
            grade_qs = (ActivityGrade.objects
                        .filter(lesson__group__teacher_groups__teacher=request.user)
                        .order_by("lesson__group__name"))

        context["grade_qs"] = grade_qs

        teacher_students = User.objects.filter(user_groups__group__teacher_groups__teacher=request.user).distinct()
        context["teacher_students"] = teacher_students

        scores = ActivityGrade.ScoreChoices.choices
        context["scores"] = scores

        return context

    def get(self, request):
        context = self.get_context_data(request)

        return render(request, self.template_name, context)

    def is_valid(self, group_id, lesson_id, student_id, score) -> (bool, str):
        if not group_id or not lesson_id or not student_id or not score:
            return False, "Majburiy maydonlarni to'ldiring!"

        return True, ""

    def invalid_context(self, request, err_msg, group_id, lesson_id, student_id, score) -> dict:
        context = self.get_context_data(request)
        context["err_msg"] = err_msg

        if group_id:
            context["group_id"] = int(group_id)
        else:
            context["group_id"] = group_id
        if lesson_id:
            context["lesson_id"] = int(lesson_id)
        else:
            context["lesson_id"] = lesson_id
        if student_id:
            context["student_id"] = int(student_id)
        else:
            context["student_id"] = student_id
        if score:
            context["score"] = int(score)
        else:
            context["score"] = score

        if group_id:
            context["lessons"] = Lesson.objects.filter(group__id=group_id)
            context["students"] = User.objects.filter(user_groups__group__id=group_id)

        return context

    def create_object_and_respond(self, request, group_id, lesson_id, student_id, score):
        group_id = int(group_id)
        lesson_id = int(lesson_id)
        student_id = int(student_id)
        score = int(score)

        try:
            grade, created = ActivityGrade.objects.get_or_create(
                lesson=Lesson.objects.get(id=lesson_id),
                student=User.objects.get(id=student_id),
                score=score
            )
            if not created:
                context = self.invalid_context(request, "Baho mavjud tekshirib qayta urining!", group_id, lesson_id, student_id, score)
                return render(request, self.template_name, context)

        except Exception as e:
            context = self.invalid_context(request, "Hatolik yuz berdi :(", group_id, lesson_id, student_id, score)
            return render(request, self.template_name, context)

        return redirect("teacher_classwork_marking")

    def update_object_and_respond(self, request, grade_id,  group_id, lesson_id, student_id, score):
        group_id = int(group_id)
        lesson_id = int(lesson_id)
        student_id = int(student_id)
        score = int(score)

        grade = ActivityGrade.objects.get(id=grade_id)
        grade.lesson = Lesson.objects.get(id=lesson_id)
        grade.student = User.objects.get(id=student_id)
        grade.score = score
        grade.save()

        return redirect("teacher_classwork_marking")

    def post(self, request):
        group_id = request.POST.get("group_id")
        lesson_id = request.POST.get("lesson_id")
        student_id = request.POST.get("student_id")
        score = request.POST.get("score")
        # For updating
        is_editing = request.POST.get("is_editing")
        grade_id = request.POST.get("grade_id")

        is_valid, err_msg = self.is_valid(group_id, lesson_id, student_id, score)

        if is_valid:
            if is_editing and grade_id:
                return self.update_object_and_respond(request, grade_id,  group_id, lesson_id, student_id, score)
            else:
                return self.create_object_and_respond(request, group_id, lesson_id, student_id, score)

        # Invalid
        context = self.invalid_context(request, err_msg, group_id, lesson_id, student_id, score)
        return render(request, self.template_name, context)


class TeacherHomeworkMarkingView(RoleAccessMixin, View):
    template_name = "teachers/hw-marking.html"
    allowed_role = "teacher"

    def get_context_data(self, request) -> dict:
        context = {}

        teacher_groups = TeacherGroups.objects.filter(teacher=request.user)
        context["teacher_groups"] = teacher_groups

        group_query = request.GET.get("group")
        if not group_query or group_query == "all":
            grade_qs = (HomeworkGrade.objects
                        .filter(lesson__group__teacher_groups__teacher=request.user)
                        .order_by("lesson__group__name"))
        elif teacher_groups.filter(group__name=group_query).exists():
            grade_qs = (HomeworkGrade.objects
                        .filter(lesson__group__teacher_groups__teacher=request.user, lesson__group__name=group_query)
                        .order_by("lesson__group__name"))
        else:
            grade_qs = (HomeworkGrade.objects
                        .filter(lesson__group__teacher_groups__teacher=request.user)
                        .order_by("lesson__group__name"))

        context["grade_qs"] = grade_qs

        teacher_students = User.objects.filter(user_groups__group__teacher_groups__teacher=request.user).distinct()
        context["teacher_students"] = teacher_students

        scores = HomeworkGrade.ScoreChoices.choices
        context["scores"] = scores

        return context

    def get(self, request):
        context = self.get_context_data(request)
        return render(request, self.template_name, context)

    def is_valid(self, group_id, lesson_id, student_id, score) -> (bool, str):
        if not group_id or not lesson_id or not student_id or not score:
            return False, "Majburiy maydonlarni to'ldiring!"

        return True, ""

    def invalid_context(self, request, err_msg, group_id, lesson_id, student_id, score) -> dict:
        context = self.get_context_data(request)
        context["err_msg"] = err_msg

        if group_id:
            context["group_id"] = int(group_id)
        else:
            context["group_id"] = group_id
        if lesson_id:
            context["lesson_id"] = int(lesson_id)
        else:
            context["lesson_id"] = lesson_id
        if student_id:
            context["student_id"] = int(student_id)
        else:
            context["student_id"] = student_id
        if score:
            context["score"] = int(score)
        else:
            context["score"] = score

        if group_id:
            context["lessons"] = Lesson.objects.filter(group__id=group_id)
            context["students"] = User.objects.filter(user_groups__group__id=group_id)

        return context

    def create_object_and_respond(self, request, group_id, lesson_id, student_id, score):
        group_id = int(group_id)
        lesson_id = int(lesson_id)
        student_id = int(student_id)
        score = int(score)

        try:
            grade, created = HomeworkGrade.objects.get_or_create(
                lesson=Lesson.objects.get(id=lesson_id),
                student=User.objects.get(id=student_id),
                score=score
            )
            if not created:
                context = self.invalid_context(request, "Baho mavjud tekshirib qayta urining!", group_id, lesson_id,
                                               student_id, score)
                return render(request, self.template_name, context)

        except Exception as e:
            context = self.invalid_context(request, "Hatolik yuz berdi :(", group_id, lesson_id, student_id, score)
            return render(request, self.template_name, context)

        return redirect("teacher_homework_marking")

    def update_object_and_respond(self, request, grade_id,  group_id, lesson_id, student_id, score):
        group_id = int(group_id)
        lesson_id = int(lesson_id)
        student_id = int(student_id)
        score = int(score)

        grade = HomeworkGrade.objects.get(id=grade_id)
        grade.lesson = Lesson.objects.get(id=lesson_id)
        grade.student = User.objects.get(id=student_id)
        grade.score = score
        grade.save()

        return redirect("teacher_classwork_marking")

    def post(self, request):
        group_id = request.POST.get("group_id")
        lesson_id = request.POST.get("lesson_id")
        student_id = request.POST.get("student_id")
        score = request.POST.get("score")
        # For updating
        is_editing = request.POST.get("is_editing")
        grade_id = request.POST.get("grade_id")

        is_valid, err_msg = self.is_valid(group_id, lesson_id, student_id, score)

        if is_valid:
            if is_editing and grade_id:
                return self.update_object_and_respond(request, grade_id, group_id, lesson_id, student_id, score)
            else:
                return self.create_object_and_respond(request, group_id, lesson_id, student_id, score)

        # Invalid
        context = self.invalid_context(request, err_msg, group_id, lesson_id, student_id, score)
        return render(request, self.template_name, context)


def get_group_students(request, group_id):
    students = User.objects.filter(user_groups__group__id=group_id).values("id", "username", "first_name")
    return JsonResponse(list(students), safe=False)


def get_group_lessons(request, group_id):
    lessons = Lesson.objects.filter(group__id=group_id).values("id", "lesson_date", "start_time", "end_time")
    return JsonResponse(list(lessons), safe=False)


class DeleteActivityGradeView(RoleAccessMixin, View):
    allowed_role = "teacher"

    def post(self, request, grade_id):
        grade = get_object_or_404(ActivityGrade, id=grade_id)
        grade.delete()

        return JsonResponse({"success": True})


class DeleteHomeworkGradeView(RoleAccessMixin, View):
    allowed_role = "teacher"

    def post(self, request, grade_id):
        grade = get_object_or_404(HomeworkGrade, id=grade_id)
        grade.delete()

        return JsonResponse({"success": True})



