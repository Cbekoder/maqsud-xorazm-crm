from django.urls import path
from .views import ManagerHomeView

urlpatterns = [
    path('', ManagerHomeView.as_view(), name='ManagerHome'),
]
