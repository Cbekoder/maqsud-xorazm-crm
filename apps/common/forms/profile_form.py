from django import forms

from models import User


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "phone"]

        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "id": "inputFirstName",
                    "placeholder": "Ism",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "id": "inputLastName",
                    "placeholder": "Familiya",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "id": "inputPhone",
                    "placeholder": "Telefon Raqam",
                }
            ),
        }




