/* ===== GIVE GRIP - MODERN JAVASCRIPT FRAMEWORK ===== */

// Global variables
let isLoading = false;
let currentUser = null;

// DOM Content Loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

// Initialize Application
function initializeApp() {
    setupEventListeners();
    setupAnimations();
    setupScrollEffects();
    setupMobileNavigation();
    setupUserMenu();
    setupBackToTop();
    setupLoadingSpinner();
    
    // Check if user is authenticated
    checkAuthentication();
    
    // Initialize tooltips and other UI components
    initializeUIComponents();
}

// ===== EVENT LISTENERS =====
function setupEventListeners() {
    // Form submissions
    document.addEventListener('submit', handleFormSubmission);
    
    // Input focus effects
    document.addEventListener('focusin', handleInputFocus);
    document.addEventListener('focusout', handleInputBlur);
    
    // Button clicks
    document.addEventListener('click', handleButtonClicks);
    
    // Window events
    window.addEventListener('scroll', handleScroll);
    window.addEventListener('resize', handleResize);
    window.addEventListener('beforeunload', handleBeforeUnload);
}

// ===== FORM HANDLING =====
function handleFormSubmission(event) {
    const form = event.target;
    const formType = form.dataset.formType;
    
    if (formType === 'donation') {
        event.preventDefault();
        handleDonationForm(form);
    } else if (formType === 'contact') {
        event.preventDefault();
        handleContactForm(form);
    } else if (formType === 'campaign') {
        event.preventDefault();
        handleCampaignForm(form);
    }
}

function handleDonationForm(form) {
    const formData = new FormData(form);
    const amount = formData.get('amount');
    const campaignId = formData.get('campaign_id');
    
    if (!amount || amount <= 0) {
        showNotification('Please enter a valid donation amount', 'error');
        return;
    }
    
    showLoadingSpinner();
    
    // Simulate API call
    setTimeout(() => {
        hideLoadingSpinner();
        showNotification('Thank you for your donation!', 'success');
        form.reset();
        
        // Update campaign progress
        updateCampaignProgress(campaignId, amount);
    }, 2000);
}

function handleContactForm(form) {
    const formData = new FormData(form);
    const name = formData.get('name');
    const email = formData.get('email');
    const message = formData.get('message');
    
    if (!name || !email || !message) {
        showNotification('Please fill in all fields', 'error');
        return;
    }
    
    showLoadingSpinner();
    
    // Simulate API call
    setTimeout(() => {
        hideLoadingSpinner();
        showNotification('Message sent successfully!', 'success');
        form.reset();
    }, 1500);
}

function handleCampaignForm(form) {
    const formData = new FormData(form);
    const title = formData.get('title');
    const description = formData.get('description');
    const goal = formData.get('goal');
    
    if (!title || !description || !goal) {
        showNotification('Please fill in all required fields', 'error');
        return;
    }
    
    showLoadingSpinner();
    
    // Simulate API call
    setTimeout(() => {
        hideLoadingSpinner();
        showNotification('Campaign created successfully!', 'success');
        form.reset();
        
        // Redirect to campaigns page
        setTimeout(() => {
            window.location.href = '/campaigns/';
        }, 1000);
    }, 2000);
}

// ===== INPUT HANDLING =====
function handleInputFocus(event) {
    const input = event.target;
    const formGroup = input.closest('.form-group');
    
    if (formGroup) {
        formGroup.classList.add('focused');
    }
}

function handleInputBlur(event) {
    const input = event.target;
    const formGroup = input.closest('.form-group');
    
    if (formGroup) {
        formGroup.classList.remove('focused');
        
        // Validate input
        validateInput(input);
    }
}

