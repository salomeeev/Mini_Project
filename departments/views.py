from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Department
from .forms import DepartmentForm

@login_required
def department_list(request):
    departments = Department.objects.all().order_by('name')
    return render(request, 'departments/department_list.html', {'departments': departments})

@login_required
def department_add(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Department Created Successfully.")
            return redirect('departments:list')
        else:
            messages.error(request, "Error creating department. Please check details.")
    else:
        form = DepartmentForm()
    return render(request, 'departments/department_form.html', {'form': form, 'action': 'Add'})

@login_required
def department_edit(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, "Department Updated Successfully.")
            return redirect('departments:list')
        else:
            messages.error(request, "Error updating department. Please check details.")
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'departments/department_form.html', {'form': form, 'action': 'Edit', 'department': department})

@login_required
def department_delete(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        # Let's count how many employees are affected
        emp_count = department.employees.filter(is_deleted=False).count()
        department.delete()
        messages.success(request, f"Department '{department.name}' Deleted Successfully. {emp_count} employees had their department unset.")
        return redirect('departments:list')
    return render(request, 'departments/department_confirm_delete.html', {'department': department})
