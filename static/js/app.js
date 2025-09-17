// Debt Payoff Planner JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        if (!alert.classList.contains('alert-danger')) {
            setTimeout(function() {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }, 5000);
        }
    });

    // Form validation helpers
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Number input formatting
    const currencyInputs = document.querySelectorAll('input[type="number"][step="0.01"]');
    currencyInputs.forEach(function(input) {
        input.addEventListener('blur', function() {
            if (this.value && !isNaN(this.value)) {
                this.value = parseFloat(this.value).toFixed(2);
            }
        });
    });

    // APR input validation
    const aprInputs = document.querySelectorAll('input[name="apr"]');
    aprInputs.forEach(function(input) {
        input.addEventListener('input', function() {
            const value = parseFloat(this.value);
            if (value > 50) {
                this.setCustomValidity('APR seems too high. Please double-check this value.');
            } else if (value < 0) {
                this.setCustomValidity('APR cannot be negative.');
            } else {
                this.setCustomValidity('');
            }
        });
    });

    // Balance input validation
    const balanceInputs = document.querySelectorAll('input[name="balance"]');
    balanceInputs.forEach(function(input) {
        input.addEventListener('input', function() {
            const value = parseFloat(this.value);
            if (value < 0) {
                this.setCustomValidity('Balance cannot be negative.');
            } else if (value > 100000) {
                this.setCustomValidity('Balance seems very high. Please double-check this value.');
            } else {
                this.setCustomValidity('');
            }
        });
    });

    // Minimum payment validation
    const minPaymentInputs = document.querySelectorAll('input[name="minimum_payment"]');
    minPaymentInputs.forEach(function(input) {
        input.addEventListener('input', function() {
            const value = parseFloat(this.value);
            const balanceInput = document.querySelector('input[name="balance"]');
            const balance = balanceInput ? parseFloat(balanceInput.value) : 0;
            
            if (value < 0) {
                this.setCustomValidity('Minimum payment cannot be negative.');
            } else if (balance > 0 && value > balance * 0.5) {
                this.setCustomValidity('Minimum payment seems very high compared to balance. Please double-check.');
            } else {
                this.setCustomValidity('');
            }
        });
    });

    // Smooth scrolling for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                e.preventDefault();
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Delete confirmation with better UX
    const deleteLinks = document.querySelectorAll('a[href*="/delete_card/"]');
    deleteLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const cardName = this.closest('tr').querySelector('td strong').textContent;
            
            if (confirm(`Are you sure you want to delete "${cardName}"? This action cannot be undone.`)) {
                // Add loading state
                this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Deleting...';
                this.classList.add('disabled');
                
                // Navigate to delete URL
                window.location.href = this.href;
            }
        });
    });

    // Loading states for form submissions
    const submitButtons = document.querySelectorAll('button[type="submit"]');
    submitButtons.forEach(function(button) {
        button.closest('form').addEventListener('submit', function() {
            button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
            button.disabled = true;
        });
    });

    // Auto-save draft functionality (optional enhancement)
    const cardFormInputs = document.querySelectorAll('#add_card form input, #edit_card form input');
    if (cardFormInputs.length > 0) {
        const draftKey = 'debt_card_draft';
        
        // Load draft on page load
        const draft = localStorage.getItem(draftKey);
        if (draft && window.location.pathname.includes('/add_card')) {
            const draftData = JSON.parse(draft);
            Object.keys(draftData).forEach(function(key) {
                const input = document.querySelector(`input[name="${key}"]`);
                if (input && !input.value) {
                    input.value = draftData[key];
                }
            });
        }
        
        // Save draft on input
        cardFormInputs.forEach(function(input) {
            input.addEventListener('input', function() {
                if (window.location.pathname.includes('/add_card')) {
                    const formData = {};
                    cardFormInputs.forEach(function(inp) {
                        if (inp.value) {
                            formData[inp.name] = inp.value;
                        }
                    });
                    localStorage.setItem(draftKey, JSON.stringify(formData));
                }
            });
        });
        
        // Clear draft on successful submit
        const cardForm = document.querySelector('#add_card form, #edit_card form');
        if (cardForm) {
            cardForm.addEventListener('submit', function() {
                localStorage.removeItem(draftKey);
            });
        }
    }
});

// Utility functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 2
    }).format(amount);
}

function formatPercentage(rate) {
    return new Intl.NumberFormat('en-US', {
        style: 'percent',
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    }).format(rate / 100);
}

// Export for use in other scripts
window.DebtPlannerUtils = {
    formatCurrency: formatCurrency,
    formatPercentage: formatPercentage
};