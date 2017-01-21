from django import forms
from omp.models import Project, Category


class CategoryForm(forms.ModelForm):
    id = forms.CharField(max_length=128, help_text="Please enter the category id.")
    name = forms.CharField(max_length=128, help_text="Please enter the category name.")
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Category
        fields = ('id', 'name',)


class ProjectForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Enter the project title\n")
    description = forms.CharField(max_length=500, help_text="Enter the project description\n")
    softeng = forms.BooleanField(help_text="Software Engineering Project? ")
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)


    class Meta:
        # Provide an association between the ModelForm and a model
        model = Project
        # What fields do we want to include in our form?
        # This way we don't need every field in the model present.
        # Some fields may allow NULL values, so we may not want to include them.
        # Here, we are hiding the foreign key.
        # we can either exclude the category field from the form,
        exclude = ('category',)
        # or specify the fields to include (i.e. not include the category field)
        #fields = ('title', 'url', 'views')