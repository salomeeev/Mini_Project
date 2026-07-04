document.addEventListener('DOMContentLoaded', function () {
    // Sidebar Toggle
    const sidebar = document.getElementById('sidebar');
    const toggleBtn = document.getElementById('sidebarToggle');
    
    if (toggleBtn && sidebar) {
        toggleBtn.addEventListener('click', function () {
            sidebar.classList.toggle('collapsed');
        });
    }

    // Auto-dismiss Alerts
    const alerts = document.querySelectorAll('.toast-alert');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            // Fade out animation
            alert.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            alert.style.opacity = '0';
            alert.style.transform = 'translateX(50px)';
            setTimeout(function () {
                alert.remove();
            }, 500);
        }, 4000);
    });
});

// Loading Spinner Control
function showLoading() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.classList.add('active');
    }
}

function hideLoading() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.classList.remove('active');
    }
}

// Profile Image Preview function (called by input onchange)
function previewImage(input) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        
        reader.onload = function (e) {
            const preview = document.getElementById('profileImagePreview');
            if (preview) {
                preview.src = e.target.result;
            }
        };
        
        reader.readAsDataURL(input.files[0]);
    }
}
