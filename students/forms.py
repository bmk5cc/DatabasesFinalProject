from django.forms import ModelForm

from students.models import Course


class AddClassForm(ModelForm):
    class Meta:
        model = Course
        fields = ['name']