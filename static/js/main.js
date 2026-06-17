'use strict';

document.addEventListener('DOMContentLoaded', function () {

    // ── Back-to-top ───────────────────────────────────────────────────────────
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

    // ════════════════════════════════════════════════════════════════════════════
    // HERO SLIDESHOW
    // ════════════════════════════════════════════════════════════════════════════
    (function initHeroSlideshow() {
        const slides       = Array.from(document.querySelectorAll('.hero-slide'));
        const dots         = Array.from(document.querySelectorAll('.hero-dot'));
        const captionEl    = document.getElementById('heroCaption');
        const captionText  = document.getElementById('heroCaptionText');
        const progressFill = document.getElementById('heroProgressFill');

        if (slides.length < 2) return;   // nothing to cycle

        const DURATION = 6000;           // ms per slide
        let current    = 0;
        let timer      = null;
        let progTimer  = null;
        let paused     = false;

        function showSlide(idx) {
            const prev = current;
            current    = (idx + slides.length) % slides.length;

            // Crossfade
            slides[prev].classList.remove('active');
            slides[prev].classList.add('leaving');
            slides[current].classList.add('active');

            // Clean leaving class after transition
            setTimeout(() => slides[prev].classList.remove('leaving'), 1900);

            // Dot indicators
            dots.forEach((d, i) => d.classList.toggle('active', i === current));

            // Caption
            if (captionEl && captionText) {
                const cap = slides[current].dataset.caption || '';
                if (cap) {
                    captionEl.classList.remove('visible');
                    setTimeout(() => {
                        captionText.textContent = cap;
                        captionEl.classList.add('visible');
                    }, 400);
                } else {
                    captionEl.classList.remove('visible');
                }
            }

            // Progress bar reset
            startProgress();
        }

        function startProgress() {
            if (!progressFill) return;
            // Reset
            progressFill.style.transition = 'none';
            progressFill.style.width = '0%';
            // Force reflow
            void progressFill.offsetWidth;
            // Run
            progressFill.style.transition = `width ${DURATION}ms linear`;
            progressFill.style.width = '100%';
        }

        function nextSlide() {
            if (!paused) showSlide(current + 1);
        }

        function startTimer() {
            clearInterval(timer);
            timer = setInterval(nextSlide, DURATION);
        }

        // Dot click
        dots.forEach((dot, i) => {
            dot.addEventListener('click', () => {
                showSlide(i);
                startTimer();  // restart interval
            });
        });

        // Pause on hover
        const heroEl = document.getElementById('hero');
        if (heroEl) {
            heroEl.addEventListener('mouseenter', () => { paused = true; });
            heroEl.addEventListener('mouseleave', () => { paused = false; });
        }

        // Touch swipe support
        let touchStartX = 0;
        const slidesEl = document.getElementById('heroSlides');
        if (slidesEl) {
            slidesEl.addEventListener('touchstart', e => { touchStartX = e.touches[0].clientX; }, { passive: true });
            slidesEl.addEventListener('touchend',   e => {
                const dx = e.changedTouches[0].clientX - touchStartX;
                if (Math.abs(dx) > 50) {
                    showSlide(dx < 0 ? current + 1 : current - 1);
                    startTimer();
                }
            }, { passive: true });
        }

        // Init: show caption for first slide, start progress + timer
        if (captionEl && captionText) {
            const firstCap = slides[0]?.dataset.caption || '';
            if (firstCap) {
                captionText.textContent = firstCap;
                setTimeout(() => captionEl.classList.add('visible'), 800);
            }
        }
        startProgress();
        startTimer();
    })();


    // ════════════════════════════════════════════════════════════════════════════
    // PARALLAX — hero slides translate at 35% scroll speed
    // ════════════════════════════════════════════════════════════════════════════
    (function initParallax() {
        const slidesContainer = document.getElementById('heroSlides');
        if (!slidesContainer) return;

        // Disable on reduced-motion
        if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

        // Disable on small screens (perf + mobile Safari issues)
        if (window.innerWidth < 768) return;

        let raf     = false;
        let lastY   = 0;

        function applyParallax() {
            const y   = window.scrollY;
            const max = window.innerHeight;
            if (y > max) { raf = false; return; }   // below hero, stop
            const shift = (y * 0.32).toFixed(2);
            slidesContainer.style.transform = `translateY(${shift}px)`;
            raf = false;
        }

        window.addEventListener('scroll', () => {
            if (!raf) {
                raf = true;
                requestAnimationFrame(applyParallax);
            }
        }, { passive: true });
    })();


    // ── SPA smooth-scroll ─────────────────────────────────────────────────────
    const isIndex = window.location.pathname === '/' || window.location.pathname === '';
    const NAV_H   = document.getElementById('mainNavbar')?.offsetHeight || 70;

    function scrollToSection(hash) {
        const target = document.getElementById(hash);
        if (!target) return false;
        const top = target.getBoundingClientRect().top + window.scrollY - NAV_H - 8;
        window.scrollTo({ top, behavior: 'smooth' });
        history.pushState(null, '', '#' + hash);
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
                e.preventDefault();
                window.location.href = '/#' + hash;
            }
        });
    });

    if (isIndex && window.location.hash) {
        const initHash = window.location.hash.slice(1);
        setTimeout(() => scrollToSection(initHash), 150);
    }

    // ── Scroll spy ────────────────────────────────────────────────────────────
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

    // ── Reveal animations ─────────────────────────────────────────────────────
    const revealEls = document.querySelectorAll('[data-reveal]');
    if (revealEls.length && 'IntersectionObserver' in window) {
        const DELAYS = ['0s', '.08s', '.16s', '.24s', '.32s', '.40s', '.48s'];
        document.body.classList.add('js-ready');

        const revealObserver = new IntersectionObserver(entries => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('revealed');
                    revealObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0, rootMargin: '0px 0px -20px 0px' });

        revealEls.forEach(el => {
            const d = parseInt(el.dataset.delay || '0', 10);
            el.style.transitionDelay = DELAYS[d] || '0s';
            revealObserver.observe(el);
        });
    }

    // ── Animated counters ─────────────────────────────────────────────────────
    function animateCount(el, target, duration) {
        const suffix = el.dataset.suffix || (el.textContent.includes('+') ? '+' : '');
        const start  = performance.now();

        function step(now) {
            const t   = Math.min((now - start) / duration, 1);
            const ease = 1 - Math.pow(1 - t, 3);           // ease-out cubic
            const cur  = Math.round(target * ease);
            el.textContent = cur.toLocaleString() + (t < 1 ? '' : suffix);
            if (t < 1) requestAnimationFrame(step);
        }
        requestAnimationFrame(step);
    }

    if ('IntersectionObserver' in window) {
        const counterObserver = new IntersectionObserver(entries => {
            entries.forEach(entry => {
                if (!entry.isIntersecting) return;
                const el     = entry.target;
                const target = parseInt(el.dataset.count || el.dataset.counter || el.textContent, 10);
                if (!isNaN(target) && target > 0) {
                    el.dataset.suffix = el.textContent.includes('+') ? '+' : '';
                    animateCount(el, target, 1400);
                }
                counterObserver.unobserve(el);
            });
        }, { threshold: 0.4 });

        document.querySelectorAll('[data-count], [data-counter]').forEach(el => {
            counterObserver.observe(el);
        });
    }

    // ── FAQ accordion icon toggle ─────────────────────────────────────────────
    document.querySelectorAll('.faq-question').forEach(btn => {
        const targetId = btn.dataset.bsTarget;
        if (!targetId) return;
        const collapseEl = document.querySelector(targetId);
        if (!collapseEl) return;
        collapseEl.addEventListener('show.bs.collapse', () => btn.setAttribute('aria-expanded', 'true'));
        collapseEl.addEventListener('hide.bs.collapse', () => btn.setAttribute('aria-expanded', 'false'));
    });

    // ── Gallery filter ────────────────────────────────────────────────────────
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
