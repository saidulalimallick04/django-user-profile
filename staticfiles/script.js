/**
 * Main Application JavaScript File
 * Handles common functionality across all pages
 */

// DOM Ready Function
document.addEventListener('DOMContentLoaded', function() {
    // Initialize components based on page
    const bodyId = document.body.id;
    const pageName = bodyId || document.querySelector('main')?.id || 'generic';
    
    // Common initializations
    initNavigation();
    initForms();
    initModals();
    
    // Page-specific initializations
    switch(pageName) {
        case 'login-page':
            initLoginPage();
            break;
        case 'signup-page':
            initSignupPage();
            break;
        case 'profile-page':
            initProfilePage();
            break;
        case 'forgot-password-page':
            initForgotPasswordPage();
            break;
        case 'otp-verification-page':
            initOtpPage();
            break;
        // Add more page cases as needed
    }
    
    // Global event listeners
    setupGlobalListeners();
});

// ===== GLOBAL FUNCTIONS =====

/**
 * Initialize navigation functionality
 */
function initNavigation() {
    // Mobile menu toggle
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const navMenu = document.querySelector('.nav-links');
    
    if (mobileMenuToggle && navMenu) {
        mobileMenuToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            this.classList.toggle('open');
            this.setAttribute('aria-expanded', this.classList.contains('open'));
        });
    }
    
    // Active link highlighting
    const currentPath = window.location.pathname.split('/').pop();
    document.querySelectorAll('.nav-links a').forEach(link => {
        const linkPath = link.getAttribute('href').split('/').pop();
        if (linkPath === currentPath) {
            link.classList.add('active');
        }
    });
}

/**
 * Initialize form validations and enhancements
 */
function initForms() {
    document.querySelectorAll('form').forEach(form => {
        // Add form validation
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
                showToast('Please correct the errors in the form', 'error');
            }
        });
        
        // Add input enhancements
        form.querySelectorAll('input').forEach(input => {
            // Add focus classes
            input.addEventListener('focus', function() {
                this.parentElement.classList.add('focused');
            });
            
            input.addEventListener('blur', function() {
                this.parentElement.classList.remove('focused');
                validateField(this);
            });
            
            // Real-time validation for certain fields
            if (input.type === 'email' || input.type === 'password' || input.hasAttribute('required')) {
                input.addEventListener('input', function() {
                    validateField(this);
                });
            }
        });
    });
}

/**
 * Initialize modal dialogs
 */
function initModals() {
    // Modal toggle functionality
    document.querySelectorAll('[data-modal-toggle]').forEach(toggle => {
        const modalId = toggle.getAttribute('data-modal-toggle');
        const modal = document.getElementById(modalId);
        
        if (modal) {
            toggle.addEventListener('click', () => {
                modal.classList.toggle('hidden');
                document.body.classList.toggle('modal-open');
                modal.setAttribute('aria-hidden', modal.classList.contains('hidden'));
                
                // Focus on first input when modal opens
                if (!modal.classList.contains('hidden')) {
                    const firstInput = modal.querySelector('input, button, [tabindex]');
                    if (firstInput) firstInput.focus();
                }
            });
        }
    });
    
    // Close modals when clicking outside or on close button
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('click', function(e) {
            if (e.target === this || e.target.classList.contains('modal-close')) {
                this.classList.add('hidden');
                document.body.classList.remove('modal-open');
                this.setAttribute('aria-hidden', 'true');
            }
        });
        
        // Close with Escape key
        modal.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && !this.classList.contains('hidden')) {
                this.classList.add('hidden');
                document.body.classList.remove('modal-open');
                this.setAttribute('aria-hidden', 'true');
            }
        });
    });
}

/**
 * Setup global event listeners
 */
function setupGlobalListeners() {
    // Toast notifications close button
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('toast-close')) {
            e.target.parentElement.remove();
        }
    });
    
    // Password visibility toggle
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('toggle-password')) {
            const input = e.target.previousElementSibling;
            if (input && input.type === 'password') {
                input.type = 'text';
                e.target.textContent = 'Hide';
                e.target.setAttribute('aria-label', 'Hide password');
            } else if (input) {
                input.type = 'password';
                e.target.textContent = 'Show';
                e.target.setAttribute('aria-label', 'Show password');
            }
        }
    });
}

/**
 * Login page specific functionality
 */
function initLoginPage() {
    // Remember me functionality
    const rememberMe = document.getElementById('remember-me');
    if (rememberMe && localStorage.getItem('rememberedEmail')) {
        const emailField = document.getElementById('login-identifier');
        if (emailField) {
            emailField.value = localStorage.getItem('rememberedEmail');
            rememberMe.checked = true;
        }
    }
    
    if (rememberMe) {
        rememberMe.addEventListener('change', function() {
            const emailField = document.getElementById('login-identifier');
            if (emailField) {
                if (this.checked && emailField.value) {
                    localStorage.setItem('rememberedEmail', emailField.value);
                } else {
                    localStorage.removeItem('rememberedEmail');
                }
            }
        });
    }
}

