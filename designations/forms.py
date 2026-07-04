# pyrefly: ignore [missing-import]
from django import forms
# pyrefly: ignore [missing-import]
from .models import Designation

class DesignationForm(forms.ModelForm):
    class Meta:
        model = Designation
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Designation Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter Designation Description'}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            query = Designation.objects.filter(name__iexact=name)
            if self.instance.pk:
                query = query.exclude(pk=self.instance.pk)
            if query.exists():
                raise forms.ValidationError("A designation with this name already exists.")
        return name
