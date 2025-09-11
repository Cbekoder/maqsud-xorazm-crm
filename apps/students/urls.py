from django.urls import path
from .views import StudentHomeView, StudentProgressView

from . import views, attendance_view


urlpatterns = [
    path('', StudentHomeView.as_view(), name='StudentHome'),
    path('progress/', StudentProgressView.as_view(), name='student_progress'),
    path('timetable/', views.StudentTimeTableView.as_view(), name='timetable'),
    path('lessons/<str:group_name>/', views.StudentLessonsListView.as_view(), name='lessons'),
    path('lesson-detail/<int:pk>/', views.StudentLessonDetailView.as_view(), name='lesson_detail'),
    # Attendance related
    path("attendance/<str:group_name>/", attendance_view.StudentGroupAttendanceView.as_view(), name="group_attendance")
]
