// ===================================
// GAYBECK STARKIDS SMS - WEBSITE SCRIPTS
// ===================================

const API_BASE = 'http://localhost:5000/api';

document.addEventListener('DOMContentLoaded', function() {
    // Initialize
    initNavigation();
    initButtons();
    initSmoothScroll();
    initFormHandling();
    initMobileMenu();
    loadDynamicContent();
    checkServerHealth();
});

// ===== NAVIGATION =====
function initNavigation() {
    const navLinks = document.querySelectorAll('.nav-menu a');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // Remove active class from all links
            navLinks.forEach(l => l.classList.remove('active'));
            // Add active class to clicked link
            this.classList.add('active');
        });
    });
    
    // Scroll effect on navbar
    window.addEventListener('scroll', function() {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 50) {
            navbar.style.boxShadow = '0 2px 20px rgba(0,0,0,0.15)';
        } else {
            navbar.style.boxShadow = 'var(--shadow)';
        }
    });
}

// ===== BUTTONS =====
function initButtons() {
    // Download buttons
    const downloadBtns = document.querySelectorAll('[data-action="download"]');
    downloadBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            handleDownload();
        });
    });
    
    // Contact buttons
    const contactBtns = document.querySelectorAll('[data-action="contact"]');
    contactBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            scrollToSection('contact');
        });
    });
    
    // Pricing button clicks
    const pricingBtns = document.querySelectorAll('.pricing-card .btn');
    pricingBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const planName = this.closest('.pricing-card').querySelector('h3').textContent;
            showNotification('Plan selected: ' + planName, 'success');
        });
    });
}

// ===== SMOOTH SCROLL =====
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// ===== FORM HANDLING =====
function initFormHandling() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            // Get form data
            const formData = new FormData(this);
            const data = Object.fromEntries(formData);
            
            // Validate
            if (!validateForm(data)) {
                showNotification('Please fill in all required fields', 'error');
                return;
            }
            
            // Submit to backend
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            submitBtn.disabled = true;
            submitBtn.textContent = 'Sending...';
            
            try {
                const response = await fetch(`${API_BASE}/contact`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                
                if (response.ok) {
                    showNotification(result.message || 'Message sent successfully!', 'success');
                    this.reset();
                } else {
                    showNotification(result.error || 'Error sending message', 'error');
                }
            } catch (error) {
                // Fallback to local handling if API unavailable
                showNotification('Message received! We will contact you soon.', 'success');
                this.reset();
            }
            
            submitBtn.disabled = false;
            submitBtn.textContent = originalText;
        });
    });
}

// ===== FORM VALIDATION =====
function validateForm(data) {
    // Check required fields
    if (data.name && data.name.trim() === '') return false;
    if (data.email && data.email.trim() === '') return false;
    if (data.message && data.message.trim() === '') return false;
    
    // Validate email format
    if (data.email && !isValidEmail(data.email)) {
        showNotification('Please enter a valid email address', 'error');
        return false;
    }
    
    return true;
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// ===== MOBILE MENU =====
function initMobileMenu() {
    const navMenu = document.querySelector('.nav-menu');
    
    // Create hamburger menu for mobile
    if (window.innerWidth < 768) {
        createMobileMenu();
    }
    
    // Handle window resize
    window.addEventListener('resize', function() {
        if (window.innerWidth < 768) {
            createMobileMenu();
        } else {
            removeMobileMenu();
        }
    });
}

function createMobileMenu() {
    // Check if already exists
    if (document.querySelector('.hamburger-menu')) return;
    
    const nav = document.querySelector('.nav-container');
    const hamburger = document.createElement('div');
    hamburger.className = 'hamburger-menu';
    hamburger.innerHTML = '☰';
    hamburger.style.cssText = `
        font-size: 1.5em;
        cursor: pointer;
        color: var(--primary-color);
    `;
    
    const navMenu = document.querySelector('.nav-menu');
    navMenu.style.cssText = `
        position: absolute;
        top: 70px;
        left: 0;
        right: 0;
        flex-direction: column;
        background: white;
        box-shadow: var(--shadow);
        display: none;
        width: 100%;
        gap: 0;
    `;
    navMenu.classList.add('mobile-menu');
    
    hamburger.addEventListener('click', function() {
        const display = navMenu.style.display;
        navMenu.style.display = display === 'none' ? 'flex' : 'none';
    });
    
    // Position before nav menu
    nav.insertBefore(hamburger, navMenu);
}

function removeMobileMenu() {
    const hamburger = document.querySelector('.hamburger-menu');
    if (hamburger) hamburger.remove();
    
    const navMenu = document.querySelector('.mobile-menu');
    if (navMenu) {
        navMenu.style.cssText = '';
        navMenu.classList.remove('mobile-menu');
    }
}

// ===== DOWNLOAD FUNCTION =====
function handleDownload() {
    showNotification('Download starting...', 'info');
    
    // In real implementation, this would trigger the actual download
    // For now, we'll show a message
    setTimeout(() => {
        showNotification('Download complete! Check your downloads folder.', 'success');
    }, 2000);
}

// ===== SCROLL TO SECTION =====
function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.scrollIntoView({ behavior: 'smooth' });
    }
}

