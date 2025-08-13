from django.urls import path
from .views import TeacherHomeView

urlpatterns = [
    path('', TeacherHomeView.as_view(), name='TeacherHome'),

]
