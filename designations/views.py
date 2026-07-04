from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Designation
from .forms import DesignationForm

@login_required
def designation_list(request):
    designations = Designation.objects.all().order_by('name')
    return render(request, 'designations/designation_list.html', {'designations': designations})

@login_required
def designation_add(request):
    if request.method == 'POST':
        form = DesignationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Designation Created Successfully.")
            return redirect('designations:list')
        else:
            messages.error(request, "Error creating designation. Please check details.")
    else:
        form = DesignationForm()
    return render(request, 'designations/designation_form.html', {'form': form, 'action': 'Add'})

@login_required
def designation_edit(request, pk):
    designation = get_object_or_404(Designation, pk=pk)
    if request.method == 'POST':
        form = DesignationForm(request.POST, instance=designation)
        if form.is_valid():
            form.save()
            messages.success(request, "Designation Updated Successfully.")
            return redirect('designations:list')
        else:
            messages.error(request, "Error updating designation. Please check details.")
    else:
        form = DesignationForm(instance=designation)
    return render(request, 'designations/designation_form.html', {'form': form, 'action': 'Edit', 'designation': designation})

@login_required
def designation_delete(request, pk):
    designation = get_object_or_404(Designation, pk=pk)
    if request.method == 'POST':
        emp_count = designation.employees.filter(is_deleted=False).count()
        designation.delete()
        messages.success(request, f"Designation '{designation.name}' Deleted Successfully. {emp_count} employees had their designation unset.")
        return redirect('designations:list')
    return render(request, 'designations/designation_confirm_delete.html', {'designation': designation})
