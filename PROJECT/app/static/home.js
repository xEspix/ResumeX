// Theme Toggle Functionality
const themeToggle = document.getElementById('theme-toggle');
const body = document.body;

// Check for saved theme or default to dark
const savedTheme = localStorage.getItem('theme') || 'dark';
body.setAttribute('data-theme', savedTheme);

themeToggle.addEventListener('click', () => {
    const currentTheme = body.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    body.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
});

// 3D Background Animation
class BackgroundAnimation {
    constructor() {
        this.canvas = document.getElementById('bg-canvas');
        this.ctx = this.canvas.getContext('2d');
        this.particles = [];
        this.floatingShapes = [];
        this.mouse = { x: 0, y: 0 };
        
        this.init();
        this.createParticles();
        this.createFloatingShapes();
        this.animate();
        this.bindEvents();
    }

    init() {
        this.resizeCanvas();
        window.addEventListener('resize', () => this.resizeCanvas());
        window.addEventListener('mousemove', (e) => {
            this.mouse.x = e.clientX;
            this.mouse.y = e.clientY;
        });
    }

    resizeCanvas() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }

    createParticles() {
        const particleCount = Math.floor((this.canvas.width * this.canvas.height) / 15000);
        
        for (let i = 0; i < particleCount; i++) {
            this.particles.push({
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height,
                size: Math.random() * 2 + 1,
                speedX: (Math.random() - 0.5) * 0.5,
                speedY: (Math.random() - 0.5) * 0.5,
                opacity: Math.random() * 0.5 + 0.1
            });
        }
    }

    createFloatingShapes() {
        const shapeCount = 8;
        const shapes = ['cube', 'sphere', 'pyramid', 'torus'];
        
        for (let i = 0; i < shapeCount; i++) {
            this.floatingShapes.push({
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height,
                size: Math.random() * 60 + 30,
                type: shapes[Math.floor(Math.random() * shapes.length)],
                rotation: Math.random() * Math.PI * 2,
                rotationSpeed: (Math.random() - 0.5) * 0.02,
                speedX: (Math.random() - 0.5) * 0.3,
                speedY: (Math.random() - 0.5) * 0.3,
                opacity: Math.random() * 0.1 + 0.05,
                color: `hsl(${Math.random() * 60 + 200}, 70%, 60%)`
            });
        }
    }

    drawParticle(particle) {
        this.ctx.save();
        this.ctx.globalAlpha = particle.opacity;
        this.ctx.fillStyle = this.getThemeColor();
        this.ctx.beginPath();
        this.ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
        this.ctx.fill();
        this.ctx.restore();
    }

    drawFloatingShape(shape) {
        this.ctx.save();
        this.ctx.translate(shape.x, shape.y);
        this.ctx.rotate(shape.rotation);
        this.ctx.globalAlpha = shape.opacity;
        this.ctx.strokeStyle = shape.color;
        this.ctx.lineWidth = 2;

        switch (shape.type) {
            case 'cube':
                this.drawWireframeCube(shape.size);
                break;
            case 'sphere':
                this.drawWireframeSphere(shape.size);
                break;
            case 'pyramid':
                this.drawWireframePyramid(shape.size);
                break;
            case 'torus':
                this.drawWireframeTorus(shape.size);
                break;
        }

        this.ctx.restore();
    }

    drawWireframeCube(size) {
        const half = size / 2;
        
        // Front face
        this.ctx.strokeRect(-half, -half, size, size);
        
        // Back face (simulated 3D)
        const offset = size * 0.3;
        this.ctx.beginPath();
        this.ctx.moveTo(-half + offset, -half - offset);
        this.ctx.lineTo(half + offset, -half - offset);
        this.ctx.lineTo(half + offset, half - offset);
        this.ctx.lineTo(-half + offset, half - offset);
        this.ctx.closePath();
        this.ctx.stroke();
        
        // Connecting lines
        this.ctx.beginPath();
        this.ctx.moveTo(-half, -half);
        this.ctx.lineTo(-half + offset, -half - offset);
        this.ctx.moveTo(half, -half);
        this.ctx.lineTo(half + offset, -half - offset);
        this.ctx.moveTo(half, half);
        this.ctx.lineTo(half + offset, half - offset);
        this.ctx.moveTo(-half, half);
        this.ctx.lineTo(-half + offset, half - offset);
        this.ctx.stroke();
    }

    drawWireframeSphere(size) {
        const radius = size / 2;
        
        // Main circle
        this.ctx.beginPath();
        this.ctx.arc(0, 0, radius, 0, Math.PI * 2);
        this.ctx.stroke();
        
        // Horizontal ellipse
        this.ctx.beginPath();
        this.ctx.ellipse(0, 0, radius, radius * 0.3, 0, 0, Math.PI * 2);
        this.ctx.stroke();
        
        // Vertical ellipse
        this.ctx.beginPath();
        this.ctx.ellipse(0, 0, radius * 0.3, radius, 0, 0, Math.PI * 2);
        this.ctx.stroke();
    }

    drawWireframePyramid(size) {
        const base = size / 2;
        const height = size * 0.8;
        
        this.ctx.beginPath();
        // Base
        this.ctx.moveTo(-base, base);
        this.ctx.lineTo(base, base);
        this.ctx.lineTo(base, -base);
        this.ctx.lineTo(-base, -base);
        this.ctx.closePath();
        
        // Lines to apex
        this.ctx.moveTo(-base, base);
        this.ctx.lineTo(0, -height);
        this.ctx.moveTo(base, base);
        this.ctx.lineTo(0, -height);
        this.ctx.moveTo(base, -base);
        this.ctx.lineTo(0, -height);
        this.ctx.moveTo(-base, -base);
        this.ctx.lineTo(0, -height);
        
        this.ctx.stroke();
    }

    drawWireframeTorus(size) {
        const outerRadius = size / 2;
        const innerRadius = size / 4;
        
        // Outer circle
        this.ctx.beginPath();
        this.ctx.arc(0, 0, outerRadius, 0, Math.PI * 2);
        this.ctx.stroke();
        
        // Inner circle
        this.ctx.beginPath();
        this.ctx.arc(0, 0, innerRadius, 0, Math.PI * 2);
        this.ctx.stroke();
        
        // Cross lines
        this.ctx.beginPath();
        this.ctx.ellipse(0, 0, outerRadius, outerRadius * 0.2, 0, 0, Math.PI * 2);
        this.ctx.stroke();
    }

    getThemeColor() {
        const theme = document.body.getAttribute('data-theme');
        return theme === 'light' ? 'rgba(59, 130, 246, 0.3)' : 'rgba(139, 92, 246, 0.4)';
    }

    updateParticles() {
        this.particles.forEach(particle => {
            particle.x += particle.speedX;
            particle.y += particle.speedY;

            // Mouse interaction
            const dx = this.mouse.x - particle.x;
            const dy = this.mouse.y - particle.y;
            const distance = Math.sqrt(dx * dx + dy * dy);
            
            if (distance < 100) {
                particle.x -= dx * 0.001;
                particle.y -= dy * 0.001;
            }

            // Boundary check
            if (particle.x < 0 || particle.x > this.canvas.width) particle.speedX *= -1;
            if (particle.y < 0 || particle.y > this.canvas.height) particle.speedY *= -1;

            // Keep within bounds
            particle.x = Math.max(0, Math.min(this.canvas.width, particle.x));
            particle.y = Math.max(0, Math.min(this.canvas.height, particle.y));
        });
    }

    updateFloatingShapes() {
        this.floatingShapes.forEach(shape => {
            shape.x += shape.speedX;
            shape.y += shape.speedY;
            shape.rotation += shape.rotationSpeed;

            // Boundary check
            if (shape.x < -100 || shape.x > this.canvas.width + 100) shape.speedX *= -1;
            if (shape.y < -100 || shape.y > this.canvas.height + 100) shape.speedY *= -1;
        });
    }

    drawConnections() {
        this.ctx.strokeStyle = this.getThemeColor();
        this.ctx.lineWidth = 1;

        for (let i = 0; i < this.particles.length; i++) {
            for (let j = i + 1; j < this.particles.length; j++) {
                const dx = this.particles[i].x - this.particles[j].x;
                const dy = this.particles[i].y - this.particles[j].y;
                const distance = Math.sqrt(dx * dx + dy * dy);

                if (distance < 120) {
                    this.ctx.globalAlpha = (120 - distance) / 120 * 0.1;
                    this.ctx.beginPath();
                    this.ctx.moveTo(this.particles[i].x, this.particles[i].y);
                    this.ctx.lineTo(this.particles[j].x, this.particles[j].y);
                    this.ctx.stroke();
                }
            }
        }
    }

    animate() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        this.updateParticles();
        this.updateFloatingShapes();

        // Draw floating shapes
        this.floatingShapes.forEach(shape => this.drawFloatingShape(shape));

        // Draw particles
        this.particles.forEach(particle => this.drawParticle(particle));

        // Draw connections
        this.drawConnections();

        requestAnimationFrame(() => this.animate());
    }

    bindEvents() {
        // Add parallax effect to hero content based on mouse movement
        document.addEventListener('mousemove', (e) => {
            const heroContent = document.querySelector('.hero-content');
            if (heroContent) {
                const x = (e.clientX / window.innerWidth) - 0.5;
                const y = (e.clientY / window.innerHeight) - 0.5;
                
                heroContent.style.transform = `translate(${x * 20}px, ${y * 20}px)`;
            }
        });
    }
}

// Feature Cards Animation
const observeFeatureCards = () => {
    const featureCards = document.querySelectorAll('.feature-card');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                const delay = entry.target.getAttribute('data-delay') || 0;
                setTimeout(() => {
                    entry.target.classList.add('visible');
                }, delay);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    featureCards.forEach(card => observer.observe(card));
};

// FAQ Functionality
const initFAQ = () => {
    const faqItems = document.querySelectorAll('.faq-item');
    
    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        
        question.addEventListener('click', () => {
            const isActive = item.classList.contains('active');
            
            // Close all items
            faqItems.forEach(otherItem => {
                otherItem.classList.remove('active');
            });
            
            // Open clicked item if it wasn't active
            if (!isActive) {
                item.classList.add('active');
            }
        });
    });
};

// Smooth scrolling for anchor links
const initSmoothScrolling = () => {
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
};

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new BackgroundAnimation();
    observeFeatureCards();
    initFAQ();
    initSmoothScrolling();
});

// Handle resize events
window.addEventListener('resize', () => {
    // Recalculate any size-dependent animations
    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach(card => {
        if (card.classList.contains('visible')) {
            card.style.transform = 'translateY(0)';
        }
    });
});
