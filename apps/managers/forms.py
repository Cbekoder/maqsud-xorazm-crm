from django import forms

from models import Course


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }






