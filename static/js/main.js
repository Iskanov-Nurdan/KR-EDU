'use strict';

document.addEventListener('DOMContentLoaded', function () {

    // ── Back-to-top button ────────────────────────────────────────────────────
    const topBtn = document.getElementById('back-to-top');
    if (topBtn) {
        window.addEventListener('scroll', () => {
            topBtn.style.display = window.scrollY > 500 ? 'flex' : 'none';
        }, { passive: true });
        topBtn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
    }

    // ── Auto-dismiss alerts ───────────────────────────────────────────────────
    document.querySelectorAll('.alert-dismissible').forEach(el => {
        setTimeout(() => bootstrap.Alert.getOrCreateInstance(el)?.close(), 4500);
    });

    // ── SPA smooth-scroll (intercept /#section or #section links) ────────────
    const isIndex = window.location.pathname === '/' || window.location.pathname === '';
    const NAV_H = document.getElementById('mainNavbar')?.offsetHeight || 70;

    function scrollToSection(hash) {
        const target = document.getElementById(hash);
        if (!target) return false;
        const top = target.getBoundingClientRect().top + window.scrollY - NAV_H - 8;
        window.scrollTo({ top, behavior: 'smooth' });
        history.pushState(null, '', '#' + hash);
        // Close mobile menu
        const collapse = document.getElementById('mainNavCollapse');
        if (collapse && collapse.classList.contains('show')) {
            bootstrap.Collapse.getOrCreateInstance(collapse).hide();
        }
        return true;
    }

    document.querySelectorAll('a.spa-link, .main-nav a[data-section], .footer-nav a, a[href^="/#"], a[href^="#"]').forEach(link => {
        link.addEventListener('click', function (e) {
            const href = this.getAttribute('href') || '';
            let hash = null;
            if (href.startsWith('/#')) hash = href.slice(2);
            else if (href.startsWith('#')) hash = href.slice(1);
            if (!hash) return;

            if (isIndex) {
                e.preventDefault();
                scrollToSection(hash);
            } else {
                // Other pages: navigate to index with hash
                e.preventDefault();
                window.location.href = '/#' + hash;
            }
        });
    });

    // Handle initial hash on page load (e.g. navigating from news detail back to /#gallery)
    if (isIndex && window.location.hash) {
        const initHash = window.location.hash.slice(1);
        setTimeout(() => scrollToSection(initHash), 150);
    }

    // ── Scroll spy — highlight active nav link ────────────────────────────────
    if (isIndex) {
        const sections = Array.from(document.querySelectorAll('section[id]'));
        const navLinks = document.querySelectorAll('.main-nav a[data-section]');

        function updateActive() {
            const scrollMid = window.scrollY + NAV_H + window.innerHeight * 0.25;
            let current = sections[0];
            for (const s of sections) {
                if (s.offsetTop <= scrollMid) current = s;
            }
            navLinks.forEach(link => {
                link.classList.toggle('active', link.dataset.section === current?.id);
            });
        }

        window.addEventListener('scroll', updateActive, { passive: true });
        updateActive();
    }

    // ── Reveal animations (progressive enhancement) ──────────────────────────
    const revealEls = document.querySelectorAll('[data-reveal]');
    if (revealEls.length && 'IntersectionObserver' in window) {
        const DELAYS = ['0s', '.08s', '.16s', '.24s', '.32s', '.40s', '.48s'];

        // Mark body so CSS hides elements; without JS they stay visible
        document.body.classList.add('js-ready');

        const revealObserver = new IntersectionObserver(entries => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('revealed');
                    revealObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0, rootMargin: '0px 0px 0px 0px' });

        revealEls.forEach(el => {
            const d = parseInt(el.dataset.delay || '0', 10);
            el.style.transitionDelay = DELAYS[d] || '0s';
            revealObserver.observe(el);
        });
    }

    // ── Gallery JS category filter ────────────────────────────────────────────
    const filterBtns = document.querySelectorAll('.gallery-filter-btn');
    if (filterBtns.length) {
        filterBtns.forEach(btn => {
            btn.addEventListener('click', function () {
                const cat = this.dataset.cat;

                filterBtns.forEach(b => {
                    b.classList.remove('btn-primary');
                    b.classList.add('btn-outline-primary');
                });
                this.classList.add('btn-primary');
                this.classList.remove('btn-outline-primary');

                document.querySelectorAll('.g-item-wrap').forEach(item => {
                    const show = !cat || item.dataset.category === cat;
                    if (show) {
                        item.style.display = '';
                        // Force final visible state — bypasses the CSS reveal animation
                        // that would otherwise replay when display changes from none to ''
                        item.style.opacity = '1';
                        item.style.transform = 'none';
                        item.classList.add('revealed');
                    } else {
                        item.style.display = 'none';
                    }
                });
            });
        });
    }

    // ── Image preview on admin forms ──────────────────────────────────────────
    const imgInput = document.querySelector('input[type="file"][name="image"]');
    if (imgInput) {
        imgInput.addEventListener('change', function () {
            const file = this.files[0];
            if (!file || !file.type.startsWith('image/')) return;
            const reader = new FileReader();
            reader.onload = e => {
                let prev = document.getElementById('_img_prev');
                if (!prev) {
                    prev = document.createElement('img');
                    prev.id = '_img_prev';
                    prev.className = 'img-thumbnail mt-2 rounded';
                    prev.style.maxHeight = '180px';
                    imgInput.after(prev);
                }
                prev.src = e.target.result;
            };
            reader.readAsDataURL(file);
        });
    }

});
