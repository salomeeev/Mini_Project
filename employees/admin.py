from django.contrib import admin
from django.utils.html import format_html
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('image_tag', 'employee_id', 'full_name', 'email', 'phone', 'department', 'designation', 'status', 'is_deleted')
    list_filter = ('department', 'designation', 'status', 'gender', 'is_deleted')
    search_fields = ('full_name', 'employee_id', 'email', 'phone')
    ordering = ('employee_id',)
    
    def image_tag(self, obj):
        if obj.profile_image:
            return format_html('<img src="{}" style="width: 45px; height: 45px; border-radius: 50%; object-fit: cover;" />', obj.profile_image.url)
        return format_html('<span style="color: #999;">No Image</span>')
    image_tag.short_description = 'Photo'
