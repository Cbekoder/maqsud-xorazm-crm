from django.urls import path
from .views import StudentHomeView, StudentScheduleView, StudentProgressView, StudentAttendanceView

from . import views


urlpatterns = [
    path('', StudentHomeView.as_view(), name='StudentHome'),
    path('schedule/', StudentScheduleView.as_view(), name='student_schedule'),
    path('progress/', StudentProgressView.as_view(), name='student_progress'),
    path('attendance/', StudentAttendanceView.as_view(), name='student_attendance'),
]
