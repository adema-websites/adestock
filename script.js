document.addEventListener('DOMContentLoaded', () => {

    // --- Navbar Scroll Effect ---
    const navbar = document.querySelector('.navbar');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // --- Mobile Menu Toggle ---
    const menuToggle = document.querySelector('.menu-toggle');
    const navLinks = document.querySelector('.nav-links');

    if (menuToggle && navLinks) {
        menuToggle.addEventListener('click', () => {
            navLinks.classList.toggle('active');
        });

        // Close menu when a link is clicked (for single-page navigation)
        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                if (navLinks.classList.contains('active')) {
                    navLinks.classList.remove('active');
                }
            });
        });
    }


    // --- FAQ Toggle ---
    const faqItems = document.querySelectorAll('.faq-item');
    faqItems.forEach(item => {
        const questionButton = item.querySelector('.faq-question');
        const answerDiv = item.querySelector('.faq-answer');

        if (questionButton && answerDiv) {
            questionButton.addEventListener('click', () => {
                const isActive = item.classList.contains('active');

                // Optional: Close other FAQs when one opens
                // faqItems.forEach(otherItem => {
                //     if (otherItem !== item) {
                //         otherItem.classList.remove('active');
                //         otherItem.querySelector('.faq-answer').style.maxHeight = null;
                //         otherItem.querySelector('.faq-question')?.classList.remove('active');
                //     }
                // });

                item.classList.toggle('active');
                questionButton.classList.toggle('active');

                if (item.classList.contains('active')) {
                    answerDiv.style.maxHeight = answerDiv.scrollHeight + "px";
                } else {
                    answerDiv.style.maxHeight = null;
                }
            });
        }
    });

    // --- Footer Year ---
     const footerYear = document.getElementById('footer-year');
     if (footerYear) {
        footerYear.textContent = new Date().getFullYear();
     }

    // --- Smooth Scrolling for Anchor Links (within index.html) ---
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            // Only prevent default if it's truly an anchor link on the same page
            if (href.length > 1 && document.querySelector(href)) {
                e.preventDefault();
                const targetElement = document.querySelector(href);
                if (targetElement) {
                    const offsetTop = targetElement.offsetTop - (navbar ? navbar.offsetHeight : 70); // Adjust for fixed navbar
                    window.scrollTo({
                        top: offsetTop,
                        behavior: 'smooth'
                    });
                     // Close mobile menu after clicking anchor link
                    if (navLinks && navLinks.classList.contains('active')) {
                        navLinks.classList.remove('active');
                    }
                }
            }
            // Allow default behavior for links like href="#" or external links
        });
    });

}); // End DOMContentLoaded