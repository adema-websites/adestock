(function () {
    function getRelativePrefix() {
        var path = window.location.pathname.replace(/\\/g, '/');
        var normalized = path.endsWith('/') ? path + 'index.html' : path;
        var segments = normalized.split('/').filter(Boolean);
        var repoIndex = segments.lastIndexOf('adestock');

        if (repoIndex >= 0) {
            segments = segments.slice(repoIndex + 1);
        }

        var last = segments[segments.length - 1] || '';
        var pointsToFile = /\.[a-z0-9]+$/i.test(last);
        var folderDepth = Math.max(0, segments.length - (pointsToFile ? 1 : 0));

        return '../'.repeat(folderDepth);
    }

    function getCurrentPath() {
        var path = window.location.pathname.replace(/\\/g, '/');
        var normalized = path.endsWith('/') ? path + 'index.html' : path;
        var segments = normalized.split('/').filter(Boolean);
        var repoIndex = segments.lastIndexOf('adestock');

        if (repoIndex >= 0) {
            segments = segments.slice(repoIndex + 1);
        }

        if (!segments.length || segments[0] === 'index.html') {
            return 'index.html';
        }

        if (segments[segments.length - 1] === 'index.html') {
            segments.pop();
            return segments.join('/') + '/';
        }

        return segments.join('/');
    }

    function buildNav(prefix) {
        function href(path) {
            return prefix + path;
        }

        return '' +
            '<nav class="navbar adestock-site-nav" aria-label="Navegación principal">' +
                '<div class="logo">' +
                    '<a href="' + href('index.html') + '" class="logo" aria-label="Ir al inicio de ADEstock">' +
                        '<img src="' + href('img/logo-home.svg') + '" alt="Logo de ADEstock" class="logo-img">' +
                    '</a>' +
                '</div>' +
                '<button class="menu-toggle" type="button" aria-label="Abrir menú" aria-expanded="false">☰</button>' +
                '<ul class="nav-links">' +
                    '<li><a href="' + href('index.html#features') + '">Características</a></li>' +
                    '<li><a href="' + href('sistema-de-stock/') + '" data-route="sistema-de-stock/">Sistema de stock</a></li>' +
                    '<li><a href="' + href('control-de-stock/') + '" data-route="control-de-stock/">Control de stock</a></li>' +
                    '<li><a href="' + href('index.html#target-audience') + '">¿Para quién es?</a></li>' +
                    '<li><a href="' + href('index.html#faq') + '">Preguntas frecuentes</a></li>' +
                    '<li><a href="' + href('precios.html') + '" data-route="precios.html">Precios</a></li>' +
                    '<li><a href="' + href('blog/') + '" data-route="blog/">Guías</a></li>' +
                    '<li><a href="' + href('tutoriales.html') + '" data-route="tutoriales.html">Tutoriales</a></li>' +
                    '<li><a href="' + href('descargar-demo.html') + '" class="cta-button" data-route="descargar-demo.html">Descargar</a></li>' +
                '</ul>' +
            '</nav>';
    }

    function injectNavStyles() {
        if (document.getElementById('adestock-site-nav-styles')) {
            return;
        }

        var style = document.createElement('style');
        style.id = 'adestock-site-nav-styles';
        style.textContent = '' +
            '.adestock-site-nav{position:fixed;top:0;left:0;right:0;height:80px;padding:0 2rem;display:flex;align-items:center;justify-content:space-between;z-index:1000;background:rgba(255,255,255,.86);backdrop-filter:blur(12px);border-bottom:1px solid rgba(15,23,42,.08);font-family:Inter,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;box-sizing:border-box}' +
            '.adestock-site-nav *{box-sizing:border-box}' +
            '.adestock-site-nav .logo,.adestock-site-nav .logo a{display:flex;align-items:center;text-decoration:none}' +
            '.adestock-site-nav .logo img{height:40px;width:auto;display:block}' +
            '.adestock-site-nav .nav-links{display:flex;align-items:center;gap:2.5rem;list-style:none;margin:0;padding:0}' +
            '.adestock-site-nav .nav-links a{color:#475569;text-decoration:none;font-weight:600;font-size:.95rem;line-height:1.25;transition:color .2s ease}' +
            '.adestock-site-nav .nav-links a:hover,.adestock-site-nav .nav-links a.is-active{color:#2563eb}' +
            '.adestock-site-nav .nav-links a.is-active{font-weight:800}' +
            '.adestock-site-nav .cta-button{display:inline-flex;align-items:center;justify-content:center;background:#2563eb;color:#fff!important;border-radius:9999px;padding:.9rem 1.9rem;font-weight:800;box-shadow:0 10px 18px rgba(37,99,235,.22);white-space:nowrap}' +
            '.adestock-site-nav .cta-button:hover{background:#1d4ed8;color:#fff!important;transform:translateY(-1px)}' +
            '.adestock-site-nav .menu-toggle{display:none;background:transparent;border:0;color:#0f172a;font-size:1.55rem;line-height:1;cursor:pointer;padding:.4rem}' +
            '.adestock-site-nav.scrolled{background:rgba(255,255,255,.94);box-shadow:0 8px 24px rgba(15,23,42,.08)}' +
            '@media (max-width:1100px){.adestock-site-nav{padding:0 1rem}.adestock-site-nav .nav-links{gap:1.15rem}.adestock-site-nav .nav-links a{font-size:.9rem}.adestock-site-nav .cta-button{padding:.75rem 1.35rem}}' +
            '@media (max-width:968px){.adestock-site-nav .menu-toggle{display:block}.adestock-site-nav .nav-links{display:none;position:absolute;top:100%;left:0;width:100%;flex-direction:column;align-items:flex-start;background:#fff;padding:1.25rem 1.5rem 1.5rem;box-shadow:0 14px 28px rgba(15,23,42,.12);border-bottom:1px solid rgba(15,23,42,.08);gap:1rem}.adestock-site-nav .nav-links.active{display:flex}.adestock-site-nav .nav-links li,.adestock-site-nav .nav-links a{width:100%}.adestock-site-nav .cta-button{width:100%;padding:.95rem 1.25rem}}';

        document.head.appendChild(style);
    }

    function markActive(nav) {
        var current = getCurrentPath();

        nav.querySelectorAll('[data-route]').forEach(function (link) {
            var route = link.getAttribute('data-route');
            var isActive = current === route || (route === 'blog/' && current.indexOf('blog/') === 0);

            if (isActive) {
                link.classList.add('is-active');
                link.setAttribute('aria-current', 'page');
            }
        });
    }

    function wireInteractions(nav) {
        var menuToggle = nav.querySelector('.menu-toggle');
        var navLinks = nav.querySelector('.nav-links');

        window.addEventListener('scroll', function () {
            if (window.scrollY > 50) {
                nav.classList.add('scrolled');
            } else {
                nav.classList.remove('scrolled');
            }
        });

        if (!menuToggle || !navLinks) {
            return;
        }

        menuToggle.addEventListener('click', function (event) {
            event.preventDefault();
            event.stopImmediatePropagation();

            var isOpen = navLinks.classList.toggle('active');
            menuToggle.setAttribute('aria-expanded', String(isOpen));
        });

        navLinks.querySelectorAll('a').forEach(function (link) {
            link.addEventListener('click', function () {
                navLinks.classList.remove('active');
                menuToggle.setAttribute('aria-expanded', 'false');
            });
        });
    }

    function keepSharedNavStructure(nav) {
        function removeLanguageSwitcher() {
            nav.querySelectorAll('.lang-switcher').forEach(function (switcher) {
                switcher.remove();
            });
        }

        removeLanguageSwitcher();

        if (window.MutationObserver) {
            var observer = new MutationObserver(removeLanguageSwitcher);
            observer.observe(nav, { childList: true, subtree: true });
        }
    }

    function mountNav() {
        injectNavStyles();

        var wrapper = document.createElement('div');
        wrapper.innerHTML = buildNav(getRelativePrefix());

        var nextNav = wrapper.firstElementChild;
        var currentNav = document.querySelector('nav.adestock-site-nav, nav.navbar, nav.seo-nav');
        var pageHeader = currentNav && currentNav.closest('.page-header');

        if (pageHeader) {
            pageHeader.replaceWith(nextNav);
            document.body.classList.add('nav-replaced-page-header');
        } else if (currentNav) {
            currentNav.replaceWith(nextNav);
        } else {
            document.body.insertBefore(nextNav, document.body.firstChild);
            document.body.classList.add('nav-injected');
        }

        markActive(nextNav);
        wireInteractions(nextNav);
        keepSharedNavStructure(nextNav);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', mountNav);
    } else {
        mountNav();
    }
})();