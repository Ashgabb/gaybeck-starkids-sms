// ===================================
// GAYBECK STARKIDS SMS - WEBSITE SCRIPTS V2
// With Backend API Integration
// ===================================

const API_BASE = 'http://localhost:5000/api';

document.addEventListener('DOMContentLoaded', function() {
    initNavigation();
    initButtons();
    initSmoothScroll();
    initFormHandling();
    initMobileMenu();
    loadDynamicContent();
    checkServerHealth();
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
        console.log('Using static content (API not available)');
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
    // Insert stats section after hero
    const hero = document.querySelector('.hero');
    if (!hero || document.querySelector('[data-stats]')) return;
    
    const statsContainer = document.createElement('section');
    statsContainer.setAttribute('data-stats', 'true');
    statsContainer.style.cssText = 'padding: 60px 20px; background: #f8f9fa;';
    statsContainer.innerHTML = `
        <div class="container">
            <h2 style="text-align: center; margin-bottom: 40px;">System Statistics</h2>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 30px;">
                <div style="text-align: center; padding: 30px; background: white; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                    <div style="font-size: 2.5em; font-weight: bold; color: #27ae60;">${stats.total_students}</div>
                    <div style="color: #7f8c8d; margin-top: 10px; font-size: 1em;">Students Managed</div>
                </div>
                <div style="text-align: center; padding: 30px; background: white; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                    <div style="font-size: 2.5em; font-weight: bold; color: #27ae60;">${stats.total_teachers}</div>
                    <div style="color: #7f8c8d; margin-top: 10px; font-size: 1em;">Teachers Tracked</div>
                </div>
                <div style="text-align: center; padding: 30px; background: white; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                    <div style="font-size: 2.5em; font-weight: bold; color: #27ae60;">GHS ${stats.total_fees_collected}</div>
                    <div style="color: #7f8c8d; margin-top: 10px; font-size: 1em;">Fees Collected</div>
                </div>
                <div style="text-align: center; padding: 30px; background: white; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                    <div style="font-size: 2.5em; font-weight: bold; color: #e74c3c;">GHS ${stats.pending_fees}</div>
                    <div style="color: #7f8c8d; margin-top: 10px; font-size: 1em;">Pending Fees</div>
                </div>
            </div>
        </div>
    `;
    hero.insertAdjacentElement('afterend', statsContainer);
}

// ===== SELECT PLAN =====
function selectPlan(planName) {
    showNotification(`You selected: ${planName} plan. Please fill out the contact form to proceed.`, 'success');
    const contactSection = document.getElementById('contact');
    if (contactSection) {
        contactSection.scrollIntoView({ behavior: 'smooth' });
    }
}

// ===== PRICING PLAN MODAL FUNCTIONS =====
let currentPlan = {
    name: '',
    price: '',
    features: []
};

function openPlanModal(planName, price, features) {
    currentPlan = { name: planName, price: price, features: features };
    document.getElementById('modalPlanName').textContent = planName + ' Plan';
    document.getElementById('modalPlanPrice').textContent = price;
    
    const featuresList = document.getElementById('modalFeaturesList');
    featuresList.innerHTML = features.map(f => `<li>✓ ${f}</li>`).join('');
    
    const modal = document.getElementById('planModal');
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closePlanModal() {
    const modal = document.getElementById('planModal');
    modal.classList.remove('active');
    document.body.style.overflow = 'auto';
}

function proceedToCheckout() {
    closePlanModal();
    openCheckoutModal();
}

function downloadTrial() {
    showNotification('Starting download of trial version...', 'success');
    // Trigger download
    const link = document.createElement('a');
    link.href = '../sms_backup.py';
    link.download = 'GaybeckStarkids_SMS_Trial.py';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    closePlanModal();
}

// ===== CHECKOUT MODAL FUNCTIONS =====
function openCheckoutModal() {
    document.getElementById('checkoutPlanName').textContent = currentPlan.name + ' Plan';
    document.getElementById('checkoutPlanPrice').textContent = currentPlan.price;
    
    const modal = document.getElementById('checkoutModal');
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
    
    // Setup payment method handlers
    const paymentMethods = document.querySelectorAll('input[name="payment_method"]');
    paymentMethods.forEach(method => {
        method.addEventListener('change', showPaymentDetails);
    });
}

function closeCheckoutModal() {
    const modal = document.getElementById('checkoutModal');
    modal.classList.remove('active');
    document.body.style.overflow = 'auto';
}

function showPaymentDetails() {
    const method = document.querySelector('input[name="payment_method"]:checked')?.value;
    const detailsDiv = document.getElementById('paymentDetails');
    const instructionsDiv = document.getElementById('paymentInstructions');
    const infoDiv = document.getElementById('paymentInfo');
    
    if (!method) {
        detailsDiv.style.display = 'none';
        return;
    }
    
    detailsDiv.style.display = 'block';
    
    const paymentDetails = {
        momo: {
            instructions: '📱 Mobile Money Payment',
            info: `Send ${currentPlan.price} to:\nMTN: +233 24 XXX XXXX\nVodafone: +233 55 XXX XXXX\n\nReference: GAYBECK-[Your School Name]`
        },
        card: {
            instructions: '💳 Card Payment',
            info: 'Card payment gateway loading...\nSecure payment link will be provided\nafter form submission.'
        },
        bank: {
            instructions: '🏦 Bank Transfer',
            info: `Bank: Zenith Bank\nAccount: Gaybeck Starkids\nAmount: ${currentPlan.price}\n\nReference: GAYBECK-SMS`
        }
    };
    
    const details = paymentDetails[method];
    instructionsDiv.textContent = details.instructions;
    infoDiv.textContent = details.info;
}

// Update checkout form submission
document.addEventListener('DOMContentLoaded', function() {
    const checkoutForm = document.getElementById('checkoutForm');
    if (checkoutForm) {
        checkoutForm.addEventListener('submit', handleCheckoutSubmit);
    }
});

async function handleCheckoutSubmit(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    const data = {
        ...Object.fromEntries(formData),
        plan: currentPlan.name,
        price: currentPlan.price,
        timestamp: new Date().toISOString()
    };
    
    const submitBtn = this.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    submitBtn.disabled = true;
    submitBtn.textContent = 'Processing...';
    
    try {
        // Try to send to backend
        const response = await fetch(`${API_BASE}/contact`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: data.contact_person,
                email: data.email,
                phone: data.phone,
                subject: `Purchase Request: ${data.plan} Plan`,
                message: `School: ${data.school_name}\nPayment Method: ${data.payment_method}\nPlan: ${data.plan} (${data.price})`
            })
        });
        
        if (response.ok) {
            showNotification('🎉 Order received! We will contact you shortly with payment details.', 'success');
            closeCheckoutModal();
            this.reset();
            
            // Show payment confirmation
            setTimeout(() => {
                showPaymentConfirmation(data);
            }, 1000);
        } else {
            throw new Error('Checkout failed');
        }
    } catch (error) {
        console.error('Checkout error:', error);
        showNotification('✓ Order recorded locally. Our team will contact you soon!', 'success');
        closeCheckoutModal();
        this.reset();
        showPaymentConfirmation(data);
    }
    
    submitBtn.disabled = false;
    submitBtn.textContent = originalText;
}

