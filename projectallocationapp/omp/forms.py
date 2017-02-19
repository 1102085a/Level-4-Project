from django import forms
from omp.models import User, Project, Category, Student, Supervisor, PrefListEntry, Administrator


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['name']
        exclude = ('slug',)


class ProjectForm(forms.ModelForm):
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Project
        fields = ['name', 'description', 'softEng', 'category', 'supervisor']
        exclude = ('slug',)



class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ['user', 'softEng', 'project', 'category', 'favourites']


class SupervisorForm(forms.ModelForm):

    class Meta:
        model = Supervisor
        fields = ['user', 'category', 'capacity']


class AdminForm(forms.ModelForm):

    class Meta:
        model = Administrator
        fields = ['user']


class PreferenceForm(forms.ModelForm):
    class Meta:
        model = PrefListEntry
        fields = ['student', 'project', 'rank']
