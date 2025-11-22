// Authentication related JavaScript

document.addEventListener('DOMContentLoaded', function() {
    initializeAuthForms();
    setupPasswordValidation();
});

function initializeAuthForms() {
    // Add validation to auth forms
    const authForms = document.querySelectorAll('.auth-form');
    authForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateAuthForm(this)) {
                e.preventDefault();
            }
        });
    });
}

function validateAuthForm(form) {
    const email = form.querySelector('input[type="email"]');
    const password = form.querySelector('input[type="password"]');
    const name = form.querySelector('input[type="text"]');
    
    let isValid = true;
    
    // Validate email
    if (email && !isValidEmail(email.value)) {
        showFieldError(email, 'Please enter a valid email address');
        isValid = false;
    } else {
        clearFieldError(email);
    }
    
    // Validate password
    if (password && password.value.length < 6) {
        showFieldError(password, 'Password must be at least 6 characters long');
        isValid = false;
    } else {
        clearFieldError(password);
    }
    
    // Validate name for registration
    if (name && name.value.trim().length < 2) {
        showFieldError(name, 'Name must be at least 2 characters long');
        isValid = false;
    } else if (name) {
        clearFieldError(name);
    }
    
    return isValid;
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function showFieldError(field, message) {
    clearFieldError(field);
    
    field.style.borderColor = '#dc3545';
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'field-error';
    errorDiv.style.color = '#dc3545';
    errorDiv.style.fontSize = '12px';
    errorDiv.style.marginTop = '5px';
    errorDiv.textContent = message;
    
    field.parentNode.appendChild(errorDiv);
}

function clearFieldError(field) {
    field.style.borderColor = '';
    
    const existingError = field.parentNode.querySelector('.field-error');
    if (existingError) {
        existingError.remove();
    }
}

function setupPasswordValidation() {
    const passwordFields = document.querySelectorAll('input[type="password"]');
    passwordFields.forEach(field => {
        field.addEventListener('input', function() {
            if (this.value.length > 0 && this.value.length < 6) {
                this.style.borderColor = '#dc3545';
            } else {
                this.style.borderColor = '#28a745';
            }
        });
    });
}

// Forgot password functionality
function requestPasswordReset() {
    const email = document.getElementById('resetEmail').value;
    
    if (!isValidEmail(email)) {
        showNotification('Please enter a valid email address', 'error');
        return;
    }
    
    // Simulate API call
    showNotification('Password reset instructions sent to your email', 'success');
    
    // In a real application, you would make an API call here:
    /*
    fetch('/api/auth/forgot-password', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email: email })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification('Password reset instructions sent to your email', 'success');
        } else {
            showNotification('Error: ' + data.error, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Error sending reset email', 'error');
    });
    */
}