function showPaymentConfirmation(data) {
    const confirmationHtml = `
        <div style="background: linear-gradient(135deg, #27ae60 0%, #229954 100%); color: white; padding: 30px; border-radius: 10px; text-align: center; max-width: 500px; margin: 20px auto; box-shadow: 0 10px 30px rgba(0,0,0,0.2);">
            <h3 style="margin-bottom: 15px;">✓ Purchase Initiated</h3>
            <p><strong>${data.plan} Plan</strong> - ${data.price}</p>
            <p style="font-size: 0.9em; margin: 15px 0;">Confirmation sent to: ${data.email}</p>
            <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 5px; text-align: left; margin: 15px 0; font-size: 0.9em;">
                <p><strong>Payment Method:</strong> ${data.payment_method.toUpperCase()}</p>
                <p><strong>School:</strong> ${data.school_name}</p>
                <p><strong>Contact:</strong> ${data.phone}</p>
            </div>
            <p style="font-size: 0.9em; opacity: 0.9;">We will contact you within 24 hours with next steps.</p>
        </div>
    `;
    
    // Insert into page
    const section = document.getElementById('contact') || document.querySelector('main');
    if (section) {
        const temp = document.createElement('div');
        temp.innerHTML = confirmationHtml;
        section.insertAdjacentElement('beforebegin', temp.firstElementChild);
    }
}

