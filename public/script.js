document.addEventListener('DOMContentLoaded', () => {

    // --- Navbar Scroll Effect ---
    const navbar = document.querySelector('.navbar');
    const sharedNav = document.querySelector('.adestock-site-nav');

    if (navbar && !sharedNav) {
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
                    const openNavLinks = document.querySelector('.nav-links.active');
                    if (openNavLinks) {
                        openNavLinks.classList.remove('active');
                    }
                }
            }
            // Allow default behavior for links like href="#" or external links
        });
    });

    // --- Tutorial Sidebar (active state + mobile toggle) ---
    const tutorialSidebar = document.querySelector('.tutorial-sidebar');
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const sidebarNav = document.getElementById('tutorial-sidebar-links');
    const tutorialSections = document.querySelectorAll('article.tutorial-card[id]');
    const sidebarLinks = document.querySelectorAll('.tutorial-sidebar-nav a');

    if (sidebarToggle && sidebarNav && tutorialSidebar) {
        sidebarToggle.addEventListener('click', () => {
            const isOpen = tutorialSidebar.classList.toggle('is-open');
            sidebarToggle.setAttribute('aria-expanded', isOpen);
        });

        sidebarNav.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                if (window.innerWidth <= 980) {
                    tutorialSidebar.classList.remove('is-open');
                    sidebarToggle.setAttribute('aria-expanded', 'false');
                }
            });
        });
    }

    if (tutorialSections.length && sidebarLinks.length) {
        const linkMap = new Map();
        sidebarLinks.forEach(link => linkMap.set(link.getAttribute('href'), link));

        sidebarLinks.forEach(link => link.classList.remove('active'));
        const firstLink = sidebarLinks[0];
        if (firstLink) {
            firstLink.classList.add('active');
        }

        const observer = new IntersectionObserver(
            entries => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const id = `#${entry.target.id}`;
                        sidebarLinks.forEach(link => link.classList.remove('active'));
                        const activeLink = linkMap.get(id);
                        if (activeLink) {
                            activeLink.classList.add('active');
                        }
                    }
                });
            },
            { rootMargin: '-20% 0px -60% 0px', threshold: 0.1 }
        );

        tutorialSections.forEach(section => observer.observe(section));
    }

    // --- Download Modal ---
    const downloadModal = document.getElementById('downloadModal');
    const openDownloadModalBtns = document.querySelectorAll('#openDownloadModal, .open-download-modal');
    const closeDownloadModalBtn = document.getElementById('closeDownloadModal');
    const closeModalButton = document.getElementById('closeModalButton');
    const downloadButton = document.getElementById('downloadButton');

    // Función para abrir el modal
    const openModal = (e) => {
        if (e) {
            e.preventDefault(); // Prevenir comportamiento por defecto de enlaces
        }
        if (downloadModal) {
            downloadModal.classList.add('active');
            document.body.style.overflow = 'hidden'; // Prevenir scroll del body
        }
    };

    // Función para cerrar el modal
    const closeModal = () => {
        if (downloadModal) {
            downloadModal.classList.remove('active');
            document.body.style.overflow = ''; // Restaurar scroll del body
            // Pausar el video cuando se cierra el modal
            const video = downloadModal.querySelector('video');
            if (video) {
                video.pause();
            }
        }
    };

    // Event listeners para TODOS los botones que abren el modal
    openDownloadModalBtns.forEach(btn => {
        if (btn) {
            btn.addEventListener('click', openModal);
        }
    });

    if (closeDownloadModalBtn) {
        closeDownloadModalBtn.addEventListener('click', closeModal);
    }

    if (closeModalButton) {
        closeModalButton.addEventListener('click', closeModal);
    }

    // Cerrar modal al hacer clic fuera del contenido
    if (downloadModal) {
        downloadModal.addEventListener('click', (e) => {
            if (e.target === downloadModal) {
                closeModal();
            }
        });
    }

    // Cerrar modal con tecla Escape
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && downloadModal && downloadModal.classList.contains('active')) {
            closeModal();
        }
    });

    // --- Copy to Clipboard ---
    const copyButtons = document.querySelectorAll('.copy-btn');
    copyButtons.forEach(button => {
        button.addEventListener('click', async () => {
            const textToCopy = button.getAttribute('data-copy');
            const icon = button.querySelector('i');
            
            try {
                await navigator.clipboard.writeText(textToCopy);
                
                // Cambiar el icono temporalmente para feedback visual
                icon.classList.remove('fa-copy');
                icon.classList.add('fa-check');
                button.classList.add('copied');
                
                // Restaurar el icono después de 2 segundos
                setTimeout(() => {
                    icon.classList.remove('fa-check');
                    icon.classList.add('fa-copy');
                    button.classList.remove('copied');
                }, 2000);
            } catch (err) {
                console.error('Error al copiar:', err);
                // Fallback para navegadores antiguos
                const textArea = document.createElement('textarea');
                textArea.value = textToCopy;
                textArea.style.position = 'fixed';
                textArea.style.left = '-999999px';
                document.body.appendChild(textArea);
                textArea.select();
                try {
                    document.execCommand('copy');
                    icon.classList.remove('fa-copy');
                    icon.classList.add('fa-check');
                    button.classList.add('copied');
                    setTimeout(() => {
                        icon.classList.remove('fa-check');
                        icon.classList.add('fa-copy');
                        button.classList.remove('copied');
                    }, 2000);
                } catch (err2) {
                    console.error('Fallback también falló:', err2);
                }
                document.body.removeChild(textArea);
            }
        });
    });

}); // End DOMContentLoaded