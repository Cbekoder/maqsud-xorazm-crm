from django.urls import path

from . import views


urlpatterns = [
    path('profile/edit', views.EditAuthUserProfileView.as_view(), name='edit_auth_user_profile'),
]




