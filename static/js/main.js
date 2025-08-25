// ===== GLOBAL VARIABLES =====
let isLoading = false;
let scrollPosition = 0;

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

// ===== NAVIGATION =====
function initNavbar() {
    const navbar = document.getElementById('mainNav');
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    // Navbar scroll effect
    function handleNavbarScroll() {
        if (window.scrollY > 100) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    }
    
    // Mobile menu close on link click
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (navbarCollapse.classList.contains('show')) {
                navbarToggler.click();
            }
        });
    });
    
    // Active link highlighting
    function highlightActiveLink() {
        const currentPath = window.location.pathname;
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === currentPath) {
                link.classList.add('active');
            }
        });
    }
    
    window.addEventListener('scroll', throttle(handleNavbarScroll, 100));
    highlightActiveLink();
}

// ===== BACK TO TOP BUTTON =====
function initBackToTop() {
    const backToTopBtn = document.getElementById('backToTop');
    
    function toggleBackToTop() {
        if (window.scrollY > 300) {
            backToTopBtn.classList.add('show');
        } else {
            backToTopBtn.classList.remove('show');
        }
    }
    
    backToTopBtn.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    window.addEventListener('scroll', throttle(toggleBackToTop, 100));
}

// ===== LOADING SPINNER =====
function initLoadingSpinner() {
    const spinner = document.getElementById('loading-spinner');
    
    function showSpinner() {
        if (spinner) {
            spinner.style.display = 'flex';
            document.body.style.overflow = 'hidden';
        }
    }
    
    function hideSpinner() {
        if (spinner) {
            spinner.style.display = 'none';
            document.body.style.overflow = '';
        }
    }
    
    // Hide spinner when page is fully loaded
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', hideSpinner);
    } else {
        hideSpinner();
    }
    
    // Show spinner on form submissions
    document.addEventListener('submit', (e) => {
        if (e.target.tagName === 'FORM') {
            showSpinner();
        }
    });
    
    // Show spinner on link clicks (for navigation)
    document.addEventListener('click', (e) => {
        if (e.target.tagName === 'A' && e.target.href && !e.target.href.includes('#')) {
            showSpinner();
        }
    });
}

// ===== PASSWORD TOGGLES =====
function initPasswordToggles() {
    const passwordToggles = document.querySelectorAll('.password-toggle');
    
    passwordToggles.forEach(toggle => {
        toggle.addEventListener('click', () => {
            const input = toggle.previousElementSibling;
            const icon = toggle.querySelector('i');
            
            if (input.type === 'password') {
                input.type = 'text';
                icon.classList.remove('fa-eye');
                icon.classList.add('fa-eye-slash');
            } else {
                input.type = 'password';
                icon.classList.remove('fa-eye-slash');
                icon.classList.add('fa-eye');
            }
        });
    });
}

// ===== SMOOTH SCROLLING =====
function initSmoothScrolling() {
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href');
            
            // Skip if targetId is just '#' or empty
            if (!targetId || targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                const offsetTop = targetElement.offsetTop - 80; // Account for fixed navbar
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// ===== FORM VALIDATION =====
function validateForm() {
    const forms = document.querySelectorAll('.needs-validation');
    
    forms.forEach(form => {
        form.addEventListener('submit', (e) => {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
}

// ===== ANIMATIONS =====
function initAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in-up');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe elements with animation classes
    const animatedElements = document.querySelectorAll('.animate-fade-in-up, .animate-slide-in-left, .animate-slide-in-right');
    animatedElements.forEach(el => observer.observe(el));
}

// ===== CAMPAIGN CARDS =====
function initCampaignCards() {
    const campaignCards = document.querySelectorAll('.campaign-card');
    
    campaignCards.forEach(card => {
        // Hover effect
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-8px)';
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0)';
        });
        
        // Progress bar animation
        const progressBar = card.querySelector('.progress-bar');
        if (progressBar) {
            const width = progressBar.style.width;
            progressBar.style.width = '0%';
            setTimeout(() => {
                progressBar.style.width = width;
            }, 300);
        }
    });
}

// ===== DONATION FORM =====
function initDonationForm() {
    const donationForm = document.getElementById('donationForm');
    const amountInput = document.getElementById('amount');
    const quickAmountButtons = document.querySelectorAll('.quick-amount');
    
    if (donationForm && amountInput) {
        // Quick amount buttons
        quickAmountButtons.forEach(button => {
            button.addEventListener('click', () => {
                const amount = button.dataset.amount;
                amountInput.value = amount;
                
                // Update active state
                quickAmountButtons.forEach(btn => {
                    btn.classList.remove('active', 'btn-primary');
                    btn.classList.add('btn-outline-primary');
                });
                button.classList.remove('btn-outline-primary');
                button.classList.add('active', 'btn-primary');
            });
        });
        
        // Real-time validation
        amountInput.addEventListener('input', (e) => {
            const value = parseFloat(e.target.value);
            const submitBtn = donationForm.querySelector('button[type="submit"]');
            
            if (value && value > 0) {
                submitBtn.disabled = false;
                amountInput.classList.remove('is-invalid');
                amountInput.classList.add('is-valid');
            } else {
                submitBtn.disabled = true;
                amountInput.classList.remove('is-valid');
                amountInput.classList.add('is-invalid');
            }
        });
    }
}

// ===== SHARE FUNCTIONALITY =====
function initShareButtons() {
    const shareButtons = document.querySelectorAll('[data-share]');
    
    shareButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            const platform = button.dataset.share;
            const url = encodeURIComponent(window.location.href);
            const title = encodeURIComponent(document.title);
            
            let shareUrl = '';
            
            switch (platform) {
                case 'facebook':
                    shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${url}`;
                    break;
                case 'twitter':
                    shareUrl = `https://twitter.com/intent/tweet?text=${title}&url=${url}`;
                    break;
                case 'linkedin':
                    shareUrl = `https://www.linkedin.com/sharing/share-offsite/?url=${url}`;
                    break;
                case 'whatsapp':
                    shareUrl = `https://wa.me/?text=${title}%20${url}`;
                    break;
                case 'copy':
                    navigator.clipboard.writeText(window.location.href).then(() => {
                        showToast('Link copied to clipboard!', 'success');
                    });
                    return;
            }
            
            if (shareUrl) {
                window.open(shareUrl, '_blank', 'width=600,height=400');
            }
        });
    });
}

