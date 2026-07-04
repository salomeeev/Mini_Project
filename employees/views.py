import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string

from .models import Employee
from .forms import EmployeeForm
from departments.models import Department
from designations.models import Designation

def home_redirect(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}! Login Successful.")
                return redirect('dashboard')
        messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')

@login_required
def dashboard_view(request):
    # KPIs
    total_employees = Employee.objects.filter(is_deleted=False).count()
    active_employees = Employee.objects.filter(is_deleted=False, status='Active').count()
    inactive_employees = Employee.objects.filter(is_deleted=False, status='Inactive').count()
    
    # Recently Added
    recently_added = Employee.objects.filter(is_deleted=False).order_by('-created_at')[:5]
    
    # Recent Activities: last 5 modified/created employees
    recent_activity = Employee.objects.filter(is_deleted=False).order_by('-updated_at')[:5]
    
    # Chart Data: Department-wise employee counts
    dept_chart_data = (
        Employee.objects.filter(is_deleted=False, department__isnull=False)
        .values('department__name')
        .annotate(count=Count('id'))
        .order_by('-count')
    )
    
    dept_labels = [item['department__name'] for item in dept_chart_data]
    dept_values = [item['count'] for item in dept_chart_data]
    
    # Chart Data: Status
    status_labels = ['Active', 'Inactive']
    status_values = [active_employees, inactive_employees]

    # Chart Data: Gender distribution
    gender_chart_data = (
        Employee.objects.filter(is_deleted=False)
        .values('gender')
        .annotate(count=Count('id'))
    )
    gender_labels = [item['gender'] for item in gender_chart_data]
    gender_values = [item['count'] for item in gender_chart_data]

    context = {
        'total_employees': total_employees,
        'active_employees': active_employees,
        'inactive_employees': inactive_employees,
        'recently_added': recently_added,
        'recent_activity': recent_activity,
        'dept_labels_json': json.dumps(dept_labels),
        'dept_values_json': json.dumps(dept_values),
        'status_labels_json': json.dumps(status_labels),
        'status_values_json': json.dumps(status_values),
        'gender_labels_json': json.dumps(gender_labels),
        'gender_values_json': json.dumps(gender_values),
    }
    return render(request, 'dashboard.html', context)

@login_required
def employee_list(request):
    queryset = Employee.objects.filter(is_deleted=False)
    
    # Search Query
    search_query = request.GET.get('search', '').strip()
    if search_query:
        queryset = queryset.filter(
            Q(full_name__icontains=search_query) |
            Q(employee_id__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(department__name__icontains=search_query) |
            Q(designation__name__icontains=search_query) |
            Q(city__icontains=search_query)
        )
        
    # Filters
    dept_filter = request.GET.get('department', '')
    desig_filter = request.GET.get('designation', '')
    status_filter = request.GET.get('status', '')
    gender_filter = request.GET.get('gender', '')
    
    if dept_filter:
        queryset = queryset.filter(department_id=dept_filter)
    if desig_filter:
        queryset = queryset.filter(designation_id=desig_filter)
    if status_filter:
        queryset = queryset.filter(status=status_filter)
    if gender_filter:
        queryset = queryset.filter(gender=gender_filter)
        
    # Sorting
    sort_by = request.GET.get('sort', 'employee_id') # Default sort by Employee ID
    # Map friendly sort params to fields
    sort_mapping = {
        'id': 'employee_id',
        '-id': '-employee_id',
        'name': 'full_name',
        '-name': '-full_name',
        'salary': 'salary',
        '-salary': '-salary',
        'doj': 'date_of_joining',
        '-doj': '-date_of_joining',
    }
    db_sort_field = sort_mapping.get(sort_by, 'employee_id')
    queryset = queryset.order_by(db_sort_field)
    
    # Pagination (10 per page)
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Dropdowns for Filters
    departments = Department.objects.all().order_by('name')
    designations = Designation.objects.all().order_by('name')
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'selected_dept': dept_filter,
        'selected_desig': desig_filter,
        'selected_status': status_filter,
        'selected_gender': gender_filter,
        'selected_sort': sort_by,
        'departments': departments,
        'designations': designations,
        'total_count': queryset.count(),
    }
    
    # Check if AJAX request for instant search/filter update
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.GET.get('ajax') == '1':
        html = render_to_string('employees/employee_table_partial.html', context, request=request)
        return JsonResponse({'html': html})
        
    return render(request, 'employees/employee_list.html', context)

@login_required
def employee_add(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            employee = form.save()
            messages.success(request, f"Employee '{employee.full_name}' Added Successfully.")
            return redirect('employees:list')
        else:
            messages.error(request, "Failed to add employee. Please correct the errors below.")
    else:
        form = EmployeeForm()
    return render(request, 'employees/employee_form.html', {'form': form, 'action': 'Add'})

@login_required
def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk, is_deleted=False)
    return render(request, 'employees/employee_detail.html', {'employee': employee})

@login_required
def employee_edit(request, pk):
    employee = get_object_or_404(Employee, pk=pk, is_deleted=False)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, f"Employee '{employee.full_name}' Updated Successfully.")
            return redirect('employees:detail', pk=employee.pk)
        else:
            messages.error(request, "Failed to update employee. Please correct the errors below.")
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employees/employee_form.html', {'form': form, 'action': 'Edit', 'employee': employee})

@login_required
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk, is_deleted=False)
    if request.method == 'POST':
        # Soft delete
        employee.is_deleted = True
        employee.status = 'Inactive'
        employee.save()
        messages.success(request, f"Employee '{employee.full_name}' Deleted Successfully.")
        return redirect('employees:list')
    return render(request, 'employees/employee_delete.html', {'employee': employee})

def custom_404_view(request, exception=None):
    return render(request, '404.html', status=404)