function validateInput(input) {
    const value = input.value.trim();
    const type = input.type;
    const required = input.hasAttribute('required');
    
    // Remove existing error states
    removeInputError(input);
    
    // Check required fields
    if (required && !value) {
        showInputError(input, 'This field is required');
        return false;
    }
    
    // Validate email
    if (type === 'email' && value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            showInputError(input, 'Please enter a valid email address');
            return false;
        }
    }
    
    // Validate phone
    if (input.name === 'phone' && value) {
        const phoneRegex = /^[\+]?[1-9][\d]{0,15}$/;
        if (!phoneRegex.test(value.replace(/\s/g, ''))) {
            showInputError(input, 'Please enter a valid phone number');
            return false;
        }
    }
    
    // Validate amount
    if (input.name === 'amount' && value) {
        const amount = parseFloat(value);
        if (isNaN(amount) || amount <= 0) {
            showInputError(input, 'Please enter a valid amount');
            return false;
        }
    }
    
    return true;
}

function showInputError(input, message) {
    const formGroup = input.closest('.form-group');
    const errorElement = document.createElement('div');
    errorElement.className = 'form-error';
    errorElement.textContent = message;
    
    formGroup.appendChild(errorElement);
    input.classList.add('error');
}

function removeInputError(input) {
    const formGroup = input.closest('.form-group');
    const errorElement = formGroup.querySelector('.form-error');
    
    if (errorElement) {
        errorElement.remove();
    }
    
    input.classList.remove('error');
}

// ===== BUTTON HANDLING =====
function handleButtonClicks(event) {
    const button = event.target.closest('button');
    if (!button) return;
    
    const action = button.dataset.action;
    
    switch (action) {
        case 'donate':
            handleDonateClick(button);
            break;
        case 'share':
            handleShareClick(button);
            break;
        case 'follow':
            handleFollowClick(button);
            break;
        case 'like':
            handleLikeClick(button);
            break;
    }
}

function handleDonateClick(button) {
    const campaignId = button.dataset.campaignId;
    const modal = document.getElementById('donationModal');
    
    if (modal) {
        showModal(modal);
        setupDonationModal(campaignId);
    }
}

function handleShareClick(button) {
    const url = window.location.href;
    const title = document.title;
    
    if (navigator.share) {
        navigator.share({
            title: title,
            url: url
        });
    } else {
        // Fallback to copying to clipboard
        navigator.clipboard.writeText(url).then(() => {
            showNotification('Link copied to clipboard!', 'success');
        });
    }
}

function handleFollowClick(button) {
    const isFollowing = button.classList.contains('following');
    
    if (isFollowing) {
        button.classList.remove('following');
        button.textContent = 'Follow';
        showNotification('Unfollowed successfully', 'info');
    } else {
        button.classList.add('following');
        button.textContent = 'Following';
        showNotification('Followed successfully', 'success');
    }
}

function handleLikeClick(button) {
    const isLiked = button.classList.contains('liked');
    const likeCount = button.querySelector('.like-count');
    
    if (isLiked) {
        button.classList.remove('liked');
        likeCount.textContent = parseInt(likeCount.textContent) - 1;
    } else {
        button.classList.add('liked');
        likeCount.textContent = parseInt(likeCount.textContent) + 1;
    }
}

// ===== MODAL HANDLING =====
function showModal(modal) {
    modal.classList.add('show');
    document.body.style.overflow = 'hidden';
    
    // Focus first input
    const firstInput = modal.querySelector('input, textarea, select');
    if (firstInput) {
        firstInput.focus();
    }
}

function hideModal(modal) {
    modal.classList.remove('show');
    document.body.style.overflow = '';
}

function setupDonationModal(campaignId) {
    const modal = document.getElementById('donationModal');
    const amountInputs = modal.querySelectorAll('input[name="amount"]');
    const customAmountInput = modal.querySelector('input[name="custom_amount"]');
    
    // Handle preset amount selection
    amountInputs.forEach(input => {
        input.addEventListener('change', function() {
            if (this.checked) {
                customAmountInput.value = '';
            }
        });
    });
    
    // Handle custom amount input
    customAmountInput.addEventListener('input', function() {
        amountInputs.forEach(input => input.checked = false);
    });
    
    // Handle form submission
    const form = modal.querySelector('form');
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const selectedAmount = modal.querySelector('input[name="amount"]:checked');
        const customAmount = customAmountInput.value;
        const amount = selectedAmount ? selectedAmount.value : customAmount;
        
        if (!amount || amount <= 0) {
            showNotification('Please select or enter a valid amount', 'error');
            return;
        }
        
        // Process donation
        processDonation(campaignId, amount);
    });
}

