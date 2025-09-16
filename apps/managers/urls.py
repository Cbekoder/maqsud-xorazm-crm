from django.urls import path
from .views import (ManagerHomeView, GroupListView, GroupLessonsListView,
                    EnterLessonAttendance, ExitLessonAttendance, check_enter_qr, check_exit_qr)

urlpatterns = [
    path('', ManagerHomeView.as_view(), name='ManagerHome'),
    path("groups/", GroupListView.as_view(), name="manager_all_groups"),
    path("group-lessons/<str:group_name>", GroupLessonsListView.as_view(), name="manager_group_lessons"),
    path("enter-attendance/<int:lesson_id>", EnterLessonAttendance.as_view(), name="manager_enter_attendance"),
    path("exit-attendance/<int:lesson_id>", ExitLessonAttendance.as_view(), name="manager_exit_attendance"),
    path("check-enter-qr/<int:lesson_id>", check_enter_qr, name="manager_check_enter_qr"),
    path("check-exit-qr/<int:lesson_id>", check_exit_qr, name="manager_exit_enter_qr"),
]
