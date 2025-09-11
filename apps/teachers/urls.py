from django.urls import path
from .views import (TeacherHomeView, TeacherTimeTableView, TeacherGroupDetailView, AllTeacherStudentsView,
                    TeacherGroupStudentsView)

urlpatterns = [
    path('', TeacherHomeView.as_view(), name='TeacherHome'),
    path('timetable', TeacherTimeTableView.as_view(), name='teacher_timetable'),
    path('group-detail/<str:group_name>', TeacherGroupDetailView.as_view(), name='group_detail'),
    path('all-students', AllTeacherStudentsView.as_view(), name='all_students'),
    path('group-students/<str:group_name>', TeacherGroupStudentsView.as_view(), name='group_students'),

]