function processDonation(campaignId, amount) {
    showLoadingSpinner();
    
    // Simulate payment processing
    setTimeout(() => {
        hideLoadingSpinner();
        showNotification('Donation processed successfully!', 'success');
        
        // Close modal
        const modal = document.getElementById('donationModal');
        hideModal(modal);
        
        // Update campaign progress
        updateCampaignProgress(campaignId, amount);
    }, 3000);
}

// ===== NOTIFICATIONS =====
function showNotification(message, type = 'info', duration = 5000) {
    const notification = createNotificationElement(message, type);
    document.body.appendChild(notification);
    
    // Show notification
    setTimeout(() => {
        notification.classList.add('show');
    }, 100);
    
    // Auto hide
    setTimeout(() => {
        hideNotification(notification);
    }, duration);
}

function createNotificationElement(message, type) {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    
    const icon = getNotificationIcon(type);
    
    notification.innerHTML = `
        <div class="notification-content">
            <i class="notification-icon">${icon}</i>
            <span class="notification-message">${message}</span>
        </div>
        <button class="notification-close" onclick="this.parentElement.remove()">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    return notification;
}

function getNotificationIcon(type) {
    switch (type) {
        case 'success': return '<i class="fas fa-check-circle"></i>';
        case 'error': return '<i class="fas fa-exclamation-circle"></i>';
        case 'warning': return '<i class="fas fa-exclamation-triangle"></i>';
        case 'info': return '<i class="fas fa-info-circle"></i>';
        default: return '<i class="fas fa-info-circle"></i>';
    }
}

function hideNotification(notification) {
    notification.classList.remove('show');
    setTimeout(() => {
        if (notification.parentElement) {
            notification.parentElement.removeChild(notification);
        }
    }, 300);
}

// ===== LOADING SPINNER =====
function setupLoadingSpinner() {
    const spinner = document.getElementById('loading-spinner');
    if (!spinner) return;
    
    // Hide spinner on page load
    setTimeout(() => {
        hideLoadingSpinner();
    }, 1000);
}

function showLoadingSpinner() {
    if (isLoading) return;
    
    isLoading = true;
    const spinner = document.getElementById('loading-spinner');
    if (spinner) {
        spinner.classList.add('show');
    }
}

function hideLoadingSpinner() {
    isLoading = false;
    const spinner = document.getElementById('loading-spinner');
    if (spinner) {
        spinner.classList.remove('show');
    }
}

// ===== MOBILE NAVIGATION =====
function setupMobileNavigation() {
    const navbarToggle = document.getElementById('navbar-toggle');
    const navbarMenu = document.getElementById('navbar-menu');
    
    if (!navbarToggle || !navbarMenu) return;
    
    navbarToggle.addEventListener('click', function() {
        navbarMenu.classList.toggle('show');
        
        // Animate hamburger
        const spans = this.querySelectorAll('span');
        spans.forEach(span => span.classList.toggle('active'));
    });
    
    // Close menu when clicking outside
    document.addEventListener('click', function(event) {
        if (!navbarToggle.contains(event.target) && !navbarMenu.contains(event.target)) {
            navbarMenu.classList.remove('show');
            const spans = navbarToggle.querySelectorAll('span');
            spans.forEach(span => span.classList.remove('active'));
        }
    });
}

// ===== USER MENU =====
function setupUserMenu() {
    const userMenuToggle = document.getElementById('user-menu-toggle');
    const userDropdown = document.getElementById('user-dropdown');
    
    if (!userMenuToggle || !userDropdown) return;
    
    userMenuToggle.addEventListener('click', function(event) {
        event.stopPropagation();
        userDropdown.classList.toggle('show');
    });
    
    // Close dropdown when clicking outside
    document.addEventListener('click', function(event) {
        if (!userMenuToggle.contains(event.target)) {
            userDropdown.classList.remove('show');
        }
    });
}

// ===== SCROLL EFFECTS =====
function setupScrollEffects() {
    const elements = document.querySelectorAll('[data-animate]');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const element = entry.target;
                const animation = element.dataset.animate;
                element.classList.add(animation);
                observer.unobserve(element);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    elements.forEach(element => {
        observer.observe(element);
    });
}

function handleScroll() {
    const scrollTop = window.pageYOffset;
    const backToTop = document.getElementById('back-to-top');
    
    if (backToTop) {
        if (scrollTop > 300) {
            backToTop.classList.add('show');
        } else {
            backToTop.classList.remove('show');
        }
    }
    
    // Parallax effects
    const parallaxElements = document.querySelectorAll('[data-parallax]');
    parallaxElements.forEach(element => {
        const speed = element.dataset.parallax || 0.5;
        const yPos = -(scrollTop * speed);
        element.style.transform = `translateY(${yPos}px)`;
    });
}

// ===== BACK TO TOP =====
function setupBackToTop() {
    const backToTop = document.getElementById('back-to-top');
    if (!backToTop) return;
    
    backToTop.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// ===== ANIMATIONS =====
function setupAnimations() {
    // Add animation classes to elements
    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in');
            }
        });
    });
    
    animatedElements.forEach(element => {
        observer.observe(element);
    });
}

// ===== UTILITY FUNCTIONS =====
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// ===== CAMPAIGN FUNCTIONS =====
function updateCampaignProgress(campaignId, amount) {
    const campaignCard = document.querySelector(`[data-campaign-id="${campaignId}"]`);
    if (!campaignCard) return;
    
    const progressBar = campaignCard.querySelector('.progress-fill');
    const currentAmount = campaignCard.querySelector('.current-amount');
    const goalAmount = campaignCard.querySelector('.goal-amount');
    
    if (progressBar && currentAmount && goalAmount) {
        const current = parseFloat(currentAmount.textContent.replace(/[^0-9.]/g, ''));
        const goal = parseFloat(goalAmount.textContent.replace(/[^0-9.]/g, ''));
        const newCurrent = current + parseFloat(amount);
        
        currentAmount.textContent = formatCurrency(newCurrent);
        
        const percentage = Math.min((newCurrent / goal) * 100, 100);
        progressBar.style.width = percentage + '%';
        
        // Add animation
        progressBar.classList.add('animate-progress');
        setTimeout(() => {
            progressBar.classList.remove('animate-progress');
        }, 1000);
    }
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

// ===== AUTHENTICATION =====
function checkAuthentication() {
    // Check if user is logged in (this would typically check cookies/session)
    const userMenu = document.querySelector('.user-menu');
    const authButtons = document.querySelector('.navbar-actions');
    
    if (userMenu && authButtons) {
        // For demo purposes, check if user menu exists
        if (userMenu.style.display !== 'none') {
            currentUser = {
                name: userMenu.querySelector('.user-name').textContent,
                email: 'user@example.com'
            };
        }
    }
}

// ===== UI COMPONENTS =====
function initializeUIComponents() {
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize dropdowns
    initializeDropdowns();
    
    // Initialize tabs
    initializeTabs();
    
    // Initialize accordions
    initializeAccordions();
}

function initializeTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    
    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', showTooltip);
        element.addEventListener('mouseleave', hideTooltip);
    });
}

function showTooltip(event) {
    const element = event.target;
    const tooltipText = element.dataset.tooltip;
    
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip';
    tooltip.textContent = tooltipText;
    
    document.body.appendChild(tooltip);
    
    const rect = element.getBoundingClientRect();
    tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
    tooltip.style.top = rect.top - tooltip.offsetHeight - 10 + 'px';
    
    element.tooltip = tooltip;
}

function hideTooltip(event) {
    const element = event.target;
    if (element.tooltip) {
        element.tooltip.remove();
        element.tooltip = null;
    }
}

function initializeDropdowns() {
    const dropdowns = document.querySelectorAll('.dropdown');
    
    dropdowns.forEach(dropdown => {
        const toggle = dropdown.querySelector('.dropdown-toggle');
        const menu = dropdown.querySelector('.dropdown-menu');
        
        if (toggle && menu) {
            toggle.addEventListener('click', function(e) {
                e.preventDefault();
                menu.classList.toggle('show');
            });
        }
    });
}

function initializeTabs() {
    const tabContainers = document.querySelectorAll('.tabs');
    
    tabContainers.forEach(container => {
        const tabs = container.querySelectorAll('.tab');
        const contents = container.querySelectorAll('.tab-content');
        
        tabs.forEach(tab => {
            tab.addEventListener('click', function() {
                const target = this.dataset.target;
                
                // Remove active class from all tabs and contents
                tabs.forEach(t => t.classList.remove('active'));
                contents.forEach(c => c.classList.remove('active'));
                
                // Add active class to current tab and content
                this.classList.add('active');
                const content = container.querySelector(`[data-content="${target}"]`);
                if (content) {
                    content.classList.add('active');
                }
            });
        });
    });
}

function initializeAccordions() {
    const accordions = document.querySelectorAll('.accordion');
    
    accordions.forEach(accordion => {
        const header = accordion.querySelector('.accordion-header');
        const content = accordion.querySelector('.accordion-content');
        
        if (header && content) {
            header.addEventListener('click', function() {
                const isOpen = accordion.classList.contains('open');
                
                // Close all accordions
                accordions.forEach(acc => {
                    acc.classList.remove('open');
                    const accContent = acc.querySelector('.accordion-content');
                    if (accContent) {
                        accContent.style.maxHeight = null;
                    }
                });
                
                // Open current accordion if it was closed
                if (!isOpen) {
                    accordion.classList.add('open');
                    content.style.maxHeight = content.scrollHeight + 'px';
                }
            });
        }
    });
}

// ===== EVENT HANDLERS =====
function handleResize() {
    // Handle responsive behavior
    const isMobile = window.innerWidth <= 768;
    
    if (isMobile) {
        document.body.classList.add('mobile');
    } else {
        document.body.classList.remove('mobile');
    }
}

function handleBeforeUnload(event) {
    // Save any unsaved form data
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        if (form.dataset.autoSave) {
            saveFormData(form);
        }
    });
}

function saveFormData(form) {
    const formData = new FormData(form);
    const data = {};
    
    for (let [key, value] of formData.entries()) {
        data[key] = value;
    }
    
    localStorage.setItem(`form_${form.dataset.formType}`, JSON.stringify(data));
}

function loadFormData(form) {
    const saved = localStorage.getItem(`form_${form.dataset.formType}`);
    if (saved) {
        const data = JSON.parse(saved);
        Object.keys(data).forEach(key => {
            const input = form.querySelector(`[name="${key}"]`);
            if (input) {
                input.value = data[key];
            }
        });
    }
}

// ===== EXPORT FUNCTIONS =====
window.GiveGrip = {
    showNotification,
    showLoadingSpinner,
    hideLoadingSpinner,
    showModal,
    hideModal,
    formatCurrency,
    updateCampaignProgress
};

// ===== PERFORMANCE OPTIMIZATION =====
// Throttle scroll events
const throttledScroll = throttle(handleScroll, 16);
window.addEventListener('scroll', throttledScroll);

// Debounce resize events
const debouncedResize = debounce(handleResize, 250);
window.addEventListener('resize', debouncedResize);

// ===== SERVICE WORKER REGISTRATION =====
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/sw.js')
            .then(function(registration) {
                console.log('SW registered: ', registration);
            })
            .catch(function(registrationError) {
                console.log('SW registration failed: ', registrationError);
            });
    });
}




