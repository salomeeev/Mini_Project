document.addEventListener('DOMContentLoaded', function () {
    const employeeForm = document.querySelector('form');
    if (!employeeForm) return;

    // We only perform validation if fields exist
    const emailField = document.getElementById('id_email');
    const phoneField = document.getElementById('id_phone');
    const salaryField = document.getElementById('id_salary');
    const dobField = document.getElementById('id_date_of_birth');
    const dojField = document.getElementById('id_date_of_joining');

    function showError(field, message) {
        // Remove existing error if any
        removeError(field);
        field.classList.add('is-invalid');
        
        const errorDiv = document.createElement('div');
        errorDiv.className = 'invalid-feedback text-danger-custom';
        errorDiv.id = field.id + '-error';
        errorDiv.textContent = message;
        field.parentNode.appendChild(errorDiv);
    }

    function removeError(field) {
        field.classList.remove('is-invalid');
        const existingError = document.getElementById(field.id + '-error');
        if (existingError) {
            existingError.remove();
        }
    }

    // Real-time validations
    if (emailField) {
        emailField.addEventListener('input', function () {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (this.value && !emailRegex.test(this.value)) {
                showError(this, 'Please enter a valid email address.');
            } else {
                removeError(this);
            }
        });
    }

    if (phoneField) {
        phoneField.addEventListener('input', function () {
            // Strip non-digits
            const cleaned = this.value.replace(/\D/g, '');
            if (this.value && cleaned.length !== 10) {
                showError(this, 'Phone number must contain exactly 10 digits.');
            } else {
                removeError(this);
            }
        });
    }

    if (salaryField) {
        salaryField.addEventListener('input', function () {
            const salary = parseFloat(this.value);
            if (this.value && (isNaN(salary) || salary <= 0)) {
                showError(this, 'Salary must be a positive number greater than 0.');
            } else {
                removeError(this);
            }
        });
    }

    // Form submit blocker
    employeeForm.addEventListener('submit', function (e) {
        let hasErrors = false;

        // 1. Email check
        if (emailField) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailField.value) {
                showError(emailField, 'Email is required.');
                hasErrors = true;
            } else if (!emailRegex.test(emailField.value)) {
                showError(emailField, 'Please enter a valid email address.');
                hasErrors = true;
            }
        }

        // 2. Phone check
        if (phoneField) {
            const cleaned = phoneField.value.replace(/\D/g, '');
            if (!phoneField.value) {
                showError(phoneField, 'Phone number is required.');
                hasErrors = true;
            } else if (cleaned.length !== 10) {
                showError(phoneField, 'Phone number must contain exactly 10 digits.');
                hasErrors = true;
            }
        }

        // 3. Salary check
        if (salaryField) {
            const salary = parseFloat(salaryField.value);
            if (!salaryField.value) {
                showError(salaryField, 'Salary is required.');
                hasErrors = true;
            } else if (isNaN(salary) || salary <= 0) {
                showError(salaryField, 'Salary must be a positive number greater than 0.');
                hasErrors = true;
            }
        }

        // 4. Dates check
        if (dobField && dojField && dobField.value && dojField.value) {
            const dob = new Date(dobField.value);
            const doj = new Date(dojField.value);
            
            if (doj < dob) {
                showError(dojField, 'Date of joining cannot be before date of birth.');
                hasErrors = true;
            } else {
                const diffTime = Math.abs(doj - dob);
                const diffYears = diffTime / (1000 * 60 * 60 * 24 * 365.25);
                if (diffYears < 18) {
                    showError(dojField, 'Employee must be at least 18 years old at date of joining.');
                    hasErrors = true;
                }
            }
        }

        if (hasErrors) {
            e.preventDefault();
            // Scroll to the first invalid element
            const firstInvalid = document.querySelector('.is-invalid');
            if (firstInvalid) {
                firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        } else {
            showLoading(); // Show loading spinner on successful submission
        }
    });
});
