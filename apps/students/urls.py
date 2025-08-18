from django.urls import path
from .views import StudentHomeView, StudentScheduleView, StudentProgressView, StudentAttendanceView

from . import views, attendance_view


urlpatterns = [
    path('', StudentHomeView.as_view(), name='StudentHome'),
    path('schedule/', StudentScheduleView.as_view(), name='student_schedule'),
    path('progress/', StudentProgressView.as_view(), name='student_progress'),
    path('attendance/', StudentAttendanceView.as_view(), name='student_attendance'),
    path('timetable/', views.StudentTimeTableView.as_view(), name='timetable'),
    # Attendance related
    path("scan/<int:lesson_id>/", attendance_view.scan_attendance, name="scan_attendance"),
    path("api/mark/", attendance_view.api_mark_attendance, name="api_mark_attendance"),
]
