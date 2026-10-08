document.addEventListener("DOMContentLoaded", function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    const admissionForm = document.getElementById('admissionForm');
    if(admissionForm && !admissionForm.hasAttribute('data-no-ajax')) {
        admissionForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if(data.status === 'success') {
                    this.innerHTML = `
                        <div class="text-center py-4">
                            <i class="bi bi-check-circle-fill text-success" style="font-size: 5rem;"></i>
                            <h2 class="mt-4 fw-bold text-dark">Application Submitted!</h2>
                            <p class="lead text-muted">${data.message}</p>
                            <div class="alert alert-success d-inline-block mt-3 px-4 py-3 shadow-sm">
                                <strong class="fs-5">Application ID: ${data.app_id}</strong>
                            </div>
                            <p class="text-muted mt-3">Please keep this ID for future reference. Our team will contact you soon.</p>
                            <a href="/" class="btn btn-primary btn-lg mt-3 px-5">Return to Home</a>
                        </div>
                    `;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                this.submit();
            });
        });
    }
});
