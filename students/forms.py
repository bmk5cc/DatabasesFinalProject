from django.forms import ModelForm

from students.models import Job, Course


class JobForm(ModelForm):
    class Meta:
        model = Job
        fields = '__all__'