/**
 * Signup page specific functionality
 */
function initSignupPage() {
    // Password strength indicator
    const passwordField = document.getElementById('password');
    if (passwordField) {
        passwordField.addEventListener('input', function() {
            const strengthIndicator = document.getElementById('password-strength');
            if (strengthIndicator) {
                const strength = calculatePasswordStrength(this.value);
                strengthIndicator.textContent = strength.text;
                strengthIndicator.className = 'password-strength ' + strength.class;
            }
        });
    }
}

/**
 * Profile page specific functionality
 */
function initProfilePage() {
    // Avatar upload preview
    const avatarInput = document.getElementById('avatar-upload');
    if (avatarInput) {
        avatarInput.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                if (!file.type.match('image.*')) {
                    showToast('Please select an image file', 'error');
                    return;
                }
                
                const reader = new FileReader();
                reader.onload = function(e) {
                    const avatar = document.querySelector('.profile-avatar');
                    if (avatar) avatar.src = e.target.result;
                }
                reader.readAsDataURL(file);
            }
        });
    }
}

/**
 * Forgot password page functionality
 */
function initForgotPasswordPage() {
    // Additional validation can be added here if needed
}

/**
 * OTP verification page functionality
 */
function initOtpPage() {
    // OTP input auto-focus and navigation
    const otpInputs = document.querySelectorAll('.otp-input');
    if (otpInputs.length > 0) {
        otpInputs[0].focus();
        
        otpInputs.forEach((input, index) => {
            input.addEventListener('input', function() {
                if (this.value.length === 1 && index < otpInputs.length - 1) {
                    otpInputs[index + 1].focus();
                }
                
                // Auto-submit if all fields are filled
                if (index === otpInputs.length - 1 && this.value.length === 1) {
                    const allFilled = Array.from(otpInputs).every(i => i.value.length === 1);
                    if (allFilled) {
                        document.getElementById('otp-verification-form')?.requestSubmit();
                    }
                }
            });
            
            input.addEventListener('keydown', function(e) {
                if (e.key === 'Backspace' && !this.value && index > 0) {
                    otpInputs[index - 1].focus();
                }
            });
        });
    }
    
    // OTP resend countdown
    const resendButton = document.getElementById('resend-otp');
    const countdownElement = document.getElementById('countdown');
    if (resendButton && countdownElement) {
        let timeLeft = 300; // 5 minutes in seconds
        
        const updateCountdown = () => {
            const minutes = Math.floor(timeLeft / 60);
            const seconds = timeLeft % 60;
            countdownElement.textContent = `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
            
            if (timeLeft <= 0) {
                clearInterval(timer);
                resendButton.disabled = false;
                resendButton.classList.remove('disabled');
                countdownElement.textContent = 'Code expired';
            } else {
                timeLeft--;
            }
        };
        
        updateCountdown(); // Initial call
        const timer = setInterval(updateCountdown, 1000);
        
        resendButton.addEventListener('click', function() {
            // Implement resend logic here
            showToast('New OTP code sent to your email');
            timeLeft = 300;
            this.disabled = true;
            this.classList.add('disabled');
            updateCountdown();
        });
    }
}

// ===== UTILITY FUNCTIONS =====

/**
 * Calculate password strength
 */
function calculatePasswordStrength(password) {
    if (!password) return { text: '', class: '' };
    
    let strength = 0;
    
    // Length check
    if (password.length >= 4) strength++;
    if (password.length >= 8) strength++;
    
    // Character type checks
    if (/[A-Z]/.test(password)) strength++;
    if (/[0-9]/.test(password)) strength++;
    if (/[^A-Za-z0-9]/.test(password)) strength++;
    
    // Return result
    if (password.length < 4) return { text: 'Too short', class: 'weak' };
    if (strength <= 1) return { text: 'Weak', class: 'weak' };
    if (strength <= 2) return { text: 'Medium', class: 'medium' };
    return { text: 'Strong', class: 'strong' };
}

/**
 * Show toast notification
 */
function showToast(message, type = 'success') {
    // Remove existing toasts to prevent stacking
    document.querySelectorAll('.toast').forEach(toast => toast.remove());
    
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.setAttribute('role', 'status');
    toast.setAttribute('aria-live', 'polite');
    toast.innerHTML = `
        <span class="toast-message">${message}</span>
        <button class="toast-close" aria-label="Close notification">&times;</button>
    `;
    
    document.body.appendChild(toast);
    
    // Auto-remove after delay
    setTimeout(() => {
        toast.remove();
    }, 5000);
}