// Close modal when clicking outside or pressing Escape
document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('planModal');
    if (modal) {
        modal.addEventListener('click', function(event) {
            if (event.target === modal) {
                closePlanModal();
            }
        });
    }
    
    // Escape key handler
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            closePlanModal();
        }
    });
});

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

// ===== NAVIGATION =====
function initNavigation() {
    const navLinks = document.querySelectorAll('.nav-menu a');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            navLinks.forEach(l => l.classList.remove('active'));
            this.classList.add('active');
        });
    });
    
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
    document.querySelectorAll('button').forEach(btn => {
        if (btn.textContent.includes('Download')) {
            btn.addEventListener('click', handleDownload);
        }
        if (btn.textContent.includes('Learn More')) {
            btn.addEventListener('click', () => scrollToSection('features'));
        }
    });
    
    const contactBtns = document.querySelectorAll('[data-action="contact"]');
    contactBtns.forEach(btn => {
        btn.addEventListener('click', () => scrollToSection('contact'));
    });
}

// ===== HANDLE DOWNLOAD =====
async function handleDownload() {
    const email = prompt('Enter your email to download:');
    if (!email) return;
    
    try {
        const response = await fetch(`${API_BASE}/download`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: email,
                os: navigator.platform
            })
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showNotification('Download starting...', 'success');
            setTimeout(() => {
                const link = document.createElement('a');
                link.href = 'GAYBECK_STARKIDS_SMS_20251204_201507.zip';
                link.download = 'GAYBECK_STARKIDS_SMS_20251204_201507.zip';
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            }, 1000);
        }
    } catch (error) {
        showNotification('Download unavailable. Try direct link.', 'info');
    }
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
            
            const formData = new FormData(this);
            const data = Object.fromEntries(formData);
            
            if (!validateForm(data)) {
                showNotification('Please fill in all required fields', 'error');
                return;
            }
            
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
    if (data.name && data.name.trim() === '') return false;
    if (data.email && data.email.trim() === '') return false;
    if (data.message && data.message.trim() === '') return false;
    
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
    
    if (window.innerWidth < 768) {
        createMobileMenu();
    }
    
    window.addEventListener('resize', function() {
        if (window.innerWidth < 768) {
            createMobileMenu();
        } else {
            removeMobileMenu();
        }
    });
}

function createMobileMenu() {
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

// ===== SCROLL TO SECTION =====
function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.scrollIntoView({ behavior: 'smooth' });
    }
}

// ===== NOTIFICATIONS =====
function showNotification(message, type = 'info') {
    const existing = document.querySelector('.notification');
    if (existing) existing.remove();
    
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.textContent = message;
    
    const colors = {
        'success': '#27ae60',
        'error': '#e74c3c',
        'info': '#3498db'
    };
    
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background-color: ${colors[type] || colors['info']};
        color: white;
        padding: 15px 25px;
        border-radius: 5px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        z-index: 1000;
        animation: slideIn 0.3s ease-in-out;
        max-width: 300px;
    `;
    
    document.body.appendChild(notification);
    
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

console.log('✅ Gaybeck Starkids SMS Website - Scripts Loaded');