// ===== TOAST NOTIFICATIONS =====
function showToast(message, type = 'info') {
    const toastContainer = document.getElementById('toast-container') || createToastContainer();
    
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    `;
    
    toastContainer.appendChild(toast);
    
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    // Remove toast element after it's hidden
    toast.addEventListener('hidden.bs.toast', () => {
        toast.remove();
    });
}

function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container position-fixed top-0 end-0 p-3';
    container.style.zIndex = '9999';
    document.body.appendChild(container);
    return container;
}

// ===== SEARCH FUNCTIONALITY =====
function initSearch() {
    const searchInput = document.getElementById('searchInput');
    const searchResults = document.getElementById('searchResults');
    
    if (searchInput) {
        const debouncedSearch = debounce(async (query) => {
            if (query.length < 2) {
                searchResults.style.display = 'none';
                return;
            }
            
            try {
                const response = await fetch(`/api/search/?q=${encodeURIComponent(query)}`);
                const data = await response.json();
                
                if (data.results && data.results.length > 0) {
                    displaySearchResults(data.results);
                } else {
                    searchResults.innerHTML = '<div class="p-3 text-muted">No results found</div>';
                }
                searchResults.style.display = 'block';
            } catch (error) {
                console.error('Search error:', error);
            }
        }, 300);
        
        searchInput.addEventListener('input', (e) => {
            debouncedSearch(e.target.value);
        });
        
        // Hide results when clicking outside
        document.addEventListener('click', (e) => {
            if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
                searchResults.style.display = 'none';
            }
        });
    }
}

function displaySearchResults(results) {
    const searchResults = document.getElementById('searchResults');
    
    searchResults.innerHTML = results.map(result => `
        <a href="${result.url}" class="dropdown-item">
            <div class="d-flex align-items-center">
                <img src="${result.image || '/static/images/default-campaign.jpg'}" 
                     alt="${result.title}" class="rounded me-2" style="width: 40px; height: 40px; object-fit: cover;">
                <div>
                    <div class="fw-bold">${result.title}</div>
                    <small class="text-muted">${result.description}</small>
                </div>
            </div>
        </a>
    `).join('');
}

// ===== RESPONSIVE HANDLING =====
function handleResize() {
    const isMobile = window.innerWidth < 768;
    
    // Adjust navbar for mobile
    const navbar = document.getElementById('mainNav');
    if (navbar) {
        if (isMobile) {
            navbar.classList.add('mobile');
        } else {
            navbar.classList.remove('mobile');
        }
    }
    
    // Adjust card layouts
    const campaignCards = document.querySelectorAll('.campaign-card');
    campaignCards.forEach(card => {
        if (isMobile) {
            card.classList.add('mobile-layout');
        } else {
            card.classList.remove('mobile-layout');
        }
    });
}

const debouncedResize = debounce(handleResize, 250);

// ===== INITIALIZATION =====
document.addEventListener('DOMContentLoaded', function() {
    initNavbar();
    initBackToTop();
    initLoadingSpinner();
    initPasswordToggles();
    initSmoothScrolling();
    validateForm();
    initAnimations();
    initCampaignCards();
    initDonationForm();
    initShareButtons();
    initSearch();
    handleResize();
    
    // Event listeners
    window.addEventListener('resize', debouncedResize);
    
    // Global error handling
    window.addEventListener('error', (e) => {
        console.error('Global error:', e.error);
        showToast('Something went wrong. Please try again.', 'danger');
    });
    
    // Handle AJAX errors
    document.addEventListener('ajax:error', (e) => {
        showToast('Request failed. Please try again.', 'danger');
    });
});

// ===== EXPORT FUNCTIONS FOR GLOBAL USE =====
window.GiveGrip = {
    showToast,
    initSearch,
    shareCampaign: function(title, text, url) {
        if (navigator.share) {
            navigator.share({ title, text, url });
        } else {
            const shareUrl = `https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}&url=${encodeURIComponent(url)}`;
            window.open(shareUrl, '_blank');
        }
    }
};




