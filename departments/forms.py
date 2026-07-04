from django import forms
from .models import Department

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Department Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter Department Description'}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            # Check for unique name manually if editing
            # Django handles unique constraint, but good to have clean_field for clear error message
            query = Department.objects.filter(name__iexact=name)
            if self.instance.pk:
                query = query.exclude(pk=self.instance.pk)
            if query.exists():
                raise forms.ValidationError("A department with this name already exists.")
        return name
