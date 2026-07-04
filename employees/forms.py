import re
from django import forms
# pyrefly: ignore [missing-import]
from django.utils import timezone
# pyrefly: ignore [missing-import]
from .models import Employee
from departments.models import Department
from designations.models import Designation

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'full_name', 'email', 'phone', 'department', 'designation',
            'salary', 'gender', 'date_of_birth', 'date_of_joining',
            'address', 'city', 'state', 'country', 'zip_code',
            'profile_image', 'status'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'John Doe'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'john.doe@example.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '10-digit mobile number'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'designation': forms.Select(attrs={'class': 'form-select'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 50000.00', 'step': '0.01'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_of_joining': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'House No, Street, Area...'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ZIP Code'}),
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*', 'onchange': 'previewImage(this)'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            query = Employee.objects.filter(email__iexact=email)
            if self.instance.pk:
                query = query.exclude(pk=self.instance.pk)
            if query.exists():
                raise forms.ValidationError("An employee with this email already exists.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            # Strip spaces, dashes, etc. to count digits
            digits = re.sub(r'\D', '', phone)
            if len(digits) != 10:
                raise forms.ValidationError("Phone number must contain exactly 10 digits.")
            return digits
        return phone

    def clean_salary(self):
        salary = self.cleaned_data.get('salary')
        if salary is not None and salary <= 0:
            raise forms.ValidationError("Salary must be a positive number greater than 0.")
        return salary

    def clean(self):
        cleaned_data = super().clean()
        dob = cleaned_data.get('date_of_birth')
        doj = cleaned_data.get('date_of_joining')

        if dob and doj:
            if doj < dob:
                raise forms.ValidationError({
                    'date_of_joining': "Date of joining cannot be before date of birth."
                })
            
            # Simple check: must be at least 18 years old to join
            age_at_joining = (doj - dob).days / 365.25
            if age_at_joining < 18:
                raise forms.ValidationError({
                    'date_of_joining': "Employee must be at least 18 years old at the date of joining."
                })
        
        return cleaned_data
