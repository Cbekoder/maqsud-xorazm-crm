from django.urls import path
from .views import (TeacherHomeView, TeacherTimeTableView, TeacherGroupDetailView, AllTeacherStudentsView,
                    TeacherGroupStudentsView,
                    AllTeacherLessonsView, TeacherGroupLessonsView, TeacherLessonDetailView,
                    delete_class_material, delete_homework_material)

urlpatterns = [
    path('', TeacherHomeView.as_view(), name='TeacherHome'),
    path('timetable', TeacherTimeTableView.as_view(), name='teacher_timetable'),
    path('group-detail/<str:group_name>', TeacherGroupDetailView.as_view(), name='group_detail'),
    path('all-students', AllTeacherStudentsView.as_view(), name='all_students'),
    path('group-students/<str:group_name>', TeacherGroupStudentsView.as_view(), name='group_students'),
    path('all-lessons', AllTeacherLessonsView.as_view(), name='teacher_all_lessons'),
    path('group-lessons/<str:group_name>', TeacherGroupLessonsView.as_view(), name='teacher_group_lessons'),
    path('lesson-detail/<int:pk>', TeacherLessonDetailView.as_view(), name='teacher_lesson_detail'),

    path('class_materials/<int:material_id>}/delete', delete_class_material, name="teacher_delete_class_material"),
    path('homework_materials/<int:material_id>}/delete', delete_homework_material, name="teacher_delete_homework_material"),
]
