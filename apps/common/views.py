from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy

from apps.common.utils import RoleAccessMixin
from apps.common.forms.profile_form import ProfileForm
from models import User


# Create your views here.
class EditAuthUserProfileView(RoleAccessMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = "common/profile.html"
    success_url = reverse_lazy("edit_auth_user_profile")
    context_object_name = "user"

    def get_object(self, queryset=None):
        return self.request.user
