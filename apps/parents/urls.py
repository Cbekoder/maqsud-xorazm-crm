from django.urls import path
from .views import ParentHomeView

urlpatterns = [
    path('', ParentHomeView.as_view(), name='ParentHome'),
]