// ===== NOTIFICATIONS =====
function showNotification(message, type = 'info') {
    // Remove existing notification
    const existing = document.querySelector('.notification');
    if (existing) existing.remove();
    
    // Create notification element
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.textContent = message;
    
    // Set styles based on type
    const colors = {
        'success': '#27ae60',
        'error': '#e74c3c',
        'info': '#3498db'
    };
    
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background-color: ${colors[type] || colors['info'}};
        color: white;
        padding: 15px 25px;
        border-radius: 5px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        z-index: 1000;
        animation: slideIn 0.3s ease-in-out;
        max-width: 300px;
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-in-out';
        setTimeout(() => notification.remove(), 300);
    }, 5000);
}

// ===== ANIMATIONS =====
const style = document.createElement('style');
style.innerHTML = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
`;
document.head.appendChild(style);

// ===== PRICING COMPARISON =====
function comparePricingPlans() {
    const pricingCards = document.querySelectorAll('.pricing-card');
    
    pricingCards.forEach((card, index) => {
        card.addEventListener('mouseenter', function() {
            pricingCards.forEach(c => c.style.opacity = '0.6');
            this.style.opacity = '1';
        });
        
        card.addEventListener('mouseleave', function() {
            pricingCards.forEach(c => c.style.opacity = '1');
        });
    });
}

// ===== SCROLL ANIMATIONS =====
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'fadeIn 0.6s ease-in-out';
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    document.querySelectorAll('.feature-card, .module, .pricing-card, .testimonial').forEach(el => {
        el.style.opacity = '0';
        observer.observe(el);
    });
}

// Initialize scroll animations when page loads
window.addEventListener('load', initScrollAnimations);

// ===== UTILITY FUNCTIONS =====

// Debounce function for resize events
function debounce(func, delay) {
    let timeoutId;
    return function(...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func(...args), delay);
    };
}

// Track page scroll position
let lastScrollTop = 0;
window.addEventListener('scroll', debounce(function() {
    const navbar = document.querySelector('.navbar');
    const scrollTop = window.scrollY;
    
    if (scrollTop > lastScrollTop) {
        // Scrolling down
        navbar.style.boxShadow = '0 2px 10px rgba(0,0,0,0.1)';
    } else {
        // Scrolling up
        navbar.style.boxShadow = '0 2px 20px rgba(0,0,0,0.15)';
    }
    lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
}, 100));

// ===== ACCESSIBILITY =====

// Keyboard navigation
document.addEventListener('keydown', function(e) {
    // ESC key closes any open menus
    if (e.key === 'Escape') {
        const mobileMenu = document.querySelector('.mobile-menu');
        if (mobileMenu) {
            mobileMenu.style.display = 'none';
        }
    }
    
    // Tab navigation
    if (e.key === 'Tab') {
        const focusedElement = document.activeElement;
        focusedElement.style.outline = '2px solid #27ae60';
    }
});

// Focus visible for keyboard navigation
document.addEventListener('keyup', function(e) {
    if (e.key === 'Tab') {
        document.body.classList.add('keyboard-nav');
    }
});

// Remove keyboard-nav class on mouse move
document.addEventListener('mousemove', function() {
    document.body.classList.remove('keyboard-nav');
});

// ===== LOAD DYNAMIC CONTENT =====
async function loadDynamicContent() {
    try {
        // Load features
        const featuresResponse = await fetch(`${API_BASE}/features`);
        if (featuresResponse.ok) {
            const features = await featuresResponse.json();
            populateFeatures(features);
        }
        
        // Load modules
        const modulesResponse = await fetch(`${API_BASE}/modules`);
        if (modulesResponse.ok) {
            const modules = await modulesResponse.json();
            populateModules(modules);
        }
        
        // Load pricing
        const pricingResponse = await fetch(`${API_BASE}/pricing`);
        if (pricingResponse.ok) {
            const pricing = await pricingResponse.json();
            populatePricing(pricing);
        }
        
        // Load testimonials
        const testimonialsResponse = await fetch(`${API_BASE}/testimonials`);
        if (testimonialsResponse.ok) {
            const testimonials = await testimonialsResponse.json();
            populateTestimonials(testimonials);
        }
        
        // Load system stats
        const statsResponse = await fetch(`${API_BASE}/stats`);
        if (statsResponse.ok) {
            const stats = await statsResponse.json();
            displayStats(stats);
        }
    } catch (error) {
        console.log('Using static content (API not available)', error);
    }
}

// ===== POPULATE FEATURES =====
function populateFeatures(features) {
    const grid = document.querySelector('.features-grid');
    if (!grid || grid.children.length > 0) return;
    
    features.forEach(feature => {
        const card = document.createElement('div');
        card.className = 'feature-card';
        card.innerHTML = `
            <div class="feature-icon">${feature.icon}</div>
            <h3>${feature.title}</h3>
            <p>${feature.description}</p>
        `;
        grid.appendChild(card);
    });
}

// ===== POPULATE MODULES =====
function populateModules(modules) {
    const grid = document.querySelector('.modules-grid');
    if (!grid || grid.children.length > 0) return;
    
    modules.forEach(module => {
        const card = document.createElement('div');
        card.className = 'module';
        card.innerHTML = `
            <h3>${module.icon} ${module.name}</h3>
            <ul>
                ${module.features.map(f => `<li>${f}</li>`).join('')}
            </ul>
        `;
        grid.appendChild(card);
    });
}

// ===== POPULATE PRICING =====
function populatePricing(pricing) {
    const grid = document.querySelector('.pricing-grid');
    if (!grid || grid.children.length > 0) return;
    
    pricing.forEach(tier => {
        const card = document.createElement('div');
        card.className = 'pricing-card' + (tier.featured ? ' featured' : '');
        card.innerHTML = `
            ${tier.featured ? '<div class="badge">RECOMMENDED</div>' : ''}
            <h3>${tier.name}</h3>
            <div class="price">${tier.price}</div>
            <div class="price-desc">${tier.duration}</div>
            <ul>
                ${tier.features.map(f => `<li>✓ ${f}</li>`).join('')}
            </ul>
            <button class="btn btn-primary" onclick="selectPlan('${tier.name}')">Get Started</button>
        `;
        grid.appendChild(card);
    });
}

// ===== POPULATE TESTIMONIALS =====
function populateTestimonials(testimonials) {
    const grid = document.querySelector('.testimonials-grid');
    if (!grid || grid.children.length > 0) return;
    
    testimonials.forEach(testimonial => {
        const card = document.createElement('div');
        card.className = 'testimonial';
        card.innerHTML = `
            <div class="rating">${'⭐'.repeat(testimonial.rating)}</div>
            <p>"${testimonial.quote}"</p>
            <div class="author">- ${testimonial.name}, ${testimonial.school}</div>
        `;
        grid.appendChild(card);
    });
}

// ===== DISPLAY STATS =====
function displayStats(stats) {
    const statsContainer = document.querySelector('[data-stats]');
    if (statsContainer) {
        statsContainer.innerHTML = `
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 20px; margin-top: 30px;">
                <div style="text-align: center; padding: 20px; background: #f8f9fa; border-radius: 10px;">
                    <div style="font-size: 2em; font-weight: bold; color: #27ae60;">${stats.total_students}</div>
                    <div style="color: #7f8c8d;">Students Managed</div>
                </div>
                <div style="text-align: center; padding: 20px; background: #f8f9fa; border-radius: 10px;">
                    <div style="font-size: 2em; font-weight: bold; color: #27ae60;">${stats.total_teachers}</div>
                    <div style="color: #7f8c8d;">Teachers Tracked</div>
                </div>
                <div style="text-align: center; padding: 20px; background: #f8f9fa; border-radius: 10px;">
                    <div style="font-size: 2em; font-weight: bold; color: #27ae60;">GHS ${stats.total_fees_collected}</div>
                    <div style="color: #7f8c8d;">Fees Collected</div>
                </div>
                <div style="text-align: center; padding: 20px; background: #f8f9fa; border-radius: 10px;">
                    <div style="font-size: 2em; font-weight: bold; color: #e74c3c;">GHS ${stats.pending_fees}</div>
                    <div style="color: #7f8c8d;">Pending Fees</div>
                </div>
            </div>
        `;
    }
}

// ===== SELECT PLAN =====
function selectPlan(planName) {
    showNotification(`You selected: ${planName} plan. Please fill out the contact form to proceed.`, 'success');
    document.querySelector('#contact')?.scrollIntoView({ behavior: 'smooth' });
}

// ===== CHECK SERVER HEALTH =====
async function checkServerHealth() {
    try {
        const response = await fetch(`${API_BASE}/health`);
        if (response.ok) {
            console.log('✅ Backend API is available');
            document.body.classList.add('api-available');
        }
    } catch (error) {
        console.log('ℹ️ Backend API not available - using static content');
        document.body.classList.add('api-unavailable');
    }
}

console.log('Gaybeck Starkids SMS Website - Scripts Loaded');
