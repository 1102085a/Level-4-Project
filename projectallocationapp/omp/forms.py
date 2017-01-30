from django import forms
from omp.models import User, Project, Category, Student, Supervisor, PrefListEntry


class CategoryForm(forms.ModelForm):
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Category
        fields = ['name']


class ProjectForm(forms.ModelForm):
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Project
        fields = ['name', 'description', 'softEng', 'category', 'supervisor']
        exclude = ('category',)


class StudentForm(forms.ModelForm):
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Student
        fields = ['user', 'softEng', 'project', 'category', 'favourites']


class SupervisorForm(forms.ModelForm):
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Supervisor
        fields = ['user', 'category', 'capacity']


class PreferenceForm(forms.ModelForm):
    class Meta:
        model = PrefListEntry
        fields = ['student', 'project', 'rank']
